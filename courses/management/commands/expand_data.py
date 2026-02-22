from django.core.management.base import BaseCommand
from users.models import User
from courses.models import Course, Lesson, Assignment, Review
from django.utils import timezone
import datetime
import random

class Command(BaseCommand):
    help = 'Expands the course library with more diverse demo items'

    def handle(self, *args, **kwargs):
        instructor, created = User.objects.get_or_create(
            username='harsh',
            defaults={'role': 'instructor', 'email': 'harsh@mycourse.com'}
        )
        if created:
            instructor.set_password('pass123')
            instructor.save()

        # Ensure we have some students for reviews
        if User.objects.filter(role='student').count() < 3:
            for i in range(3):
                u, created = User.objects.get_or_create(username=f'student_{i}', defaults={'role': 'student'})
                if created:
                    u.set_password('pass123')
                    u.save()

        extra_courses = [
            {
                'title': 'Digital Marketing Mastery 2026',
                'description': 'Master SEO, SEM, and Social Media Growth. Learn to run highly profitable ad campaigns on modern platforms.',
                'price': 1499.00,
                'banner': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80',
                'category': 'Marketing',
                'lessons': ['Introduction to SEM', 'Advanced Facebook Ads']
            },
            {
                'title': 'Financial Analysis & Valuation',
                'description': 'A deep dive into corporate finance, stock valuation, and investment banking essentials. Perfect for aspiring analysts.',
                'price': 2999.00,
                'banner': 'https://images.unsplash.com/photo-1611974714025-e8a48550428d?w=800&q=80',
                'category': 'Finance & Accounting',
                'lessons': ['DCF Modeling', 'Ratio Analysis']
            },
            {
                'title': 'The Complete Graphic Design Bootcamp',
                'description': 'Learn Photoshop, Illustrator, and Canva. Create stunning brand identities from scratch.',
                'price': 699.00,
                'banner': 'https://images.unsplash.com/photo-1541462608141-ad60397d44c5?w=800&q=80',
                'category': 'Design',
                'lessons': ['Color Theory', 'Logo Design Fundamentals']
            },
            {
                'title': 'Cybersecurity Fundamentals',
                'description': 'Protect your data and networks. Learn ethical hacking, encryption, and risk management.',
                'price': 1899.00,
                'banner': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80',
                'category': 'IT & Software',
                'lessons': ['Network Security', 'Ethical Hacking Intro']
            },
            {
                'title': 'AI & Machine Learning Masterclass',
                'description': 'From linear regression to deep learning. Build real-world AI projects with Python.',
                'price': 4500.00,
                'banner': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
                'category': 'Development',
                'lessons': ['Neural Networks Intro', 'Computer Vision Basics']
            },
            {
                'title': 'The Product Management Handbook',
                'description': 'Master the art of building products that sell. Strategy, UX, and market fit.',
                'price': 8999.00,
                'banner': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80',
                'category': 'Business',
                'lessons': ['Discovery & Framing', 'Product Roadmap Design']
            },
            {
                'title': 'Next.js 15: Full Stack Powerhouse',
                'description': 'Build blazingly fast web apps with the latest Next.js features and App Router.',
                'price': 2200.00,
                'banner': 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800&q=80',
                'category': 'Development',
                'lessons': ['Server Components', 'Streaming & Suspense']
            },
            {
                'title': 'Django REST API: Backend Development',
                'description': 'Build production-ready REST APIs with Django and Django REST Framework. Authentication, serializers, and deployment.',
                'price': 1799.00,
                'banner': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80',
                'category': 'Development',
                'lessons': ['REST Basics', 'JWT Authentication', 'Deployment']
            },
            {
                'title': 'Data Structures & Algorithms in Python',
                'description': 'Master arrays, trees, graphs, and dynamic programming. Ace your coding interviews.',
                'price': 999.00,
                'banner': 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&q=80',
                'category': 'Development',
                'lessons': ['Big O & Arrays', 'Trees and Graphs', 'Dynamic Programming']
            },
            {
                'title': 'Cloud DevOps with AWS',
                'description': 'CI/CD, containers, and infrastructure as code. Deploy and scale applications on AWS.',
                'price': 3299.00,
                'banner': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80',
                'category': 'IT & Software',
                'lessons': ['EC2 & VPC', 'Docker & ECS', 'Terraform Basics']
            },
            {
                'title': 'React Native: Mobile App Development',
                'description': 'Build cross-platform iOS and Android apps with React Native and Expo.',
                'price': 2499.00,
                'banner': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&q=80',
                'category': 'Development',
                'lessons': ['Setup & Components', 'Navigation', 'APIs & State']
            },
            {
                'title': 'SQL & Database Design',
                'description': 'Write efficient queries, design schemas, and optimize performance. PostgreSQL and MySQL.',
                'price': 1199.00,
                'banner': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=800&q=80',
                'category': 'Development',
                'lessons': ['SELECT & JOINs', 'Indexes & Optimization', 'Transactions']
            },
            {
                'title': 'Leadership & Team Management',
                'description': 'Lead remote and hybrid teams. Communication, delegation, and performance reviews.',
                'price': 1599.00,
                'banner': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80',
                'category': 'Business',
                'lessons': ['One-on-Ones', 'Feedback Culture', 'Remote Leadership']
            },
            {
                'title': 'Fitness & Nutrition Fundamentals',
                'description': 'Science-based workout and nutrition plans. Build sustainable healthy habits.',
                'price': 799.00,
                'banner': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&q=80',
                'category': 'Health & Fitness',
                'lessons': ['Nutrition Basics', 'Strength Training', 'Recovery & Sleep']
            }
        ]

        comments = [
            "Amazing course! Learned so much about this topic.",
            "Harsh is a great instructor. Very clear explanations.",
            "Good content, but some parts were a bit too advanced for me.",
            "Excellent value for money. Highly recommend!",
            "Sublime production quality and very insightful lessons.",
            "The best course on this subject I've found so far."
        ]

        for c_data in extra_courses:
            course, created = Course.objects.get_or_create(
                title=c_data['title'],
                defaults={
                    'description': c_data['description'],
                    'instructor': instructor,
                    'price': c_data['price'],
                    'banner_image': c_data['banner'],
                    'category': c_data['category']
                }
            )
            
            # Always sync fields
            course.description = c_data['description']
            course.instructor = instructor
            course.price = c_data['price']
            course.banner_image = c_data['banner']
            course.category = c_data['category'] # Sync category
            course.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Added: {course.title}'))
                for i, l_title in enumerate(c_data['lessons']):
                    Lesson.objects.create(course=course, title=l_title, content="Enjoy this lesson!", order=i+1)
                Assignment.objects.create(
                    course=course, 
                    title="Final Project", 
                    description="Submit your work.", 
                    deadline=timezone.now() + datetime.timedelta(days=7)
                )

            # Seed Reviews if they don't exist
            if not course.reviews.exists():
                students = User.objects.filter(role='student')
                for s in students.order_by('?')[:random.randint(2, 4)]:
                    Review.objects.create(
                        course=course,
                        student=s,
                        rating=random.randint(4, 5),
                        comment=random.choice(comments)
                    )
                
                # Update Course Totals
                revs = Review.objects.filter(course=course)
                course.rating_count = revs.count()
                course.average_rating = round(sum(r.rating for r in revs) / revs.count(), 1)
                course.save()

        self.stdout.write(self.style.SUCCESS('Course expansion complete!'))
