import re
import json
from collections import Counter
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

STOPWORDS = {
    "a","an","and","are","as","at","be","by","for","from","has","he","in","is","it","its",
    "of","on","or","that","the","to","was","were","will","with","this","your","you","we",
    "our","their","they","them","i","me","my","us","how","what","why","when","where",
    "cara","dan","di","ke","dari","untuk","yang","ini","itu","dengan","atau","pada",
    "el","la","los","las","un","una","de","del","para","por","com","que","y"
}

ACRONYMS = {
    "seo": "SEO", "utm": "UTM", "faq": "FAQ", "ai": "AI", "asmr": "ASMR",
    "api": "API", "pdf": "PDF", "csv": "CSV", "json": "JSON", "url": "URL",
    "ctr": "CTR", "cpc": "CPC", "roi": "ROI", "saas": "SaaS",
    "youtube": "YouTube", "tiktok": "TikTok", "instagram": "Instagram",
}

HASHTAG_CLUSTERS = {
    "asmr": ["asmr", "asmrvideo", "asmrsounds", "sleepasmr", "relaxingasmr"],
    "rain": ["rain", "rainsounds", "rainsound", "rainforsleep", "relaxingrain", "whitenoise"],
    "sleep": ["sleep", "sleepsounds", "sleepmusic", "deepsleep", "bettersleep"],
    "relax": ["relax", "relaxing", "relaxingmusic", "calm", "calming"],
    "music": ["music", "relaxingmusic", "sleepmusic", "backgroundmusic"],
    "youtube": ["youtube", "youtubetips", "youtubeshorts", "creator"],
    "tiktok": ["tiktok", "tiktoktips", "shortvideo", "contentcreator"],
    "seo": ["seo", "seotips", "seotools", "contentseo", "digitalmarketing"],
    "keyword": ["keywords", "keywordresearch", "seowriting"],
    "title": ["titles", "titleideas", "headlineideas", "copywriting"],
    "meta": ["metadescription", "seotips", "searchsnippet"],
    "marketing": ["marketing", "digitalmarketing", "contentmarketing", "growthmarketing"],
    "business": ["business", "smallbusiness", "businesstools", "productivity"],
    "content": ["content", "contentcreator", "contentmarketing", "contentideas"],
    "writer": ["writing", "writers", "copywriting", "blogging"],
    "blog": ["blog", "blogging", "blogtips", "contentwriting"],
    "instagram": ["instagram", "instagramtips", "socialmedia"],
    "social": ["socialmedia", "socialmediatips", "contentcreator"],
}

TOOLS = [
    {"name":"SEO Title Generator","slug":"title-generator","keyword":"seo title generator","intent":"create click-worthy search titles","desc":"Generate clear title ideas with search intent, benefit, and length awareness."},
    {"name":"Meta Description Generator","slug":"meta-description","keyword":"meta description generator","intent":"write search snippets","desc":"Create concise meta descriptions for pages, tools, posts, and landing pages."},
    {"name":"Hashtag Generator","slug":"hashtag-generator","keyword":"hashtag generator","intent":"create relevant social tags","desc":"Generate topic-aware hashtags from captions, keywords, and content ideas."},
    {"name":"Word Counter","slug":"word-counter","keyword":"word counter","intent":"measure writing length","desc":"Count words, characters, sentences, paragraphs, and estimated reading time."},
    {"name":"UTM Builder","slug":"utm-builder","keyword":"utm builder","intent":"track campaign links","desc":"Build clean UTM campaign links for analytics and marketing reports."},
    {"name":"Keyword Density Checker","slug":"keyword-density-checker","keyword":"keyword density checker","intent":"detect overused terms","desc":"Check repeated terms and density to keep writing natural and useful."},
    {"name":"Slug Generator","slug":"slug-generator","keyword":"slug generator","intent":"create clean URLs","desc":"Turn titles into short, readable, SEO-friendly URL slugs."},
    {"name":"Content Brief Generator","slug":"content-brief-generator","keyword":"content brief generator","intent":"plan content structure","desc":"Create a practical content brief with title ideas, outline, FAQ, and internal link suggestions."},
    {"name":"YouTube Description Generator","slug":"youtube-description-generator","keyword":"youtube description generator","intent":"write video descriptions","desc":"Generate structured video descriptions with summary, key points, CTA, and hashtags."},
    {"name":"FAQ Generator","slug":"faq-generator","keyword":"faq generator","intent":"answer user questions","desc":"Generate useful FAQ questions and answers for tool pages, guides, and landing pages."},
    {"name":"Blog Outline Generator","slug":"blog-outline-generator","keyword":"blog outline generator","intent":"structure blog posts","desc":"Create H1/H2/H3 outlines that match user intent and content workflow."},
    {"name":"Social Caption Generator","slug":"social-caption-generator","keyword":"social caption generator","intent":"write captions","desc":"Generate hooks, captions, CTAs, and hashtags for social media posts."},
    {"name":"AdSense Readiness Checklist","slug":"adsense-readiness-checklist","keyword":"adsense readiness checklist","intent":"prepare website for monetization","desc":"Review content, trust pages, navigation, and policy readiness before applying."},
    {"name":"FAQ Schema JSON-LD Generator","slug":"faq-schema-generator","keyword":"faq schema generator","intent":"generate structured data","desc":"Create FAQPage JSON-LD markup from question-answer pairs."},
    {"name":"Robots.txt Generator","slug":"robots-generator","keyword":"robots txt generator","intent":"create crawler rules","desc":"Generate a simple robots.txt file with sitemap reference."},
    {"name":"Sitemap URL Builder","slug":"sitemap-url-builder","keyword":"sitemap url builder","intent":"build XML sitemap","desc":"Convert a list of URLs into a basic XML sitemap."},
]

GUIDES = [
    {"title":"How to Use Free SEO Tools Without Over-Optimizing","slug":"free-seo-tools-without-over-optimizing","keyword":"free seo tools","description":"A practical workflow for using SEO tools while keeping pages helpful for readers."},
    {"title":"YouTube Title Generator: Examples and Workflow","slug":"youtube-title-generator-workflow","keyword":"youtube title generator","description":"How to create clearer video titles for search, browse, and suggested traffic."},
    {"title":"Meta Description Examples for Tool Pages","slug":"meta-description-examples-tool-pages","keyword":"meta description examples","description":"Examples of concise meta descriptions for free tools and SaaS landing pages."},
    {"title":"Hashtag Generator Guide for Creators","slug":"hashtag-generator-guide","keyword":"hashtag generator","description":"How to choose hashtags that describe the content instead of stuffing trends."},
    {"title":"UTM Builder Guide for Small Campaigns","slug":"utm-builder-guide","keyword":"utm builder","description":"A clean naming workflow for social, newsletter, and creator campaigns."},
    {"title":"Keyword Density Checker: What to Fix","slug":"keyword-density-checker-guide","keyword":"keyword density checker","description":"Use density as a quality signal, not as a ranking formula."},
    {"title":"URL Slug Best Practices for SEO","slug":"url-slug-best-practices","keyword":"slug generator","description":"Create readable URLs and avoid changing slugs without redirects."},
    {"title":"AdSense Readiness Checklist for New Sites","slug":"adsense-readiness-checklist-guide","keyword":"adsense readiness checklist","description":"Trust pages, content quality, navigation, and traffic quality before applying."},
    {"title":"SaaS SEO Strategy for Free Tool Websites","slug":"saas-seo-free-tools-strategy","keyword":"saas seo strategy","description":"How to grow a tool website with useful tools, examples, and internal links."},
    {"title":"Word Counter for SEO Writing and Captions","slug":"word-counter-seo-writing","keyword":"word counter","description":"Use word count and reading time as editorial controls for better writing."},
]

def clean_words(text):
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]

def smart_title(text):
    parts = re.findall(r"[a-zA-Z0-9]+", (text or "").strip())
    out = []
    for p in parts:
        low = p.lower()
        out.append(ACRONYMS.get(low, low.capitalize()))
    return " ".join(out) or "Online Tool"

def smart_sentence(text):
    s = smart_title(text)
    return s if s != "Online Tool" else "your topic"

def add_unique(items, value):
    if value and value not in items:
        items.append(value)

def tagify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "", (value or "").strip().lower())
    if not value or len(value) < 2 or value.isdigit():
        return ""
    return "#" + value

def add_tag(tags, value):
    tag = tagify(value)
    if tag and tag not in tags:
        tags.append(tag)

def detect_intent_terms(keyword):
    terms = set(clean_words(keyword))
    if {"asmr", "rain"} & terms or "sleep" in terms:
        return "relaxation/sleep audience"
    if "seo" in terms or "keyword" in terms:
        return "search and content optimization"
    if "youtube" in terms or "video" in terms:
        return "video discovery"
    if "business" in terms or "marketing" in terms:
        return "business growth"
    return "general productivity"

def title_ideas(keyword):
    kw = smart_title(keyword or "online tool")
    intent = detect_intent_terms(keyword)
    templates = [
        "Best {kw} Tool for Fast Results",
        "Free {kw} Generator Online",
        "How to Use {kw} in Minutes",
        "{kw}: Simple Tool for Creators and Marketers",
        "Improve Your Workflow With This {kw} Tool",
        "Top {kw} Tips for Beginners",
        "{kw} Checklist: Avoid Common Mistakes",
        "Fast {kw} Helper for Daily Work",
        "{kw} Examples You Can Use Today",
        "Simple {kw} Tool for Small Teams",
        "Create Better {kw} Outputs Without Guesswork",
        "{kw} Guide for {intent}",
    ]
    result = []
    for t in templates:
        idea = t.format(kw=kw, intent=intent)[:68].rstrip(" -:")
        add_unique(result, idea)
    return result[:12]

def meta_description(keyword):
    kw = smart_title(keyword or "online tool")
    intent = detect_intent_terms(keyword)
    options = [
        f"Use this free {kw} tool to create faster workflows, improve content quality, and save time with a simple browser utility.",
        f"Generate practical {kw} ideas for {intent}. Start with a topic, review the draft, and edit it for your audience.",
        f"Try a free {kw} tool for creators, writers, and marketers who need quick, useful, and editable results.",
    ]
    best = min(options, key=lambda x: abs(len(x) - 145))
    return best[:155].rstrip(" ,.")

def hashtag_ideas(text, min_tags=5, max_tags=18):
    terms = clean_words(text or "")
    tags = []
    if terms:
        for w in terms[:10]:
            add_tag(tags, w)
        if len(terms) >= 2:
            add_tag(tags, "".join(terms[:2]))
        if len(terms) >= 3:
            add_tag(tags, "".join(terms[:3]))
        for i in range(min(len(terms) - 1, 5)):
            add_tag(tags, terms[i] + terms[i + 1])
        for w in terms:
            for item in HASHTAG_CLUSTERS.get(w, []):
                add_tag(tags, item)
        termset = set(terms)
        if {"asmr", "rain"}.issubset(termset):
            for item in ["asmrrain","rainasmr","rainsounds","rainsound","rainforsleep","sleepasmr","relaxingrain","whitenoise","deepsleep","calmingvideo","relaxingsounds","sleepaid"]:
                add_tag(tags, item)
        if {"rain", "sleep"}.issubset(termset):
            for item in ["rainsleep", "sleepmusic", "sleepsounds", "bettersleep", "relaxingrain"]:
                add_tag(tags, item)
        if "seo" in termset or "keyword" in termset:
            for item in ["seo", "seotips", "seotools", "keywordresearch", "contentseo", "digitalmarketing"]:
                add_tag(tags, item)
        if "youtube" in termset or "shorts" in termset:
            for item in ["youtube", "youtubeshorts", "creator", "videomarketing", "contentcreator"]:
                add_tag(tags, item)
        if "tiktok" in termset:
            for item in ["tiktok", "tiktoktips", "shortvideo", "contentcreator"]:
                add_tag(tags, item)
        if "instagram" in termset:
            for item in ["instagram", "instagramtips", "socialmedia", "contentcreator"]:
                add_tag(tags, item)

    fallback_pool = ["contentideas", "creator", "creatorcommunity", "digitalcreator", "marketingtools", "productivity", "onlinetools", "contentcreator", "socialmedia", "growth"]
    if any(t in set(terms) for t in ["asmr", "rain", "sleep", "relax"]):
        fallback_pool = ["relaxing","calming","sleepsounds","relaxingsounds","deepsleep","whitenoise","meditation","sleepaid","relaxingvideo","asmrvideo"] + fallback_pool
    for item in fallback_pool:
        if len(tags) >= min_tags:
            break
        add_tag(tags, item)
    return tags[:max_tags]

def word_counter(text):
    text = text or ""
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    paragraphs = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    return {
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s+", "", text)),
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "reading_time_minutes": max(1, round(len(words) / 200)) if words else 0,
        "speaking_time_minutes": max(1, round(len(words) / 130)) if words else 0,
    }

def build_utm(url, source, medium, campaign, term="", content=""):
    url = (url or "").strip()
    if not url:
        return "Please enter a URL."
    if not re.match(r"^https?://", url, flags=re.I):
        url = "https://" + url
    parsed = urlparse(url)
    existing = dict(parse_qsl(parsed.query, keep_blank_values=True))
    params = {
        "utm_source": (source or "").strip().lower().replace(" ", "_"),
        "utm_medium": (medium or "").strip().lower().replace(" ", "_"),
        "utm_campaign": (campaign or "").strip().lower().replace(" ", "_"),
        "utm_term": (term or "").strip().lower().replace(" ", "_"),
        "utm_content": (content or "").strip().lower().replace(" ", "_"),
    }
    for k, v in params.items():
        if v:
            existing[k] = v
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", parsed.params, urlencode(existing), parsed.fragment))

def keyword_density(text):
    words = clean_words(text)
    total = len(words)
    counts = Counter(words)
    rows = []
    for word, count in counts.most_common(20):
        density = round((count / total) * 100, 2) if total else 0
        status = "natural"
        if density >= 8:
            status = "review repetition"
        elif density >= 4:
            status = "watch"
        rows.append({"word": word, "count": count, "density": density, "status": status})
    return {"total_words": total, "unique_words": len(counts), "rows": rows}

def slugify(text):
    s = (text or "").lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-")[:80] or "untitled"

def content_brief(topic, audience=""):
    topic_title = smart_title(topic or "online tool")
    audience = (audience or "beginners").strip()
    intent = detect_intent_terms(topic)
    return {
        "topic": topic_title,
        "audience": audience,
        "search_intent": intent,
        "titles": title_ideas(topic_title)[:6],
        "meta": meta_description(topic_title),
        "outline": [
            f"H1: {topic_title}",
            f"H2: What {topic_title} helps users do",
            "H2: Who should use this tool",
            "H2: Step-by-step workflow",
            "H2: Input-output examples",
            "H2: Common mistakes to avoid",
            "H2: FAQ",
            "H2: Related tools and next steps",
        ],
        "faqs": [
            f"What is {topic_title}?",
            f"Who should use {topic_title}?",
            f"Can I use the output directly?",
            f"How do I improve the result?",
            f"What should I check before publishing?",
        ],
        "internal_links": ["/tools/title-generator","/tools/meta-description","/tools/keyword-density-checker","/guides"],
        "quality_notes": [
            "Add original examples, not copied competitor text.",
            "Explain when users should manually edit the output.",
            "Link to related tools only when the next step is useful.",
        ],
    }

def youtube_description(topic, keywords=""):
    topic_title = smart_title(topic or "video topic")
    tags = hashtag_ideas(f"{topic} {keywords}")[:10]
    keyword_line = ", ".join(clean_words(keywords)[:8])
    description = (
        f"{topic_title}\n\n"
        f"Use this video as a simple guide or relaxing resource for {smart_sentence(topic).lower()}.\n\n"
        "Key points:\n"
        "- Clear topic and context\n"
        "- Useful information or experience for viewers\n"
        "- Easy next step after watching\n\n"
        f"Keywords: {keyword_line or smart_sentence(topic).lower()}\n\n"
        "If this helped, save the video and share it with someone who may need it."
    )
    return {"description": description, "hashtags": tags}

def faq_generator(topic, audience=""):
    topic_title = smart_title(topic or "this tool")
    audience = (audience or "users").strip()
    return [
        {"q": f"What is {topic_title}?", "a": f"{topic_title} is a practical tool or workflow that helps {audience} complete a specific task faster."},
        {"q": f"Who should use {topic_title}?", "a": f"It is useful for creators, writers, marketers, founders, students, and small teams that need quick editable drafts."},
        {"q": "Can I publish the output directly?", "a": "Use the output as a draft. Review it for accuracy, tone, originality, and context before publishing."},
        {"q": "How do I get better results?", "a": "Use specific inputs, include the audience or use case, and compare several output options before choosing one."},
        {"q": "Is this tool free?", "a": "The starter version is free to use. Future versions may add premium features for advanced workflows."},
    ]

def blog_outline(topic, intent=""):
    topic_title = smart_title(topic or "online tool")
    intent = intent or detect_intent_terms(topic)
    return [
        f"H1: {topic_title}",
        f"H2: What problem does {topic_title} solve?",
        f"H2: Who needs {topic_title}?",
        "H2: Step-by-step workflow",
        "H3: Prepare a specific input",
        "H3: Generate multiple options",
        "H3: Review quality and accuracy",
        "H2: Examples",
        "H2: Common mistakes",
        "H2: FAQ",
        "H2: Related tools",
        f"Search intent: {intent}",
    ]

def social_caption(topic, platform=""):
    topic_title = smart_title(topic or "this idea")
    platform = (platform or "social media").strip()
    tags = hashtag_ideas(topic_title)[:10]
    return {
        "hook": f"Need a faster way to handle {topic_title.lower()}?",
        "caption": f"Try this simple workflow for {topic_title}. Start with a clear input, generate a draft, then edit it so it fits your audience and platform.",
        "cta": f"Save this for your next {platform} post.",
        "hashtags": tags,
    }

def adsense_checklist(site_url, pages_count, has_privacy, has_terms, has_contact, has_original_content):
    try:
        pages_count = int(pages_count)
    except Exception:
        pages_count = 0
    checks = [
        {"item": "Website is publicly accessible", "ok": bool(site_url and site_url.startswith("http"))},
        {"item": "At least 15 useful pages/tools/guides", "ok": pages_count >= 15},
        {"item": "Privacy Policy page exists", "ok": bool(has_privacy)},
        {"item": "Terms page exists", "ok": bool(has_terms)},
        {"item": "Contact page exists", "ok": bool(has_contact)},
        {"item": "Original helpful content exists", "ok": bool(has_original_content)},
        {"item": "No invalid traffic, click incentives, or misleading ads", "ok": True},
        {"item": "Navigation is clear on mobile and desktop", "ok": True},
    ]
    score = sum(1 for c in checks if c["ok"])
    return {"score": score, "total": len(checks), "checks": checks}

def faq_schema(pairs):
    entities = []
    for p in pairs:
        q = (p.get("q") or "").strip()
        a = (p.get("a") or "").strip()
        if q and a:
            entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":entities}, ensure_ascii=False, indent=2)

def robots_txt(domain):
    domain = (domain or "https://example.com").rstrip("/")
    return f"""User-agent: *
Allow: /

Sitemap: {domain}/sitemap.xml
"""

def sitemap_xml(urls):
    clean = []
    for u in urls:
        u = (u or "").strip()
        if u:
            clean.append(u)
    body = "\n".join([f"  <url><loc>{u}</loc></url>" for u in clean])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
