from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from courses.models import Enrollment
from courses.serializers import CourseSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
        data['enrolled_courses'] = CourseSerializer([e.course for e in enrollments], many=True).data
        return Response(data)
