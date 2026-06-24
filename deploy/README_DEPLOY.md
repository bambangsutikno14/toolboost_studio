# ADSENSE_SAAS_AUTO Deployment

Recommended stack:
- Ubuntu VPS
- Python 3.10+
- Gunicorn or uWSGI
- Nginx reverse proxy
- HTTPS via Certbot or Cloudflare
- Cloudflare DNS/CDN optional

Basic Linux example:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-prod.txt
gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app
```

Then put Nginx in front of it and point your domain to the server.

Must edit before public launch:
- `.env` SITE_DOMAIN
- `.env` SITE_NAME
- Privacy Policy
- Terms of Service
- Contact email
- Real brand/about content
- Original examples and screenshots

Health check:

```text
https://yourdomain.com/healthz
```
