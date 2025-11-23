import os
import sys
from pathlib import Path

# Adjust path to find the Django project
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

username = 'apiuser'
email = 'apiuser@example.com'
password = 'password123'

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
if created:
    user.set_password(password)
    user.save()
    print(f'Created user {username} with password: {password}')
else:
    print(f'User {username} already exists')

token, _ = Token.objects.get_or_create(user=user)
print('Token:', token.key)
print('\nUse this token in requests as:')
print("Authorization: Token <token>")
