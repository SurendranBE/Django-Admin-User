from django.urls import path
from .views import *
from .api_views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # EMPLOYEE URLS
    path('register/', register_employee, name='employee_register'),
    path('employee/login/', employee_login_view, name='employee_login'),
    path('employee/dashboard/', dashboard, name='dashboard'),
    path('check-in/', check_in, name='check_in'), 
    path('check-out/', check_out, name='check_out'),  
    path('break-in/', break_in, name='break_in'), 
    path('break-out/', break_out, name='break_out'),  
    path('attendance/', attendance_view, name='attendance'),
    path('leave/', apply_leave, name='leave'),
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('project',project,name='project'),
    path('holiday', holiday, name='holiday'),
    path('logout',logout,name='logout'),
    
    
    
    # ADMIN URLS
    path('alogin/', admin_login_view, name='admin_login'),
    path('adashboard/', admin_dashboard, name='admin_dashboard'),
    path('leave_approval/', leave_approval, name='leave_approval'),
    path('projects/',project_list, name='project_list'),
    path('projects/create/', project_create, name='project_create'),
    path('projects/<int:pk>/update/', project_update, name='project_update'),
    path('projects/<int:pk>/delete/', project_delete, name='project_delete'),
    path('holiday_list', holiday_list, name='holiday_list'),
    path('holiday_create/', holiday_create, name='holiday_create'),
    path('<int:pk>/edit/', holiday_update, name='holiday_update'),
    path('<int:pk>/delete/', holiday_delete, name='holiday_delete'),
    path('attendance_list/', attendance_list, name='attendance_list'),
    path('admin_logout', admin_logout, name='admin_logout'),
    
    
    
    #API URL EMPLOYEE
    path('api/login/', EmployeeLoginAPI.as_view(), name='api_employee_login'),#same for Admin And Employee
    path('api/attendance/', AttendanceView.as_view(), name='api_attendance'),
    path('api/leaves/', LeaveListCreateView.as_view(), name='leave-list-create'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),#update and view two in one url
    path('api/projects/view/', EmployeeProjectListAPI.as_view(), name='employee_project_list_api'),
    path('api/holidays/view/', EmployeeHolidayListAPI.as_view(), name='employee_holiday_list_api'),
    path('api/password/change/', PasswordChangeAPI.as_view(), name='password_change_api'),
     
     
     
    #  API URL FOR ADMIN
    path('api/projects/create/', ProjectCreateAPI.as_view(), name='project_create_api'),
    path('api/projects/update/<int:pk>/', ProjectUpdateAPI.as_view(), name='project_update_api'),
    path('api/projects/delete/<int:pk>/', ProjectDeleteAPI.as_view(), name='project_delete_api'),
    path('api/holidays/create/', HolidayCreateAPI.as_view(), name='holiday_create_api'),
    path('api/holidays/update/<int:pk>/', HolidayUpdateAPI.as_view(), name='holiday_update_api'),
    path('api/holidays/delete/<int:pk>/', HolidayDeleteAPI.as_view(), name='holiday_delete_api'),
    path('api/attendances/view/', AdminAttendanceListAPI.as_view(), name='admin_attendance_list_api'),
    path('api/leaves/view/', AdminLeaveListAPI.as_view(), name='admin_leave_list_api'),
    path('api/leaves/approve/<int:pk>/', AdminLeaveApprovalAPI.as_view(), name='admin_leave_approval_api'),#put method


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


