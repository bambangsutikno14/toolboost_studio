#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    ".env", "requirements.txt", "requirements-prod.txt", "app/app.py", "app/scale.py",
    "app/templates/base.html", "run.bat", "generate_content.bat", "wsgi.py", "deploy/README_DEPLOY.md",
]
ok = True
for rel in required:
    path = ROOT / rel
    if path.exists():
        print("[OK]", rel)
    else:
        print("[MISSING]", rel)
        ok = False

env = (ROOT / ".env").read_text(encoding="utf-8", errors="ignore") if (ROOT / ".env").exists() else ""
for key in ["SITE_NAME", "SITE_DOMAIN", "ADSENSE_ENABLED", "APP_VERSION", "ENVIRONMENT"]:
    if key + "=" in env:
        print("[ENV OK]", key)
    else:
        print("[ENV MISSING]", key)
        ok = False

if not ok:
    sys.exit(1)
print("Pre-deploy check passed.")
