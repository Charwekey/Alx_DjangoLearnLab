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
    
    def get_token(user_data):
        response = client.post('/accounts/register/', user_data)
        if response.status_code == 201:
            return response.data['token'], response.data['user']['id']
        response = client.post('/accounts/login/', user_data)
        return response.data['token'], response.data['user_id']

    token1, id1 = get_token(user1_data)
    print(f"User A (ID: {id1}) Ready")
    token2, id2 = get_token(user2_data)
    print(f"User B (ID: {id2}) Ready")

    print("\n--- Testing Likes & Notifications ---")
    
    # 1. User B Creates a Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
    post_data = {'title': 'Likeable Post', 'content': 'Please like this!'}
    response = client.post('/api/posts/', post_data)
    if response.status_code == 201:
        post_id = response.data['id']
        print(f"User B Created Post {post_id}")
    else:
        print("User B Failed to Create Post")
        return

    # 2. User A Likes User B's Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    response = client.post(f'/api/posts/{post_id}/like/')
    print(f"User A Likes Post: {response.status_code} - {response.data.get('message')}")

    # 3. User A Likes again (Should Fail/Warn)
    response = client.post(f'/api/posts/{post_id}/like/')
    print(f"User A Likes again: {response.status_code} - {response.data.get('message')}")

    # 4. User B Checks Notifications
    client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
    response = client.get('/api/notifications/')
    print(f"User B Notifications Status: {response.status_code}")
    notifs = response.data.get('results', []) if 'results' in response.data else response.data
    
    found_like_notif = False
    for n in notifs:
        print(f" - Notification: {n}")
        # Note: String representation might vary, checking if relates to like
        if 'liked your post' in str(n) or (n.get('verb') == 'liked your post'):
            found_like_notif = True
    
    print(f"User B received like notification: {found_like_notif}")

    # 5. User A Unlikes Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    response = client.post(f'/api/posts/{post_id}/unlike/')
    print(f"User A Unlikes Post: {response.status_code} - {response.data.get('message')}")

    # 6. User A Unlikes again (Should Fail)
    response = client.post(f'/api/posts/{post_id}/unlike/')
    print(f"User A Unlikes again: {response.status_code} - {response.data.get('message')}")


if __name__ == '__main__':
    run_verification()
