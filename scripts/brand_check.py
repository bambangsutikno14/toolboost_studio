import urllib.request
import sys

BASE = "http://127.0.0.1:8000"
PATHS = [
    "/", "/about", "/examples", "/privacy", "/terms", "/contact",
    "/tools/title-generator", "/tools/meta-description", "/tools/keyword-density-checker",
    "/sitemap.xml", "/robots.txt", "/healthz",
]
ok = 0
for path in PATHS:
    url = BASE + path
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            status = r.status
            print(f"[{status}] {url}")
            if status == 200:
                ok += 1
    except Exception as e:
        print(f"[ERR] {url} -> {e}")

print(f"OK: {ok}/{len(PATHS)}")
if ok != len(PATHS):
    sys.exit(1)
