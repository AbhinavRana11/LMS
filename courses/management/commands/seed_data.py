from django.core.management.base import BaseCommand
from users.models import User
from courses.models import Course, Lesson, Assignment
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Seeds initial demo data for the LMS showcase'

    def handle(self, *args, **kwargs):
        # 1. Get or Create Instructor
        instructor, created = User.objects.get_or_create(
            username='harsh',
            defaults={'role': 'instructor', 'email': 'harsh@mycourse.com'}
        )
        if created:
            instructor.set_password('pass123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS(f'Created instructor: {instructor.username}'))

        # 2. Define Demo Courses
        demo_courses = [
            {
                'title': 'Mastering Python for Distributed Systems',
                'description': 'Learn how to build scalable, high-performance backends with Python, FastAPI, and Redis. This course covers concurrency, microservices, and modern deployment strategies.',
                'price': 1299.00,
                'lessons': [
                    {'title': 'Introduction to AsyncIO', 'content': 'Getting started with asynchronous programming in Python...', 'order': 1},
                    {'title': 'Redis for Caching', 'content': 'How to implement efficient caching layers using Redis...', 'order': 2},
                ],
                'assignment': {'title': 'Build a Scalable API', 'description': 'Create a FastAPI service that handles 1000 requests per second.'}
            },
            {
                'title': 'Modern UI/UX Design Essentials',
                'description': 'A deep dive into visual hierarchy, typography, and glassmorphism. Learn to design high-fidelity prototypes that stand out in 2026.',
                'price': 899.00,
                'lessons': [
                    {'title': 'The Power of White Space', 'content': 'Why more room means better UX...', 'order': 1},
                    {'title': 'Advanced Glassmorphism', 'content': 'Mastering the blur and transparency effects...', 'order': 2},
                ],
                'assignment': {'title': 'Redesign a SaaS Hero Section', 'description': 'Create a high-fidelity Figma mockup of a modern SaaS hero.'}
            },
            {
                'title': 'The SaaS Founders Playbook',
                'description': 'Moving from idea to $10k MRR. Comprehensive business strategies for engineer-led SaaS products, focusing on product-market fit and growth loops.',
                'price': 2499.00,
                'lessons': [
                    {'title': 'Finding Product-Market Fit', 'content': 'Strategies for validating your SaaS idea...', 'order': 1},
                    {'title': 'Growth Loops vs Funnels', 'content': 'Implementing viral growth mechanics...', 'order': 2},
                ],
                'assignment': {'title': 'Draft your GTM Strategy', 'description': 'Write a 2-page go-to-market plan for your product.'}
            }
        ]

        # 3. Create Courses, Lessons, and Assignments
        for course_data in demo_courses:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'instructor': instructor,
                    'price': course_data['price']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Course: {course.title}'))
                
                # Add Lessons
                for l_data in course_data['lessons']:
                    Lesson.objects.create(
                        course=course,
                        title=l_data['title'],
                        content=l_data['content'],
                        order=l_data['order']
                    )
                
                # Add Assignment
                a_data = course_data['assignment']
                Assignment.objects.create(
                    course=course,
                    title=a_data['title'],
                    description=a_data['description'],
                    deadline=timezone.now() + datetime.timedelta(days=14)
                )
            else:
                self.stdout.write(self.style.WARNING(f'Course already exists: {course.title}'))

        self.stdout.write(self.style.SUCCESS('Demo data seeding complete!'))
