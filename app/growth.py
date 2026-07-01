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
    {"name":"Creator Content Pack Generator","slug":"creator-content-pack","keyword":"creator content pack generator","intent":"generate complete content packs","desc":"Generate titles, hooks, short script, captions, hashtags, thumbnail text, pinned comment, and upload checklist from one idea."},
    {"name":"Shorts Script Generator","slug":"shorts-script-generator","keyword":"shorts script generator","intent":"write short video scripts","desc":"Create a mobile-friendly short video script with hook, scenes, subtitles, CTA, caption, and hashtags."},
    {"name":"Thumbnail Text Maker","slug":"thumbnail-text-maker","keyword":"thumbnail text maker","intent":"create thumbnail text ideas","desc":"Generate short thumbnail words, curiosity angles, layout notes, and emotional text variants for beginner creators."},
    {"name":"Content Calendar Generator","slug":"content-calendar-generator","keyword":"content calendar generator","intent":"plan consistent uploads","desc":"Create a 7-day or 30-day creator content calendar with topic angle, title, caption, CTA, and hashtags."},
    {"name":"Clip Idea Generator","slug":"clip-idea-generator","keyword":"clip idea generator","intent":"find short clip ideas","desc":"Turn a transcript or rough notes into clip ideas, hooks, titles, captions, and timestamp-style sections."},
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

CREATOR_TOOL_SLUGS = [
    "creator-content-pack",
    "shorts-script-generator",
    "thumbnail-text-maker",
    "content-calendar-generator",
    "clip-idea-generator",
]

GUIDES = [
    {"title":"Creator Content Toolkit: Faster Workflow for Beginners","slug":"creator-content-toolkit-workflow","keyword":"creator content toolkit","description":"A practical workflow for turning one idea into titles, scripts, captions, hashtags, thumbnail text, and an upload checklist."},
    {"title":"How Beginner Creators Can Plan 7 Days of Content","slug":"beginner-creator-content-calendar","keyword":"content calendar for creators","description":"Use a simple content calendar to reduce decision fatigue and upload more consistently."},
    {"title":"Shorts Script Formula for YouTube, TikTok, and Reels","slug":"shorts-script-formula","keyword":"shorts script generator","description":"A fast script structure with hook, value, scene flow, subtitles, and CTA."},
    {"title":"Thumbnail Text Ideas That Beginners Can Use","slug":"thumbnail-text-ideas","keyword":"thumbnail text maker","description":"How to write short, clear thumbnail text that supports the title without misleading viewers."},
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


# ---------------------------
# V7 Creator Studio Engine
# ---------------------------

PLATFORM_PRESETS = {
    "youtube shorts": {"length": "35-55 seconds", "cta": "Subscribe for more simple creator workflows.", "format": "short vertical video"},
    "youtube": {"length": "3-8 minutes", "cta": "Subscribe and save this for your next upload.", "format": "video"},
    "tiktok": {"length": "20-45 seconds", "cta": "Save this and try it for your next post.", "format": "short vertical video"},
    "instagram reels": {"length": "20-45 seconds", "cta": "Save this reel and follow for more ideas.", "format": "reel"},
    "reels": {"length": "20-45 seconds", "cta": "Save this reel and follow for more ideas.", "format": "reel"},
    "blog": {"length": "600-1200 words", "cta": "Bookmark this guide and use the checklist.", "format": "article"},
}

TONE_PRESETS = {
    "relaxing": ["calm", "soft", "slow", "comforting", "peaceful"],
    "viral": ["curious", "fast", "bold", "high-energy", "shareable"],
    "educational": ["clear", "useful", "step-by-step", "practical", "beginner-friendly"],
    "professional": ["trusted", "simple", "direct", "polished", "credible"],
    "funny": ["light", "playful", "unexpected", "casual", "memorable"],
}

def normalize_choice(value, default="youtube shorts"):
    value = (value or default).strip().lower()
    return value

def platform_profile(platform):
    key = normalize_choice(platform)
    return PLATFORM_PRESETS.get(key, {"length": "30-60 seconds", "cta": "Save this and try it today.", "format": key or "content"})

def tone_words(tone):
    return TONE_PRESETS.get(normalize_choice(tone, "educational"), TONE_PRESETS["educational"])

def creator_angles(niche, goal="growth"):
    topic = smart_title(niche or "creator content")
    goal = (goal or "growth").strip().lower()
    base = [
        f"Beginner mistake in {topic}",
        f"Fast workflow for {topic}",
        f"Before vs after using {topic}",
        f"Simple checklist for {topic}",
        f"One-minute guide to {topic}",
        f"Why {topic} feels hard at first",
        f"How to start {topic} with limited tools",
        f"Save time with this {topic} process",
        f"{topic} idea you can try today",
        f"Common myth about {topic}",
    ]
    if "money" in goal or "monet" in goal:
        base.insert(0, f"How {topic} can support monetization")
        base.insert(1, f"Low-cost {topic} workflow for beginners")
    elif "engage" in goal:
        base.insert(0, f"Question-based {topic} idea to get comments")
    elif "affiliate" in goal:
        base.insert(0, f"Soft-sell {topic} content idea for affiliate posts")
    return base[:10]

def creator_title_pack(niche, platform="", tone="", goal=""):
    topic = smart_title(niche or "creator content")
    platform_name = smart_title(platform or "YouTube Shorts")
    words = tone_words(tone)
    titles = [
        f"{topic} Made Simple for Beginners",
        f"How to Create {topic} Content Faster",
        f"Stop Overthinking {topic}: Use This Workflow",
        f"{topic} Ideas You Can Use Today",
        f"Beginner {topic} Checklist for {platform_name}",
        f"Make Better {topic} Content With Less Stress",
        f"One Simple {topic} Workflow That Saves Time",
        f"From Idea to Upload: {topic} Content Pack",
        f"{topic} Tips for Creators Who Want to Grow",
        f"Try This {words[0].capitalize()} {topic} Workflow",
    ]
    result = []
    for item in titles:
        add_unique(result, item[:72].rstrip(" -:"))
    return result[:10]

def creator_hooks(niche, platform="", tone="", goal=""):
    topic = smart_title(niche or "creator content")
    words = tone_words(tone)
    hooks = [
        f"If you are stuck on {topic.lower()}, start with this simple workflow.",
        f"Here is a faster way to plan {topic.lower()} without overthinking.",
        f"Most beginners make {topic.lower()} too complicated.",
        f"Before you upload, check these {topic.lower()} basics.",
        f"You do not need expensive tools to start {topic.lower()} today.",
    ]
    if "viral" in normalize_choice(tone, ""):
        hooks = [
            f"This is why your {topic.lower()} content feels slow to make.",
            f"I wish I knew this {topic.lower()} workflow earlier.",
            f"Stop scrolling and save this {topic.lower()} shortcut.",
            f"One small fix can make your {topic.lower()} easier to finish.",
            f"Use this before you create your next {topic.lower()} post.",
        ]
    if "relax" in normalize_choice(tone, ""):
        hooks = [
            f"Here is a calm and simple {topic.lower()} idea for your next upload.",
            f"Use this peaceful workflow when you do not know what to post.",
            f"Create {topic.lower()} content slowly, clearly, and without stress.",
            f"This simple {topic.lower()} plan helps you stay consistent.",
            f"Save this {words[0]} content idea for your next upload.",
        ]
    return hooks

def short_script_scenes(topic, platform="", tone="", audience="", duration="45"):
    topic_title = smart_title(topic or "creator content")
    profile = platform_profile(platform)
    audience = (audience or "beginner creators").strip()
    words = tone_words(tone)
    return [
        {"time": "0-3s", "label": "Hook", "line": f"If you are a {audience} stuck on {topic_title.lower()}, use this simple plan."},
        {"time": "3-10s", "label": "Problem", "line": f"Most people waste time because they try to create the title, script, caption, and hashtags separately."},
        {"time": "10-25s", "label": "Value", "line": f"Start with one idea, choose one angle, write a short hook, then package it for {smart_title(platform or 'your platform')}."},
        {"time": "25-40s", "label": "Action", "line": f"Use a checklist: title, thumbnail text, caption, hashtags, and one clear CTA."},
        {"time": "40-55s", "label": "CTA", "line": profile["cta"]},
    ]

def shorts_script(topic, platform="YouTube Shorts", duration="45", tone="educational", audience="beginner creators"):
    topic_title = smart_title(topic or "creator content")
    profile = platform_profile(platform)
    scenes = short_script_scenes(topic_title, platform, tone, audience, duration)
    subtitle_text = [s["line"] for s in scenes]
    caption = f"Create {topic_title} content faster with a simple {profile['format']} workflow. Save this for your next upload."
    tags = hashtag_ideas(f"{topic_title} {platform} creator tools content")[:12]
    return {
        "topic": topic_title,
        "platform": smart_title(platform or "YouTube Shorts"),
        "duration": profile["length"],
        "scenes": scenes,
        "subtitle_text": subtitle_text,
        "caption": caption,
        "hashtags": tags,
        "checklist": ["Record vertically", "Keep hook under 3 seconds", "Add readable subtitles", "Use one CTA", "Review sound and pacing before posting"],
    }

def thumbnail_text_maker(topic, platform="", emotion="curiosity"):
    topic_title = smart_title(topic or "creator content")
    emotion = (emotion or "curiosity").strip().lower()
    variants = [
        {"style": "Curiosity", "text": f"Try This", "support": f"Use with title about {topic_title}."},
        {"style": "Problem", "text": f"Stop This", "support": f"Good for mistake/avoidance content."},
        {"style": "Result", "text": f"Faster Content", "support": f"Good for time-saving workflow content."},
        {"style": "Beginner", "text": f"Start Here", "support": f"Good for beginner tutorial content."},
        {"style": "Checklist", "text": f"Upload Ready", "support": f"Good for packaging and publishing content."},
        {"style": "Calm", "text": f"No Stress", "support": f"Good for simple workflow and relaxing niches."},
    ]
    if "money" in emotion or "profit" in emotion:
        variants.insert(0, {"style": "Monetization", "text": "Make It Pay", "support": "Use carefully; avoid unrealistic income promises."})
    layout_notes = [
        "Use 2-4 words maximum on the thumbnail.",
        "Make text readable on mobile first.",
        "Do not repeat the exact same words as the title.",
        "Use contrast, face/object focus, and one clear visual idea.",
        "Avoid fake claims or misleading before-after promises.",
    ]
    return {
        "topic": topic_title,
        "variants": variants[:8],
        "layout_notes": layout_notes,
        "title_pairing": creator_title_pack(topic_title, platform, emotion)[:5],
    }

def content_calendar(niche, platform="YouTube Shorts", days="7", audience="beginner creators", goal="growth"):
    try:
        n = int(days)
    except Exception:
        n = 7
    n = max(1, min(n, 30))
    niche_title = smart_title(niche or "creator content")
    platform_name = smart_title(platform or "YouTube Shorts")
    angles = creator_angles(niche_title, goal)
    rows = []
    for i in range(1, n + 1):
        angle = angles[(i - 1) % len(angles)]
        title = creator_title_pack(f"{niche_title} {angle}", platform, "educational", goal)[0]
        tags = hashtag_ideas(f"{niche_title} {platform} {angle}")[:8]
        rows.append({
            "day": i,
            "angle": angle,
            "title": title,
            "hook": creator_hooks(f"{niche_title} {angle}", platform, "educational", goal)[0],
            "caption": f"Day {i}: {angle}. Save this if you are building {niche_title.lower()} content for {platform_name}.",
            "cta": "Save this and use it for your next upload.",
            "hashtags": tags,
        })
    return {
        "niche": niche_title,
        "platform": platform_name,
        "days": rows,
        "workflow": ["Batch 3 ideas at once", "Write hooks first", "Reuse formats that perform", "Track impressions and clicks", "Improve one variable per upload"],
    }

def creator_content_pack(niche, platform="YouTube Shorts", audience="beginner creators", tone="educational", goal="growth"):
    niche_title = smart_title(niche or "creator content")
    platform_name = smart_title(platform or "YouTube Shorts")
    profile = platform_profile(platform)
    titles = creator_title_pack(niche_title, platform, tone, goal)
    hooks = creator_hooks(niche_title, platform, tone, goal)
    script = shorts_script(niche_title, platform, "45", tone, audience)
    thumbnail = thumbnail_text_maker(niche_title, platform, tone)
    tags = hashtag_ideas(f"{niche_title} {platform} {audience} {goal}")[:14]
    youtube_desc = youtube_description(niche_title, " ".join(tags[:5]))
    social = social_caption(niche_title, platform_name)
    pinned_comment = f"What part of {niche_title.lower()} is hardest for you right now: idea, script, caption, or consistency?"
    checklist = [
        "Choose one clear angle",
        "Pick one title and one thumbnail text",
        "Keep the hook short",
        "Add captions/subtitles",
        "Use relevant hashtags only",
        "Write one CTA",
        "Check mobile readability",
        "Publish and track impressions, clicks, and retention",
    ]
    next_ideas = creator_angles(niche_title, goal)[:7]
    return {
        "niche": niche_title,
        "platform": platform_name,
        "audience": audience or "beginner creators",
        "tone": tone or "educational",
        "goal": goal or "growth",
        "format": profile["format"],
        "titles": titles,
        "hooks": hooks,
        "script": script,
        "youtube_description": youtube_desc["description"],
        "social_caption": social["caption"],
        "hashtags": tags,
        "thumbnail_text": thumbnail["variants"][:6],
        "pinned_comment": pinned_comment,
        "upload_checklist": checklist,
        "next_content_ideas": next_ideas,
    }

def split_transcript_chunks(text):
    raw = re.split(r"(?<=[.!?])\s+|\n+", (text or "").strip())
    chunks = [c.strip() for c in raw if len(c.strip()) > 15]
    if not chunks:
        chunks = [c.strip() for c in re.split(r"[,;]+", text or "") if len(c.strip()) > 15]
    return chunks[:12]

def clip_idea_generator(transcript, platform="YouTube Shorts", niche=""):
    chunks = split_transcript_chunks(transcript)
    topic = smart_title(niche or (chunks[0] if chunks else "creator content"))
    ideas = []
    if not chunks:
        chunks = [
            f"Explain one beginner mistake about {topic}.",
            f"Show a faster workflow for {topic}.",
            f"Give a checklist for {topic}.",
        ]
    for idx, chunk in enumerate(chunks[:6], start=1):
        clean = chunk[:130].strip()
        ideas.append({
            "clip": idx,
            "section": f"Clip {idx}",
            "hook": f"Use this part as a hook: {clean}",
            "title": creator_title_pack(f"{topic} clip {idx}", platform)[0],
            "caption": f"Clip idea {idx} for {topic}. Turn this section into a short, clear post and add one CTA.",
            "hashtags": hashtag_ideas(f"{topic} {platform} clip idea")[:8],
        })
    return {
        "topic": topic,
        "platform": smart_title(platform or "YouTube Shorts"),
        "ideas": ideas,
        "editing_notes": [
            "Keep each clip focused on one idea.",
            "Add subtitles for mobile viewers.",
            "Cut silence and repeated words.",
            "Open with the strongest sentence.",
            "Do not use copyrighted video/audio without permission.",
        ],
    }
