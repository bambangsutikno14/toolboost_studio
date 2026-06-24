import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, redirect
from dotenv import load_dotenv

try:
    from adsense import adsense_script, ad_block
    from scale import init_scale
    from brand_content import BRAND, get_tool_content, INTERNAL_LINKS
    from intl import LANGUAGES, DEFAULT_LANG, get_lang, supported_lang, localized_tool, global_hreflang
    from growth import (
        TOOLS, GUIDES, title_ideas, meta_description, hashtag_ideas, word_counter,
        build_utm, keyword_density, slugify, content_brief, youtube_description,
        faq_generator, blog_outline, social_caption, adsense_checklist, faq_schema,
        robots_txt, sitemap_xml
    )
except ImportError:
    from .adsense import adsense_script, ad_block
    from .scale import init_scale
    from .brand_content import BRAND, get_tool_content, INTERNAL_LINKS
    from .intl import LANGUAGES, DEFAULT_LANG, get_lang, supported_lang, localized_tool, global_hreflang
    from .growth import (
        TOOLS, GUIDES, title_ideas, meta_description, hashtag_ideas, word_counter,
        build_utm, keyword_density, slugify, content_brief, youtube_description,
        faq_generator, blog_outline, social_caption, adsense_checklist, faq_schema,
        robots_txt, sitemap_xml
    )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")
init_scale(app)

def site_domain():
    return os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000").rstrip("/")

def get_tool(slug):
    return next((t for t in TOOLS if t["slug"] == slug), None)

def run_tool(slug, form):
    if slug == "title-generator":
        return {"type": "list", "title": "Title Ideas", "items": title_ideas(form.get("keyword", ""))}
    if slug == "meta-description":
        return {"type": "text", "title": "Meta Description", "text": meta_description(form.get("keyword", ""))}
    if slug == "hashtag-generator":
        return {"type": "text", "title": "Hashtags", "text": " ".join(hashtag_ideas(form.get("text", "")))}
    if slug == "word-counter":
        return {"type": "dict", "title": "Word Count Result", "data": word_counter(form.get("text", ""))}
    if slug == "utm-builder":
        return {"type": "text", "title": "UTM URL", "text": build_utm(form.get("url"), form.get("source"), form.get("medium"), form.get("campaign"), form.get("term"), form.get("content"))}
    if slug == "keyword-density-checker":
        return {"type": "table", "title": "Keyword Density", "data": keyword_density(form.get("text", ""))}
    if slug == "slug-generator":
        return {"type": "text", "title": "URL Slug", "text": slugify(form.get("text", ""))}
    if slug == "content-brief-generator":
        return {"type": "brief", "title": "Content Brief", "data": content_brief(form.get("topic", ""), form.get("audience", ""))}
    if slug == "youtube-description-generator":
        return {"type": "youtube", "title": "YouTube Description", "data": youtube_description(form.get("topic", ""), form.get("keywords", ""))}
    if slug == "faq-generator":
        return {"type": "faq", "title": "FAQ Ideas", "data": faq_generator(form.get("topic", ""), form.get("audience", ""))}
    if slug == "blog-outline-generator":
        return {"type": "list", "title": "Blog Outline", "items": blog_outline(form.get("topic", ""), form.get("intent", ""))}
    if slug == "social-caption-generator":
        return {"type": "social", "title": "Social Caption", "data": social_caption(form.get("topic", ""), form.get("platform", ""))}
    if slug == "adsense-readiness-checklist":
        return {"type": "checklist", "title": "AdSense Readiness", "data": adsense_checklist(
            form.get("site_url", ""), form.get("pages_count", 0),
            bool(form.get("has_privacy")), bool(form.get("has_terms")),
            bool(form.get("has_contact")), bool(form.get("has_original_content"))
        )}
    if slug == "faq-schema-generator":
        pairs = []
        for i in range(1, 6):
            q = form.get(f"q{i}", "")
            a = form.get(f"a{i}", "")
            if q and a:
                pairs.append({"q": q, "a": a})
        return {"type": "code", "title": "FAQ Schema JSON-LD", "text": faq_schema(pairs)}
    if slug == "robots-generator":
        return {"type": "code", "title": "robots.txt", "text": robots_txt(form.get("domain", ""))}
    if slug == "sitemap-url-builder":
        urls = (form.get("urls", "") or "").splitlines()
        return {"type": "code", "title": "sitemap.xml", "text": sitemap_xml(urls)}
    return {"type": "text", "title": "Result", "text": "Tool is ready."}

@app.context_processor
def inject_globals():
    return {
        "site_name": os.getenv("SITE_NAME", BRAND["name"]),
        "brand": BRAND,
        "internal_links": INTERNAL_LINKS,
        "site_domain": site_domain(),
        "contact_email": os.getenv("CONTACT_EMAIL", "your-active-email@example.com"),
        "adsense_script": adsense_script,
        "ad_block": ad_block,
        "year": datetime.now().year,
        "ga_id": os.getenv("GA_MEASUREMENT_ID", "").strip(),
        "gsc_code": os.getenv("GSC_VERIFICATION", "").strip(),
        "brand_niche": os.getenv("BRAND_NICHE", "creator, SEO, and marketing tools"),
        "languages": LANGUAGES,
        "page_lang": DEFAULT_LANG,
        "page_dir": "ltr",
        "hreflang_links": [],
    }

@app.get("/")
def home():
    return render_template(
        "home.html",
        tools=TOOLS,
        guides=GUIDES[:8],
        page_title=f"{BRAND['name']} - {BRAND['tagline']}",
        page_description=BRAND["positioning"],
        canonical=site_domain() + "/",
        page_lang=DEFAULT_LANG,
        page_dir="ltr",
        hreflang_links=global_hreflang(site_domain(), lambda code: f"/{code}/"),
    )

@app.get("/<lang>/")
def locale_home(lang):
    if not supported_lang(lang):
        return redirect("/")
    locale = get_lang(lang)
    localized_tools = [localized_tool(t, lang) for t in TOOLS]
    return render_template(
        "locale_home.html",
        locale=locale,
        tools=localized_tools,
        guides=GUIDES[:8],
        page_title=locale["title"],
        page_description=locale["description"],
        canonical=site_domain()+f"/{lang}/",
        page_lang=lang,
        page_dir=locale["dir"],
        hreflang_links=global_hreflang(site_domain(), lambda code: f"/{code}/"),
    )

@app.route("/tools/<slug>", methods=["GET", "POST"])
def tool_router(slug):
    return tool_page(DEFAULT_LANG, slug, canonical_prefix="")

@app.route("/<lang>/tools/<slug>", methods=["GET", "POST"])
def localized_tool_router(lang, slug):
    if not supported_lang(lang):
        return redirect(f"/tools/{slug}")
    return tool_page(lang, slug, canonical_prefix=f"/{lang}")

def tool_page(lang, slug, canonical_prefix=""):
    tool = get_tool(slug)
    if not tool:
        return Response("Tool not found", status=404)
    locale = get_lang(lang)
    tool = localized_tool(tool, lang)
    if "name_local" in tool:
        tool["name"] = tool["name_local"]
        tool["desc"] = tool["desc_local"]

    tool_content = get_tool_content(slug, tool["name"], tool.get("keyword", tool["name"].lower()))
    result = None
    form = request.form.to_dict() if request.method == "POST" else {}
    if request.method == "POST":
        result = run_tool(slug, form)

    return render_template(
        "tools/generic_tool.html",
        tool=tool,
        tool_content=tool_content,
        result=result,
        form=form,
        locale=locale,
        page_title=tool["name"],
        page_description=tool["desc"],
        canonical=site_domain()+canonical_prefix+"/tools/"+slug,
        page_lang=lang,
        page_dir=locale["dir"],
        hreflang_links=global_hreflang(site_domain(), lambda code: f"/{code}/tools/{slug}"),
    )

@app.get("/guides")
def guides_index():
    return render_template(
        "guides.html",
        guides=GUIDES,
        page_title="Guides and Workflows",
        page_description="Practical guides for using creator, SEO, and marketing tools.",
        canonical=site_domain() + "/guides",
        hreflang_links=global_hreflang(site_domain(), lambda code: f"/{code}/"),
    )

@app.get("/guides/<slug>")
def guide_detail(slug):
    guide = next((g for g in GUIDES if g["slug"] == slug), None)
    if not guide:
        return Response("Guide not found", status=404)
    return render_template(
        "guide.html",
        guide=guide,
        related_tools=TOOLS[:6],
        page_title=guide["title"],
        page_description=guide["description"],
        canonical=site_domain() + "/guides/" + guide["slug"],
    )

@app.get("/about")
def about():
    return render_template("about.html", tools=TOOLS[:8], page_title=f"About {BRAND['name']}", page_description=BRAND["positioning"], canonical=site_domain()+"/about")

@app.get("/examples")
def examples_page():
    return render_template("examples.html", tools=TOOLS, page_title="Tool Examples and Screenshots", page_description="Example workflows and screenshots for ToolBoost Studio tools.", canonical=site_domain()+"/examples")

@app.route("/admin/content-factory", methods=["GET", "POST"])
def content_factory():
    key = request.args.get("key") or request.form.get("key")
    admin_key = os.getenv("ADMIN_KEY", "local-secret-change-before-online")
    if key != admin_key:
        return Response("Unauthorized. Add ?key=YOUR_ADMIN_KEY", status=403)
    output = None
    if request.method == "POST":
        topic = request.form.get("topic", "online tool")
        audience = request.form.get("audience", "beginners")
        output = {"titles": title_ideas(topic), "meta": meta_description(topic), "brief": content_brief(topic, audience), "faq": faq_generator(topic, audience), "outline": blog_outline(topic), "hashtags": hashtag_ideas(topic)}
    return render_template("content_factory.html", output=output, key=key, page_title="Content Factory", page_description="Local content generator for tool pages and guides.", canonical=site_domain()+"/admin/content-factory")

@app.get("/privacy")
def privacy():
    return render_template("privacy.html", page_title="Privacy Policy", page_description=f"Privacy policy for {BRAND['name']}.", canonical=site_domain()+"/privacy")

@app.get("/terms")
def terms():
    return render_template("terms.html", page_title="Terms of Service", page_description=f"Terms of service for {BRAND['name']}.", canonical=site_domain()+"/terms")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    sent = False
    if request.method == "POST":
        data_dir = os.path.join(BASE_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        payload = {"time": datetime.utcnow().isoformat() + "Z", "name": request.form.get("name", ""), "email": request.form.get("email", ""), "message": request.form.get("message", "")}
        with open(os.path.join(data_dir, "contact_messages.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sent = True
    return render_template("contact.html", sent=sent, page_title="Contact", page_description=f"Contact {BRAND['name']}.", canonical=site_domain()+"/contact")

@app.get("/robots.txt")
def robots():
    return Response(robots_txt(site_domain()), mimetype="text/plain")

@app.get("/sitemap.xml")
def sitemap():
    urls = [site_domain()+p for p in ["/", "/about", "/examples", "/guides", "/privacy", "/terms", "/contact"]]
    urls += [site_domain()+f"/{lang}/" for lang in LANGUAGES]
    urls += [site_domain()+"/tools/"+t["slug"] for t in TOOLS]
    for lang in LANGUAGES:
        urls += [site_domain()+f"/{lang}/tools/"+t["slug"] for t in TOOLS]
    urls += [site_domain()+"/guides/"+g["slug"] for g in GUIDES]
    return Response(sitemap_xml(urls), mimetype="application/xml")

@app.get("/ads.txt")
def ads_txt():
    pub_id = os.getenv("ADSENSE_PUB_ID", "ca-pub-XXXXXXXXXXXXXXXX")
    if "XXXX" in pub_id:
        body = "# Isi setelah punya Publisher ID AdSense.\n# google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n"
    else:
        body = f"google.com, {pub_id.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    return Response(body, mimetype="text/plain")

@app.get("/api/tools")
def api_tools():
    return jsonify({"tools": TOOLS})

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "app": os.getenv("SITE_NAME", BRAND["name"]), "tools": len(TOOLS), "guides": len(GUIDES), "languages": list(LANGUAGES.keys())})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
