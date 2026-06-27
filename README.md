# ToolBoost Studio / ADSENSE_SAAS_AUTO

A Flask-based global SaaS tools website for creators, SEO writers, marketers, and small businesses.

## Local run

```bat
cd /d E:\ads\ADSENSE_SAAS_AUTO
run.bat
```

Open:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/en/
http://127.0.0.1:8000/sitemap.xml
```

## Audit

```bat
brand_check.bat
global_check.bat
pre_deploy_check.bat
```

## Important

Do not commit `.env` to GitHub. Use `.env.example` as template.

## Global SEO

Language URLs:

- `/en/`
- `/id/`
- `/es/`
- `/pt/`
- `/fr/`
- `/de/`
- `/hi/`
- `/ar/`

Tool URLs:

```text
/en/tools/title-generator
/id/tools/title-generator
/es/tools/title-generator
```

## Production

Use `wsgi.py` with Gunicorn/Waitress behind a reverse proxy or a Python hosting provider.

## Tools quality check

```bat
tools_quality_check.bat
```

## Tool validation

Run unit validation:

```bat
tools_quality_check.bat
```

Run live validation while server is running:

```bat
tools_live_check.bat
```

### V6 audit note

`tools_live_check.bat` uses case-insensitive output checks so valid title casing such as `UTM Builder` does not fail because of lowercase expectation.
