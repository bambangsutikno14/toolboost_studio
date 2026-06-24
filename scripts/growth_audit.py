import urllib.request
import sys

BASE = "http://127.0.0.1:8000"
PATHS = [
    "/", "/guides", "/robots.txt", "/sitemap.xml", "/ads.txt", "/healthz",
    "/tools/title-generator", "/tools/meta-description", "/tools/hashtag-generator",
    "/tools/word-counter", "/tools/utm-builder", "/tools/keyword-density-checker",
    "/tools/slug-generator", "/tools/content-brief-generator",
    "/tools/youtube-description-generator", "/tools/faq-generator",
    "/tools/blog-outline-generator", "/tools/social-caption-generator",
    "/tools/adsense-readiness-checklist", "/tools/faq-schema-generator",
    "/tools/robots-generator", "/tools/sitemap-url-builder",
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
print(f"\nOK: {ok}/{len(PATHS)}")
if ok != len(PATHS):
    sys.exit(1)
