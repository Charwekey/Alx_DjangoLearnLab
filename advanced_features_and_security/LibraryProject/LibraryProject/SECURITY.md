Security Notes for LibraryProject

Summary of implemented security measures:

1. Secure settings (see `settings.py`):

- `DEBUG = False` for production.
- `SECURE_BROWSER_XSS_FILTER = True` to enable the browser XSS filter.
- `X_FRAME_OPTIONS = "DENY"` to prevent clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` to prevent MIME sniffing.
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` to ensure cookies are only sent over HTTPS.
- `AUTH_USER_MODEL = 'relationship_app.User'` is set to use the custom user model.
- `MEDIA_URL` and `MEDIA_ROOT` are configured for `ImageField` uploads.

2. CSRF protection:

- All form templates include `{% csrf_token %}` (added `book_form.html`, `book_confirm_delete.html`, and `list_books.html` already contains it).

3. Safe views and ORM usage:

- Views use Django ORM and `ModelForm`s (`BookForm`) to validate and sanitize input.
- Permission checks are enforced using `@permission_required` and `PermissionRequiredMixin`.

4. Content Security Policy (CSP):

- A minimal CSP header is applied by `LibraryProject.middleware.CSPMiddleware`:
  `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'`.
- For stricter policies or nonce-based scripts, consider using `django-csp`.

5. Groups and permissions:

- Custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) are defined on the `Book` model.
- A data migration (`relationship_app/migrations/0002_create_groups.py`) creates `Editors`, `Viewers`, and `Admins` groups and assigns permissions.

Testing steps:

- Run the server and use browser devtools to verify `Content-Security-Policy` header and that CSRF-protected POSTs succeed while missing-CSRF requests fail.
- Use admin to inspect groups and assign users for functional testing.

Notes and next steps:

- Keep `DEBUG=False` and configure `ALLOWED_HOSTS` for production.
- Ensure HTTPS termination is configured in production so secure cookies are enforced.
- Consider adding automated tests for permission enforcement and basic security headers.
