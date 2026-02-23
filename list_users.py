import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from users.models import User

users = User.objects.all()
print("ID | Username | Role")
print("-" * 30)
for u in users:
    print(f"{u.id} | '{u.username}' | {u.role}")
