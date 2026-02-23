import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

username_exact = "Rana"
username_lower = "rana"
password = "testpassword123"

auth_exact = authenticate(username=username_exact, password=password)
auth_lower = authenticate(username=username_lower, password=password)

print(f"Auth '{username_exact}': {auth_exact}")
print(f"Auth '{username_lower}': {auth_lower}")
