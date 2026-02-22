from rest_framework import serializers
from .models import Course, Lesson, Enrollment, Assignment, Submission, Review

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')
    
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.ReadOnlyField(source='instructor.username')
    lessons = LessonSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor']

class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['student']
