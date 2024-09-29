from rest_framework import serializers
from .models import *


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        return attrs
    
    
# serializers.py
from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user', 'check_in', 'check_out', 'total_hours']



class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['id', 'user', 'title', 'start_date', 'end_date', 'reason', 'is_approved', 'total_days']
        read_only_fields = ['id', 'user', 'is_approved', 'total_days']  # Make some fields read-only




class UserProfileSerializer(serializers.ModelSerializer):
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
        
        
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'task_name', 'task_description', 'task_priority', 'created_at']
        read_only_fields = ['id', 'created_at']

