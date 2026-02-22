from django.db import models
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson, Enrollment, Assignment, Submission, Review
from .serializers import *
from lms_project.utils import send_lms_email

class CourseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Course.objects.all()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category__iexact=category)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(description__icontains=search)
            )
        return queryset

    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()] # Simplified for now, can add IsInstructor
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
        if created:
            send_lms_email(
                f"Welcome to {course.title}!",
                f"Hi {request.user.username},\n\nYou have successfully enrolled in {course.title}. Start learning now!",
                [request.user.email] if request.user.email else []
            )
            return Response({'status': 'enrolled'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already enrolled'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def stats(self, request):
        user = request.user
        if user.role == 'instructor' or user.role == 'admin':
            courses = Course.objects.filter(instructor=user)
            submissions = Submission.objects.filter(assignment__course__instructor=user)
            total_courses = courses.count()
            total_enrollments = Enrollment.objects.filter(course__in=courses).count()
            total_revenue = sum(c.price for c in courses) * total_enrollments
        else:
            # Student: my enrolled courses and my submissions
            total_courses = Enrollment.objects.filter(student=user).count()
            submissions = Submission.objects.filter(student=user)
            total_enrollments = total_courses
            total_revenue = 0

        total_submissions = submissions.count()
        graded_subs = submissions.filter(score__isnull=False)
        avg_score = graded_subs.aggregate(models.Avg('score'))['score__avg'] or 0
        avg_grade = "N/A"
        if avg_score >= 90: avg_grade = "A"
        elif avg_score >= 80: avg_grade = "B"
        elif avg_score >= 70: avg_grade = "C"
        elif avg_score > 0: avg_grade = "D"

        return Response({
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'total_revenue': total_revenue,
            'total_submissions': total_submissions,
            'average_grade': avg_grade
        })

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def grade(self, request, pk=None):
        submission = self.get_object()
        # Simplified: check if user is instructor of the course
        submission.score = request.data.get('score')
        submission.feedback = request.data.get('feedback')
        submission.grade = request.data.get('grade')
        submission.save()
        return Response({'status': 'graded'})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        review = serializer.save(student=self.request.user)
        self.update_course_rating(review.course)

    def perform_update(self, serializer):
        review = serializer.save()
        self.update_course_rating(review.course)

    def perform_destroy(self, instance):
        course = instance.course
        instance.delete()
        self.update_course_rating(course)

    def update_course_rating(self, course):
        reviews = Review.objects.filter(course=course)
        count = reviews.count()
        if count > 0:
            avg = sum(r.rating for r in reviews) / count
            course.average_rating = round(avg, 1)
            course.rating_count = count
        else:
            course.average_rating = 0.0
            course.rating_count = 0
        course.save()

    @action(detail=False, methods=['get'], url_path='course/(?P<course_id>[^/.]+)')
    def course_reviews(self, request, course_id=None):
        reviews = Review.objects.filter(course_id=course_id).order_by('-created_at')
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
