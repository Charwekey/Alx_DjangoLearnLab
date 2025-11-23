Deploying LibraryProject with HTTPS

This document describes how to deploy the project behind HTTPS and recommended server configuration.

1. Obtain SSL/TLS certificates

- Use Let's Encrypt (certbot) or your CA to obtain certificates for your domain(s).

2. Example Nginx configuration (reverse proxy terminating SSL)

server {
listen 80;
server_name example.com www.example.com;
return 301 https://$host$request_uri;
}

server {
listen 443 ssl http2;
server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location /static/ {
        alias /path/to/project/static/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}

3. Django settings to enable in production

- Set `DEBUG = False`.
- Set `ALLOWED_HOSTS = ['yourdomain.com']`.
- In `settings.py` enable (or set via environment variables):
  - `SECURE_SSL_REDIRECT = True`
  - `SECURE_HSTS_SECONDS = 31536000`
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
  - `SECURE_HSTS_PRELOAD = True` (only if you intend to preload)
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
  - If behind a proxy: `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`

### Environment variable examples

You can control the HTTPS/HSTS settings using environment variables so you don't
need to edit `settings.py` directly. Example variables used by this project:

- `DJANGO_SECURE_SSL_REDIRECT` (1|true to enable)
- `DJANGO_SECURE_HSTS_SECONDS` (integer seconds)
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` (1|true to enable)
- `DJANGO_SECURE_HSTS_PRELOAD` (1|true to enable)
- `DJANGO_SESSION_COOKIE_SECURE` (1|true)
- `DJANGO_CSRF_COOKIE_SECURE` (1|true)
- `DJANGO_SECURE_PROXY_SSL_HEADER` (header name, e.g. `HTTP_X_FORWARDED_PROTO`)

Windows (cmd.exe) — set for the current session:

```
set DJANGO_SECURE_SSL_REDIRECT=1
set DJANGO_SECURE_HSTS_SECONDS=31536000
set DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=1
set DJANGO_SECURE_HSTS_PRELOAD=1
```

PowerShell (current session):

```
$env:DJANGO_SECURE_SSL_REDIRECT='1'
$env:DJANGO_SECURE_HSTS_SECONDS='31536000'
$env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='1'
$env:DJANGO_SECURE_HSTS_PRELOAD='1'
```

Linux/macOS (bash):

```
export DJANGO_SECURE_SSL_REDIRECT=1
export DJANGO_SECURE_HSTS_SECONDS=31536000
export DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=1
export DJANGO_SECURE_HSTS_PRELOAD=1
```

After setting env vars, restart your WSGI/ASGI server so Django picks them up.

4. Security review notes

- HSTS is powerful — be careful enabling it for domains you don't fully control.
- Ensure you serve all resources over HTTPS (update any absolute http:// links).
- Test using SSL Labs (https://www.ssllabs.com/ssltest/) after deployment.

5. Testing locally with HTTPS (optional)

- For local testing, you can run a local reverse proxy with self-signed certs, but browsers will warn.
- Do not enable HSTS for local domains.

6. Rollout checklist

- Configure server certs and Nginx/Apache correctly.
- Update `settings.py` production variables from secure environment variables.
- Test redirects and headers.
- Monitor logs and SSL expiry dates.
