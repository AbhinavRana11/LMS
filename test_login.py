import requests
url = "http://127.0.0.1:8000/api/token/"
data = {
    "username": "Rana",
    "password": "testpassword123"
}
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
