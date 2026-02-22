import requests
url = "http://127.0.0.1:8000/api/accounts/register/"
data = {
    "username": "testuser_unique_123",
    "password": "testpassword123",
    "role": "student"
}
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
