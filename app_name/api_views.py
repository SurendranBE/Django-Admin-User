from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.permissions import AllowAny
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404




# Employee Login
class EmployeeLoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        
        if serializer.is_valid(): 
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.role == 1: 
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,'message': 'User login Successfully'}, status=status.HTTP_200_OK)
                
                elif user.role == 0:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'message': 'admin login Successfully'},status.HTTP_200_OK)
                
                else:
                    return Response({"error": "You are not authorized to log in as an employee."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "Invalid email or password for Employee."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Employee Change Password
class PasswordChangeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Employee Attendave api
class AttendanceView(APIView):
    def post(self, request):
        user = request.user 
        # Check if there is an active attendance for today (without check-out)
        attendance = Attendance.objects.filter(user=user, check_in__date=now().date()).first()
        if attendance and attendance.check_out is None:
            # If there is a check-in without a check-out, perform check-out
            check_out_time = now()
            attendance.check_out = check_out_time
            attendance.save()
            serializer = AttendanceSerializer(attendance)
            return Response({
                'detail': 'Checked out successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        elif attendance and attendance.check_out is not None:
            # If the user has already checked in and checked out today, prevent further action
            return Response({
                'detail': 'User has already checked out today.'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Perform check-in if there is no attendance for today
            check_in_time = now()
            attendance = Attendance.objects.create(user=user, check_in=check_in_time)
            serializer = AttendanceSerializer(attendance)
            return Response({
                'detail': 'Checked in successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

    
    
    
    
# post method Leave Create
class LeaveListCreateView(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
# get method for view profile and then put method for update your details
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Retrieve the currently authenticated user
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  # Return updated data as response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

# Project Create API (Admin Side)

class ProjectCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Project View for Employees 

class EmployeeProjectListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get projects assigned to the logged-in user
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# Project Update API (Admin Side)

class ProjectUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project update Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Project Delete API (Admin Side)

class ProjectDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({'message': 'Project delete successfully'},status=status.HTTP_204_NO_CONTENT)




# Admin Create Holiday
class HolidayCreateAPI(APIView):
    permission_classes = [IsAuthenticated]  # Only admin can create

    def post(self, request):
        serializer = HolidaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Holiday created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Update Holiday
class HolidayUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]  # Only admin can update

    def put(self, request, pk):
        holiday = get_object_or_404(Holiday, pk=pk)
        serializer = HolidaySerializer(holiday, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Holiday updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Delete Holiday
class HolidayDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]  # Only admin can delete

    def delete(self, request, pk):
        holiday = get_object_or_404(Holiday, pk=pk)
        holiday.delete()
        return Response({"message": "Holiday deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Employee List Holidays
class EmployeeHolidayListAPI(APIView):
    permission_classes = [IsAuthenticated]  # All employees can view holidays

    def get(self, request):
        holidays = Holiday.objects.all()
        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Admin Attendance List API
class AdminAttendanceListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attendances = Attendance.objects.select_related('user').all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# Admin Leave List API
class AdminLeaveListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaves = Leave.objects.select_related('user').all()
        serializer = LeaveApprovalSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Admin Leave Approval API
class AdminLeaveApprovalAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({"detail": "Leave request not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveApprovalSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



