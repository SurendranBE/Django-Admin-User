from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# employee register 
def register_employee(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.role = 1  # Employee role
            user.save()
            # Set the backend attribute
            user.backend = 'cqt_app.backends.EmailBackend'  # Replace 'yourapp' with the actual app name
            login(request, user)  # Automatically log the user in after registration
            return redirect('admin_login') 
        else:
            print(form.errors)
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})




# employee login 
def employee_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            print(f"Attempting to authenticate user with email: {email}")
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.role == 1:  # Check if the user has role 1 (employee)
                    print(f"Authenticated User: {user.email}, Role: {user.role}")
                    login(request, user)
                    print(f"User is logged in: {request.user.is_authenticated}")
                    # Redirect to the dashboard for employees
                    return redirect('dashboard')
            else:
                print("User authentication failed.")
                form.add_error(None, "Invalid email or password for Employee.")
    else:
        form = CustomLoginForm()

    return render(request, 'employee/login.html', {'form': form})




@login_required
# Employee Dashboard View
def dashboard(request):
    return render(request, 'employee/dashboard.html')




@login_required
# addendance for employee
def attendance_view(request):
    user = request.user
    
    if user.role != 1:  # If the user is not an employee
        return HttpResponseForbidden("You do not have permission to view this page.") 
    # Proceed if the user is an employee
    attendance_records = Attendance.objects.filter(user=user).order_by('-check_in')
    
    return render(request, 'employee/attendance.html', {'attendance_records': attendance_records})




@login_required
# check in for employee
def check_in(request):
    user = request.user
    if request.method == 'POST':
        if not Attendance.objects.filter(user=user, check_out__isnull=True).exists():
            # Create a new check-in record with current time
            Attendance.objects.create(user=user, check_in=timezone.now())
            return redirect('attendance')
        else:
            return render(request, 'attendance.html', {'error': 'You have already checked in.'})
    return render(request, 'employee/attendance.html')




@login_required
# check out employee
def check_out(request):
    user = request.user  # CustomUser instance
    # Find the latest open check-in record (i.e., check-out is not set)
    attendance_record = Attendance.objects.filter(user=user, check_out__isnull=True).last()
    if attendance_record and request.method == 'POST':
        attendance_record.check_out = timezone.now()
        attendance_record.save()  # Save the updated check-out time
        return redirect('attendance')
    return render(request, 'employee/attendance.html', {'error': 'No check-in record found.'})




@login_required
# break in employee
def break_in(request):
    user = request.user  # CustomUser instance
    if request.method == 'POST':
        # Get the last open check-in record where the user hasn't taken a break yet
        attendance_record = Attendance.objects.filter(user=user, check_out__isnull=True, break_in__isnull=True).last()
        if attendance_record:
            # Set the break-in time
            attendance_record.break_in = timezone.now()
            attendance_record.save()
            return redirect('attendance')
        else:
            # No open check-in or break already started
            return render(request, 'attendance.html', {'error': 'No open check-in record or break already started.'})
    return render(request, 'employee/attendance.html')





@login_required
# Break-out view employee
def break_out(request):
    user = request.user  # CustomUser instance
    # Check if the user has checked in, started a break, but hasn't checked out yet
    attendance_record = Attendance.objects.filter(user=user, check_out__isnull=True, break_in__isnull=False, break_out__isnull=True).last()
    if attendance_record and request.method == 'POST':
        # Set the break-out time
        attendance_record.break_out = timezone.now()
        attendance_record.save()
        return redirect('attendance')
    return render(request, 'employee/attendance.html', {'error': 'No active break found.'})





@login_required
# leave apply for employee
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user  # Set the current user
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('dashboard')
    else:
        form = LeaveForm()
    return render(request, 'employee/apply_leave.html', {'form': form})





@login_required
# profile view employee
def profile(request):
    user = request.user
    profile = get_object_or_404(User, username=user.username) 
    return render(request, 'employee/profile_view.html',{'user':user,'profile': profile})





@login_required
# profile_update employee
def profile_update(request):
    user = request.user
    profile = get_object_or_404(User, username=user.username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile view after updating
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'employee/profile_update.html', {'form': form, 'profile': profile})





@login_required
# project employee
def project(request):
    user_projects = Project.objects.filter(user=request.user)
    print(user_projects) 
    context = {
        'user_projects': user_projects,
    }
    return render(request,'employee/project_view.html',context)




@login_required
# holliday employee
def holiday(request):
    holidays =  Holiday.objects.all()
    return render(request,'employee/holiday_view.html',{'holidays':holidays})



@login_required
def logout(request):
    request.session.flush()
    return redirect('employee_login')


# ==============================================================  ADMIN CODE ======================================================

# Admin Login View
def admin_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            # If username_or_email is an email, try with EmailBackend
            if user is None:
                user = authenticate(request, email=username_or_email, password=password)
            # Check if user is valid and has the admin role
            if user is not None:
                if user.role == 0:  # Assuming 0 is for Admin
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    form.add_error(None, "You do not have admin access.")
            else:
                form.add_error(None, "Invalid username or password for Admin.")
    else:
        form = CustomLoginForm()
    return render(request, 'admin/admin_login.html', {'form': form})





@login_required
# Admin Dashboard View
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')



# admin leave aproval
@login_required
def leave_approval(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        
        leave = get_object_or_404(Leave, id=leave_id)
        
        if action == 'approve':
            leave.is_approved = True
            leave.save()
            messages.success(request, 'Leave approved successfully!')
        elif action == 'reject':
            leave.is_approved = False
            leave.save()
            messages.error(request, 'Leave rejected successfully!')

        return redirect('leave_approval')  # Redirect to the same page to refresh the list

    # Display pending leave requests
    leave_requests = Leave.objects.filter(is_approved=False)
    return render(request, 'admin/leave_approval.html', {'leave_requests': leave_requests})




# admin project list
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'admin/project_list.html', {'projects': projects})




# admin project create
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user 
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'admin/project_form.html', {'form': form})



# admin project update
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'admin/project_form.html', {'form': form})




# admin project delete
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'admin/project_confirm_delete.html', {'project': project})



# admin holiday list
@login_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'admin/holiday_list.html', {'holidays': holidays})



# admin create holiday
@login_required
def holiday_create(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm()
    return render(request, 'admin/holiday_form.html', {'form': form})




# admin holiday update
@login_required
def holiday_update(request, pk):
    holiday = Holiday.objects.get(pk=pk)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm(instance=holiday)
    return render(request, 'admin/holiday_form.html', {'form': form})




# admin holiday delete
@login_required
def holiday_delete(request, pk):
    holiday = Holiday.objects.get(pk=pk)
    if request.method == 'POST':
        holiday.delete()
        return redirect('holiday_list')
    return render(request, 'admin/holiday_confirm_delete.html', {'holiday': holiday})


# admin attendance list
@login_required
def attendance_list(request):
    # Fetch attendance records, optionally filter by user or date
    attendances = Attendance.objects.select_related('user').all()

    return render(request, 'admin/attendance_list.html', {'attendances': attendances})


# logout
@login_required
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')




