from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Employee'),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)
    email = models.EmailField(unique=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    user_img = models.ImageField(upload_to='user_img/', null=True, blank=True)
    college_passout_img = models.ImageField(upload_to='college_passout_img/', null=True, blank=True)
    experience_img = models.ImageField(upload_to='experience_img/', null=True, blank=True)
    degree_img = models.ImageField(upload_to='degree_img/', null=True, blank=True)
    designation = models.CharField(max_length=100,null=True, blank=True)
    reporting = models.CharField(max_length=100,null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    education_detail = models.TextField(null=True, blank=True)
    father_name = models.CharField(max_length=100,null=True, blank=True)
    mother_name = models.CharField(max_length=100,null=True, blank=True)
    siblings_name = models.CharField(max_length=200,null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    alt_phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username



class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True, blank=True)
    break_in = models.DateTimeField(null=True, blank=True)
    break_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)

    @property
    def total_hours(self):
        if self.check_in and self.check_out:
            duration = self.check_out - self.check_in
            total_duration = duration.total_seconds() / 3600
            
            # Subtract break time if breaks were taken
            if self.break_in and self.break_out:
                break_duration = self.break_out - self.break_in
                total_duration -= break_duration.total_seconds() / 3600
            
            return total_duration
        
        return 0

    @property
    def total_days(self):
        if self.check_in and self.check_out:
            delta = self.check_out.date() - self.check_in.date()
            return delta.days + 1  # Include the first day
        
        return 0

    class Meta:
        db_table = 'attendace'




class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)
    

    class Meta:
        db_table = 'leave'
    
    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.user} leave from {self.start_date} to {self.end_date}"
    
    
    
    
    
class Project(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]
    
    # Fields for the Project model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects') 
    task_name = models.CharField(max_length=255) 
    task_description = models.TextField()
    task_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)  # Task priority choice
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project'

    # String representation of the model
    def __str__(self):
        return f"Project for {self.user.username} - {self.task_name}"

    # Method to count all tasks
    @staticmethod
    def count_total_tasks():
        return Project.objects.count()

    # Method to count tasks created today
    @staticmethod
    def count_today_tasks():
        today = timezone.now().date()
        return Project.objects.filter(created_at__date=today).count()

    # Method to count tasks created yesterday
    @staticmethod
    def count_yesterday_tasks():
        yesterday = timezone.now().date() - timedelta(days=1)
        return Project.objects.filter(created_at__date=yesterday).count()
    
    



class Holiday(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.reason} from {self.start_date} to {self.end_date}"
    
    class Meta:
        db_table = 'holiday'