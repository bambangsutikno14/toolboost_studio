import urllib.request
import sys

BASE = "http://127.0.0.1:8000"
PATHS = [
    "/en/", "/id/", "/es/", "/pt/", "/fr/", "/de/", "/hi/", "/ar/",
    "/en/tools/title-generator", "/id/tools/title-generator", "/es/tools/title-generator",
    "/pt/tools/meta-description", "/fr/tools/hashtag-generator", "/de/tools/keyword-density-checker",
    "/hi/tools/slug-generator", "/ar/tools/content-brief-generator",
    "/sitemap.xml", "/robots.txt", "/healthz",
]
ok = 0
for p in PATHS:
    try:
        with urllib.request.urlopen(BASE + p, timeout=5) as r:
            print(f"[{r.status}] {BASE+p}")
            if r.status == 200:
                ok += 1
    except Exception as e:
        print(f"[ERR] {BASE+p} -> {e}")
print(f"OK: {ok}/{len(PATHS)}")
if ok != len(PATHS):
    sys.exit(1)
