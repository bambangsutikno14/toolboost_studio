import os
import time
from flask import jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

STARTED_AT = time.time()

def init_scale(app):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    @app.after_request
    def add_security_headers(response):
        if os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true":
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
            response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
            response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        if request.path.startswith("/static/"):
            cache_seconds = os.getenv("STATIC_CACHE_SECONDS", "86400")
            response.headers.setdefault("Cache-Control", f"public, max-age={cache_seconds}")
        return response

    @app.get("/healthz")
    def healthz():
        return jsonify({
            "ok": True,
            "app": os.getenv("SITE_NAME", "ToolBoost SaaS"),
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "environment": os.getenv("ENVIRONMENT", "local"),
            "uptime_seconds": int(time.time() - STARTED_AT),
        })

    @app.get("/version")
    def version():
        return jsonify({
            "app": os.getenv("SITE_NAME", "ToolBoost SaaS"),
            "version": os.getenv("APP_VERSION", "1.0.0"),
        })
