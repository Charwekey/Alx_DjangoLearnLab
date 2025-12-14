# Social Media API

A Django-based Social Media API with user authentication and custom user models.

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Alx_DjangoLearnLab/social_media_api.git
    cd social_media_api
    ```

2.  **Install Dependencies:**
    ```bash
    pip install django djangorestframework
    ```

3.  **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Run Development Server:**
    ```bash
    python manage.py runserver
    ```

## Authentication & User Model

The API uses Django REST Framework's Token Authentication.

### User Model
The `CustomUser` model extends `AbstractUser` and includes:
-   `bio`: User biography (TextField)
-   `profile_picture`: Image upload (ImageField)
-   `followers`: Many-to-Many relationship with `self`

### Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/accounts/register/` | Register a new user. Returns user data & token. | No |
| `POST` | `/api/accounts/login/` | Login with username/password. Returns user data & token. | No |
| `GET/PUT` | `/api/accounts/profile/` | Retrieve or update current user profile. | Yes (Token) |

### Testing
To run the automated tests:
```bash
python manage.py test accounts
```
