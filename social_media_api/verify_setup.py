import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

def run_verification():
    client = APIClient()
    
    # 1. Register
    print("Testing Registration...")
    reg_data = {
        'username': 'testuser_verify_2',
        'password': 'password123',
        'email': 'verify2@example.com',
        'bio': 'Verification bio'
    }
    response = client.post('/accounts/register/', reg_data)
    print(f"Register Status: {response.status_code}")
    
    token = None
    if response.status_code == 201:
        print("Registration Successful")
        token = response.data.get('token')
    else:
        print(f"Registration Failed: {response.data}")
        # If user exists from previous run, try login
        if "username" in response.data and "already exists" in str(response.data["username"]):
             print("User already exists, proceeding to login...")

    # 2. Login
    print("\nTesting Login...")
    login_data = {
        'username': 'testuser_verify_2',
        'password': 'password123'
    }
    response = client.post('/accounts/login/', login_data)
    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        print("Login Successful")
        token = response.data.get('token')
    else:
        print(f"Login Failed: {response.data}")

    # 3. Profile
    if token:
        print("\nTesting Profile...")
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/accounts/profile/')
        print(f"Profile Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Profile Data: {response.data}")
        else:
            print(f"Profile Failed: {response.data}")
    else:
        print("\nSkipping Profile test (No token)")

if __name__ == '__main__':
    run_verification()
