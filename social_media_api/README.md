# Social Media API

A Django-based Social Media API with user authentication and custom user models.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd social_media_api
    ```

2.  **Install dependencies:**
    ```bash
    pip install django djangorestframework Pillow
    ```

3.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

## User Model

The API uses a custom user model `CustomUser` which extends `AbstractUser`.
Additional fields:
- `bio`: Text field for user biography.
- `profile_picture`: Image field for user profile picture.
- `followers`: ManyToMany field referencing `self` (symmetrical=False).

## Authentication

 The API uses Token Authentication.

### Endpoints

-   **Register**: `POST /accounts/register/`
    -   Payload: `{"username": "user1", "password": "password123", "email": "user@example.com", "bio": "Hello"}`
    -   Response: `{"token": "...", "user": {...}}`

-   **Login**: `POST /accounts/login/`
    -   Payload: `{"username": "user1", "password": "password123"}`
    -   Response: `{"token": "...", "user_id": 1, "email": "..."}`

-   **Profile**: `GET /accounts/profile/`
    -   Headers: `Authorization: Token <your_token>`
    -   Response: User details.
