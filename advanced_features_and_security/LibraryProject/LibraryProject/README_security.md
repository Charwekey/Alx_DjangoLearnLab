# Django Security Best Practices Implemented

This document describes the security measures implemented in the Django project.

## 1. Secure Settings
- `DEBUG = False` : prevents leaking sensitive data.
- `SECURE_BROWSER_XSS_FILTER = True` : protects against reflected XSS.
- `X_FRAME_OPTIONS = "DENY"` : prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` : stops MIME sniffing attacks.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` : cookies only sent via HTTPS.

## 2. CSRF Protection
All forms use `{% csrf_token %}` to protect against CSRF attacks.

## 3. Safe Views
- Django ORM used instead of raw SQL.
- All user input validated with Django forms.
- No unsafe string interpolation in queries.

## 4. Content Security Policy
A custom middleware adds a CSP header:
