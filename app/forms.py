from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'role', 'user_img',
            'college_passout_img', 'experience_img', 'degree_img', 
            'designation', 'reporting', 'salary', 'address', 
            'education_detail', 'father_name', 'mother_name', 
            'siblings_name', 'phone_number', 'alt_phone_number'
        ]
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    role = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role Enter For Admin 0 or User 1'})
    )
    user_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    college_passout_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    experience_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    degree_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    designation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'})
    )
    reporting = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reporting'})
    )
    salary = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
    education_detail = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Education Details'})
    )
    father_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Father Name'})
    )
    mother_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mother Name'})
    )
    siblings_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Siblings Name'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    alt_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternate Phone Number'})
    )
        

    def clean(self):
        cleaned_data = super().clean()  # Call the parent class's clean method

        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        # Ensure password and password confirmation match
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match")

        return cleaned_data

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['title', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'placeholder': 'Reason for leave...'}),
        }
        
        
        
# Import your custom User model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'user_img',
            'college_passout_img',
            'experience_img',
            'degree_img',
            'phone_number',
            'alt_phone_number',
            'designation',
            'reporting',
            'salary',
            'address',
            'education_detail',
            'father_name',
            'mother_name',
            'siblings_name',
        ]
        
        widgets = {
            'email':forms.TextInput(attrs={'class': 'form-control'}),
            'user_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'college_passout_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'experience_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'degree_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'alt_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'reporting': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'education_detail': forms.Textarea(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'siblings_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)  # Required field

    class Meta:
        model = Project
        fields = ['user', 'task_name', 'task_description', 'task_priority']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'task_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task name'
            }),
            'task_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description',
                'rows': 4
            }),
            'task_priority': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


from .models import Holiday

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'dd-mm-yyyy'  # Placeholder is not typically used for date inputs
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'dd-mm-yyyy'  # Placeholder is not typically used for date inputs
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter reason for holiday',
                'rows': 3
            }),
        }


