# Social Media API Deployment Guide

This guide details how to deploy the Social Media API to a production environment (e.g., Heroku, Render).

## Prerequisites
- A GitHub repository with your code pushed.
- A Heroku/Render account.
- `requirements.txt` and `Procfile` (already created).

## 1. Environment Variables
Set the following environment variables in your hosting provider's dashboard:

| Variable | Value (Example) | Description |
| :--- | :--- | :--- |
| `DEBUG` | `False` | Disables debug mode. |
| `SECRET_KEY` | `your-long-random-secret-key` | Production secret key. |
| `ALLOWED_HOSTS` | `social-media-api.herokuapp.com` | Comma-separated list of domains. |
| `DATABASE_URL` | `postgres://user:pass@host:5432/db` | Database connection string. |

## 2. Dependencies
The project uses:
- `gunicorn`: Production WSGI server (configured in `Procfile`).
- `whitenoise`: Serving static files.
- `dj-database-url`: Parsing database URLs.
- `psycopg2-binary`: PostgreSQL adapter.

## 3. Deployment Steps (Heroku Example)
1.  **Create App**: `heroku create social-media-api-demo`
2.  **Add Database**: `heroku addons:create heroku-postgresql:hobby-dev`
3.  **Config Vars**:
    ```bash
    heroku config:set DEBUG=False
    heroku config:set SECRET_KEY='...'
    heroku config:set ALLOWED_HOSTS='social-media-api-demo.herokuapp.com'
    ```
4.  **Deploy**:
    ```bash
    git push heroku main
    ```
5.  **Migrate**:
    ```bash
    heroku run python manage.py migrate
    ```

## 4. Static Files
Configurations are set to use `WhiteNoise` to serve static files from `staticfiles/` which are gathered during the build process via `python manage.py collectstatic`.
