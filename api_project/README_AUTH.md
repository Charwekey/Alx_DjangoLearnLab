Authentication & Permissions (Django REST Framework)

This project uses token authentication and `IsAuthenticated` permission by default.

How to obtain a token

- POST username/password to the token endpoint:

  POST /api-token-auth/
  Content-Type: application/json
  Body: { "username": "apiuser", "password": "password123" }

  Response: { "token": "<your-token>" }

(You can also obtain a token by creating a user and running `scripts/create_api_user.py`.)

How to call protected endpoints

Include the token in the `Authorization` header:

  Authorization: Token <your-token>

Example curl (replace <token> with actual token):

  curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/books/

Notes

- Default permission is `IsAuthenticated`, set in `api_project/settings.py`.
- Token endpoint is available at `/api-token-auth/`.
- If you prefer session or JWT authentication, update `REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']` accordingly.
