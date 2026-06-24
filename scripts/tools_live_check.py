import sys
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE = "http://127.0.0.1:8000"

TESTS = [
    ("/tools/title-generator", {"keyword": "asmr rain"}, ["Title Ideas", "ASMR Rain"]),
    ("/tools/meta-description", {"keyword": "utm builder"}, ["Meta Description", "UTM Builder"]),
    ("/tools/hashtag-generator", {"text": "asmr rain"}, ["#asmr", "#rain", "#asmrrain"]),
    ("/tools/word-counter", {"text": "hello world this is a test"}, ["Word Count Result", "words"]),
    ("/tools/utm-builder", {"url": "https://example.com", "source": "google", "medium": "organic", "campaign": "test"}, ["utm_source=google", "utm_campaign=test"]),
    ("/tools/keyword-density-checker", {"text": "seo seo tools for creators"}, ["Keyword Density", "seo"]),
    ("/tools/slug-generator", {"text": "Best Free SEO Tools!"}, ["best-free-seo-tools"]),
    ("/tools/content-brief-generator", {"topic": "youtube title generator", "audience": "creators"}, ["Content Brief", "Outline"]),
    ("/tools/youtube-description-generator", {"topic": "asmr rain", "keywords": "sleep relaxing"}, ["YouTube Description", "Key points"]),
    ("/tools/faq-generator", {"topic": "UTM builder", "audience": "marketers"}, ["FAQ Ideas", "What is UTM builder"]),
    ("/tools/blog-outline-generator", {"topic": "keyword density checker", "intent": "informational"}, ["Blog Outline", "H1:"]),
    ("/tools/social-caption-generator", {"topic": "free SEO tools", "platform": "TikTok"}, ["Social Caption", "Hook"]),
    ("/tools/adsense-readiness-checklist", {"site_url": "https://example.com", "pages_count": "20", "has_privacy": "1", "has_terms": "1", "has_contact": "1", "has_original_content": "1"}, ["AdSense Readiness", "Score"]),
    ("/tools/faq-schema-generator", {"q1": "What is this?", "a1": "A test answer."}, ["FAQ Schema JSON-LD", "FAQPage"]),
    ("/tools/robots-generator", {"domain": "https://example.com"}, ["robots.txt", "Sitemap:"]),
    ("/tools/sitemap-url-builder", {"urls": "https://example.com/"}, ["sitemap.xml", "urlset"]),
]

ok = 0
for path, data, expected in TESTS:
    url = BASE + path
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=encoded, method="POST")
        with urllib.request.urlopen(req, timeout=8) as r:
            body = r.read().decode("utf-8", errors="ignore")
            status = r.status
        if status != 200:
            print(f"[FAIL] {url} status {status}")
            sys.exit(1)
        if "Internal Server Error" in body or "Traceback" in body:
            print(f"[FAIL] {url} returned server error text")
            sys.exit(1)
        missing = [x for x in expected if x not in body]
        if missing:
            print(f"[FAIL] {url} missing {missing}")
            sys.exit(1)
        print(f"[OK] {url}")
        ok += 1
    except Exception as e:
        print(f"[ERR] {url} -> {e}")
        print("Pastikan run.bat sedang hidup di CMD lain sebelum menjalankan tools_live_check.bat.")
        sys.exit(1)

print(f"TOOLS LIVE CHECK PASSED: {ok}/{len(TESTS)}")
