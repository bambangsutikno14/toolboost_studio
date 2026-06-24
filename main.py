import os
import re
import json
from datetime import datetime
from urllib.parse import urlencode

from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)

STOPWORDS = {
    "the", "and", "or", "for", "with", "from", "your", "you", "are", "how",
    "to", "of", "a", "an", "in", "on", "is", "best", "free", "ini", "yang",
    "dan", "untuk", "dengan", "cara"
}

def site_name():
    return os.getenv("SITE_NAME", "ToolBoost SaaS")

def adsense_script():
    enabled = os.getenv("ADSENSE_ENABLED", "false").lower() == "true"
    pub_id = os.getenv("ADSENSE_PUB_ID", "").strip()
    if not enabled or not pub_id or "XXXX" in pub_id:
        return "<!-- AdSense belum aktif. Isi Publisher ID setelah akun disetujui. -->"
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub_id}" crossorigin="anonymous"></script>'

def ad_block(slot_name="default"):
    enabled = os.getenv("ADSENSE_ENABLED", "false").lower() == "true"
    pub_id = os.getenv("ADSENSE_PUB_ID", "").strip()
    if not enabled or "XXXX" in pub_id:
        return f'<div class="ad-placeholder">Area iklan: {slot_name}. Aktifkan setelah AdSense disetujui.</div>'
    return (
        '<ins class="adsbygoogle" style="display:block" '
        f'data-ad-client="{pub_id}" data-ad-slot="1234567890" '
        'data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    )

def clean_words(text):
    words = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]

def title_ideas(keyword):
    kw = (keyword or "online tool").strip()
    templates = [
        "Best {kw} Tool for Fast Results",
        "Free {kw} Generator Online",
        "How to Use {kw} in Minutes",
        "{kw}: Simple Tool for Creators and Marketers",
        "Improve Your Workflow With This {kw} Tool",
        "Top {kw} Tips for Beginners",
        "{kw} Checklist: Avoid Common Mistakes",
        "Fast {kw} Helper for Daily Work",
    ]
    return [t.format(kw=kw.title()) for t in templates]

def meta_description(keyword):
    kw = (keyword or "online tool").strip()
    return (
        f"Use this free {kw} tool to create faster workflows, improve content quality, "
        f"and save time with a simple browser-based SaaS utility."
    )[:155]

def hashtag_ideas(text):
    tags = []
    for w in clean_words(text)[:12]:
        tags.append("#" + re.sub(r"[^a-zA-Z0-9]", "", w.title()))
    for d in ["#SaaS", "#Productivity", "#Marketing", "#CreatorTools"]:
        if d not in tags:
            tags.append(d)
    return tags[:15]

def word_counter(text):
    words = re.findall(r"\b\w+\b", text or "")
    chars = len(text or "")
    sentences = len(re.findall(r"[.!?]+", text or "")) or 1
    return {
        "words": len(words),
        "characters": chars,
        "sentences_est": sentences,
        "reading_time_min": max(1, round(len(words) / 200)),
    }

def build_utm(url, source, medium, campaign, term="", content=""):
    params = {
        "utm_source": source or "google",
        "utm_medium": medium or "organic",
        "utm_campaign": campaign or "main_campaign",
    }
    if term:
        params["utm_term"] = term
    if content:
        params["utm_content"] = content
    base = url or "https://example.com"
    sep = "&" if "?" in base else "?"
    return base + sep + urlencode(params)

@app.context_processor
def inject_globals():
    return {
        "site_name": site_name(),
        "site_domain": os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000").rstrip("/"),
        "contact_email": os.getenv("CONTACT_EMAIL", "admin@example.com"),
        "adsense_script": adsense_script,
        "ad_block": ad_block,
        "year": datetime.now().year,
    }

@app.get("/")
def home():
    tools = [
        {"name": "SEO Title Generator", "url": "/tools/title-generator", "desc": "Buat ide judul SEO untuk artikel, landing page, atau video."},
        {"name": "Meta Description Generator", "url": "/tools/meta-description", "desc": "Buat meta description pendek untuk halaman web."},
        {"name": "Hashtag Generator", "url": "/tools/hashtag-generator", "desc": "Buat hashtag dari topik atau caption."},
        {"name": "Word Counter", "url": "/tools/word-counter", "desc": "Hitung kata, karakter, dan estimasi waktu baca."},
        {"name": "UTM Builder", "url": "/tools/utm-builder", "desc": "Buat URL campaign tracking untuk marketing."},
    ]
    return render_template("home.html", tools=tools)

@app.route("/tools/title-generator", methods=["GET", "POST"])
def title_generator():
    result = []
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        result = title_ideas(keyword)
    return render_template("tools/title_generator.html", result=result, keyword=keyword)

@app.route("/tools/meta-description", methods=["GET", "POST"])
def meta_generator():
    result = ""
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        result = meta_description(keyword)
    return render_template("tools/meta_generator.html", result=result, keyword=keyword)

@app.route("/tools/hashtag-generator", methods=["GET", "POST"])
def hashtag_generator():
    result = []
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        result = hashtag_ideas(text)
    return render_template("tools/hashtag_generator.html", result=result, text=text)

@app.route("/tools/word-counter", methods=["GET", "POST"])
def word_counter_view():
    result = None
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        result = word_counter(text)
    return render_template("tools/word_counter.html", result=result, text=text)

@app.route("/tools/utm-builder", methods=["GET", "POST"])
def utm_builder():
    result = ""
    form = {}
    if request.method == "POST":
        form = request.form.to_dict()
        result = build_utm(
            form.get("url"),
            form.get("source"),
            form.get("medium"),
            form.get("campaign"),
            form.get("term"),
            form.get("content"),
        )
    return render_template("tools/utm_builder.html", result=result, form=form)

@app.get("/privacy")
def privacy():
    return render_template("privacy.html")

@app.get("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    sent = False
    if request.method == "POST":
        payload = {
            "time": datetime.utcnow().isoformat() + "Z",
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "message": request.form.get("message", ""),
        }
        data_path = os.path.join(BASE_DIR, "data", "contact_messages.jsonl")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sent = True
    return render_template("contact.html", sent=sent)

@app.get("/robots.txt")
def robots_txt():
    domain = os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000").rstrip("/")
    return Response(f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n", mimetype="text/plain")

@app.get("/sitemap.xml")
def sitemap_xml():
    domain = os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000").rstrip("/")
    urls = ["/", "/tools/title-generator", "/tools/meta-description", "/tools/hashtag-generator", "/tools/word-counter", "/tools/utm-builder", "/privacy", "/terms", "/contact"]
    items = "\n".join(f"<url><loc>{domain}{u}</loc><lastmod>{datetime.utcnow().date()}</lastmod></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>'
    return Response(xml, mimetype="application/xml")

@app.get("/ads.txt")
def ads_txt():
    pub_id = os.getenv("ADSENSE_PUB_ID", "ca-pub-XXXXXXXXXXXXXXXX")
    if "XXXX" in pub_id:
        body = "# Isi setelah punya Publisher ID AdSense.\n# google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n"
    else:
        body = f"google.com, {pub_id.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    return Response(body, mimetype="text/plain")

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "app": site_name()})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
