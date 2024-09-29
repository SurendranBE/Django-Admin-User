from rest_framework import status
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
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "You are not authorized to log in as an employee."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "Invalid email or password for Employee."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(APIView):
    def post(self, request):
        user = request.user  # Assumes the user is authenticated
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
    
    


