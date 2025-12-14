import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()

def run_verification():
    client = APIClient()
    
    print("--- Setup Users ---")
    user1_data = {'username': 'user_a', 'password': 'password123', 'email': 'a@example.com'}
    user2_data = {'username': 'user_b', 'password': 'password123', 'email': 'b@example.com'}
    user3_data = {'username': 'user_c', 'password': 'password123', 'email': 'c@example.com'}
    
    # helper for auth
    def get_token(user_data):
        response = client.post('/accounts/register/', user_data)
        if response.status_code == 201:
            return response.data['token'], response.data['user']['id']
        response = client.post('/accounts/login/', user_data)
        return response.data['token'], response.data['user_id']

    token1, id1 = get_token(user1_data)
    print(f"User A (ID: {id1}) Ready")
    token2, id2 = get_token(user2_data)
    print(f"User A (ID: {id2}) Ready")
    token3, id3 = get_token(user3_data)
    print(f"User C (ID: {id3}) Ready")

    print("\n--- Testing Follows & Feed ---")
    
    # 1. User B Creates a Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
    post_data = {'title': 'User B Post', 'content': 'Content for feed'}
    response = client.post('/api/posts/', post_data)
    if response.status_code == 201:
        print("User B Created Post")
        post_id = response.data['id']
    else:
        print("User B Failed to Create Post")
        return

    # 2. User A Follows User B
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    response = client.post(f'/accounts/follow/{id2}/')
    print(f"User A Follows User B: {response.status_code}")
    
    # 3. User A Checks Feed (Should see B's post)
    response = client.get('/api/feed/')
    print(f"User A Feed Status: {response.status_code}")
    feed_posts = response.data.get('results', []) if 'results' in response.data else response.data
    found = any(p['id'] == post_id for p in feed_posts)
    print(f"User A sees B's post: {found}")

    # 4. User C Checks Feed (Should NOT see B's post)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token3)
    response = client.get('/api/feed/')
    feed_posts_c = response.data.get('results', []) if 'results' in response.data else response.data
    found_c = any(p['id'] == post_id for p in feed_posts_c)
    print(f"User C sees B's post: {found_c}")

    # 5. User A Unfollows User B
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    response = client.post(f'/accounts/unfollow/{id2}/')
    print(f"User A Unfollows User B: {response.status_code}")
    
    # 6. User A Checks Feed (Should NOT see B's post)
    response = client.get('/api/feed/')
    feed_posts_a_new = response.data.get('results', []) if 'results' in response.data else response.data
    found_a_new = any(p['id'] == post_id for p in feed_posts_a_new)
    print(f"User A sees B's post after unfollow: {found_a_new}")

if __name__ == '__main__':
    run_verification()
