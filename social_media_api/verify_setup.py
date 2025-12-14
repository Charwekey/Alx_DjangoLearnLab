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
    
    # Create or Get User 1
    response = client.post('/accounts/register/', user1_data)
    if response.status_code == 201:
        token1 = response.data['token']
        print("User A Registered")
    else:
        # Login if exists
        response = client.post('/accounts/login/', user1_data)
        token1 = response.data['token']
        print("User A Logged In")

    # Create or Get User 2
    response = client.post('/accounts/register/', user2_data)
    if response.status_code == 201:
        token2 = response.data['token']
        print("User B Registered")
    else:
        response = client.post('/accounts/login/', user2_data)
        token2 = response.data['token']
        print("User B Logged In")

    print("\n--- Testing Posts ---")
    # User A Creates Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    post_data = {'title': 'User A First Post', 'content': 'This is the content of the post.'}
    response = client.post('/api/posts/', post_data)
    print(f"Create Post (User A): {response.status_code}")
    if response.status_code == 201:
        post_id = response.data['id']
    else:
        print(f"Failed to create post: {response.data}")
        return

    # User B Reads Post
    client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
    response = client.get(f'/api/posts/{post_id}/')
    print(f"Read Post (User B): {response.status_code}")
    
    # User B Comments on Post
    comment_data = {'post': post_id, 'content': 'Nice post!'}
    response = client.post('/api/comments/', comment_data)
    print(f"Create Comment (User B): {response.status_code}")
    if response.status_code == 201:
        comment_id = response.data['id']
    
    # User B tries to Edit Post A (Should Fail)
    edit_data = {'title': 'Hacked Post', 'content': 'Changed content'}
    response = client.put(f'/api/posts/{post_id}/', edit_data)
    print(f"Edit Post A by User B (Should be 403): {response.status_code}")

    # User A Edits own Post (Should Succeed)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token1)
    response = client.put(f'/api/posts/{post_id}/', edit_data)
    print(f"Edit Post A by User A (Should be 200): {response.status_code}")
    
    # Filtering Test
    print("\n--- Testing Search/Filtering ---")
    response = client.get('/api/posts/?search=Hacked')
    print(f"Search Results Count: {len(response.data.get('results', []))}")
    
    # Pagination Test
    print("\n--- Testing Pagination ---")
    # Create 11 more posts
    for i in range(11):
        client.post('/api/posts/', {'title': f'Post {i}', 'content': 'Content'})
    
    response = client.get('/api/posts/')
    print(f"Pagination 'count': {response.data.get('count')}")
    print(f"Pagination 'next': {response.data.get('next')}")

if __name__ == '__main__':
    run_verification()
