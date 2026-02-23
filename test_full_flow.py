import requests

base_url = "http://127.0.0.1:8000/api"
username = "instructor_test_3"
password = "testpassword123"

# 1. Register
reg_data = {
    "username": username,
    "password": password,
    "role": "instructor"
}
reg_res = requests.post(f"{base_url}/accounts/register/", json=reg_data)
print(f"Registration: {reg_res.status_code}")
print(reg_res.text)

# 2. Login
login_data = {
    "username": username,
    "password": password
}
login_res = requests.post(f"{base_url}/token/", json=login_data)
print(f"Login: {login_res.status_code}")
if login_res.status_code != 200:
    print("Login failed")
    exit()

token = login_res.json().get("access")

# 3. Create Course
course_data = {
    "title": "New Course via API",
    "description": "Description",
    "price": 499.00
}
headers = {"Authorization": f"Bearer {token}"}
course_res = requests.post(f"{base_url}/courses/", json=course_data, headers=headers)
print(f"Create Course: {course_res.status_code}")
print(course_res.text)
