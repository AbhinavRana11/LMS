import requests
import sys

def check_server(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print("Response Content (first 500 chars):")
        print(response.text[:500])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_server(sys.argv[1])
    else:
        check_server("http://127.0.0.1:8000/")
