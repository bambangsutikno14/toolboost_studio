import re
import json
from urllib.parse import urlencode
from collections import Counter

STOPWORDS = set('''
the and or for with from your you are how to of a an in on is best free yang dan untuk dengan dari ke di ini itu atau cara buat online
as by at be if into it its no not can will should would could may might about after before use using used users user tool tools
'''.split())

TOOLS = [
    {"name": "SEO Title Generator", "slug": "title-generator", "desc": "Buat ide judul SEO untuk artikel, landing page, dan video.", "intent": "creator, blogger, marketer", "keyword": "seo title generator"},
    {"name": "Meta Description Generator", "slug": "meta-description", "desc": "Buat meta description singkat agar halaman lebih menarik di hasil pencarian.", "intent": "SEO, website owner", "keyword": "meta description generator"},
    {"name": "Hashtag Generator", "slug": "hashtag-generator", "desc": "Buat hashtag relevan dari caption atau topik konten.", "intent": "TikTok, Instagram, Shorts", "keyword": "hashtag generator"},
    {"name": "Word Counter", "slug": "word-counter", "desc": "Hitung kata, karakter, kalimat, dan estimasi waktu baca.", "intent": "writer, student, editor", "keyword": "word counter"},
    {"name": "UTM Builder", "slug": "utm-builder", "desc": "Buat URL campaign tracking untuk analytics dan marketing.", "intent": "digital marketer", "keyword": "utm builder"},
    {"name": "Keyword Density Checker", "slug": "keyword-density-checker", "desc": "Cek kata yang paling sering muncul agar konten tidak berlebihan keyword.", "intent": "SEO writer", "keyword": "keyword density checker"},
    {"name": "Slug Generator", "slug": "slug-generator", "desc": "Ubah judul menjadi URL slug yang rapi dan SEO friendly.", "intent": "developer, blogger", "keyword": "slug generator"},
    {"name": "Content Brief Generator", "slug": "content-brief-generator", "desc": "Buat kerangka artikel: judul, outline, FAQ, dan keyword pendukung.", "intent": "content team", "keyword": "content brief generator"},
    {"name": "YouTube Description Generator", "slug": "youtube-description-generator", "desc": "Buat draft deskripsi YouTube dengan hook, summary, CTA, dan hashtag.", "intent": "YouTube creator", "keyword": "youtube description generator"},
    {"name": "FAQ Generator", "slug": "faq-generator", "desc": "Buat daftar FAQ berdasarkan topik dan target audience.", "intent": "SEO writer, support", "keyword": "faq generator"},
    {"name": "Blog Outline Generator", "slug": "blog-outline-generator", "desc": "Buat outline artikel cepat berdasarkan keyword dan search intent.", "intent": "blogger, writer", "keyword": "blog outline generator"},
    {"name": "Social Caption Generator", "slug": "social-caption-generator", "desc": "Buat caption sosial media dengan hook, value, dan CTA.", "intent": "social media creator", "keyword": "social caption generator"},
    {"name": "AdSense Readiness Checklist", "slug": "adsense-readiness-checklist", "desc": "Cek kesiapan situs sebelum diajukan ke AdSense.", "intent": "publisher", "keyword": "adsense readiness checklist"},
    {"name": "FAQ Schema JSON-LD Generator", "slug": "faq-schema-generator", "desc": "Buat JSON-LD FAQPage dari daftar pertanyaan dan jawaban.", "intent": "SEO developer", "keyword": "faq schema generator"},
    {"name": "Robots.txt Generator", "slug": "robots-generator", "desc": "Buat robots.txt sederhana dengan sitemap URL.", "intent": "webmaster", "keyword": "robots txt generator"},
    {"name": "Sitemap URL Builder", "slug": "sitemap-url-builder", "desc": "Buat daftar URL sitemap XML sederhana dari URL halaman.", "intent": "webmaster, SEO", "keyword": "sitemap url builder"},
]

GUIDES = [
    {
        "slug": "free-seo-tools-for-small-business",
        "title": "Free SEO Tools for Small Business: Practical Workflow",
        "description": "A practical guide for small businesses using free SEO tools to plan content, improve pages, and attract organic users.",
        "keyword": "free SEO tools for small business",
        "audience": "small business owners and solo marketers",
        "sections": [
            "Small businesses need simple tools that save time instead of complicated dashboards.",
            "Start with a clear page target: one keyword, one user problem, and one useful output.",
            "Use a title generator to produce angles, then manually choose the version that matches search intent.",
            "Use a meta description generator to write a concise search snippet that explains the benefit of the page.",
            "Use a word counter to keep tutorials complete without padding the article with repeated phrases.",
            "Track every campaign with UTM links so social traffic, newsletter traffic, and organic traffic are separated.",
        ],
        "faq": [
            ("Can free SEO tools compete with paid tools?", "Yes, for basic workflows. Paid tools help with large-scale data, but free tools can still support useful content and consistent publishing."),
            ("Should every page target a keyword?", "Every indexable page should have a clear topic and user problem. A keyword helps keep the page focused."),
        ],
    },
    {
        "slug": "youtube-title-generator-guide",
        "title": "YouTube Title Generator Guide for Better Clicks",
        "description": "Learn how to use a YouTube title generator without creating misleading clickbait.",
        "keyword": "YouTube title generator",
        "audience": "YouTube creators",
        "sections": [
            "A strong YouTube title explains what the viewer will get before they click.",
            "Use power words carefully. A title can be exciting without promising something fake.",
            "Create at least ten title options, then remove versions that are too vague or too long.",
            "Match the title with the thumbnail and video content. This improves viewer trust.",
            "For evergreen videos, include the main topic early in the title.",
            "Review analytics after publishing and rewrite titles that get impressions but low click-through rate.",
        ],
        "faq": [
            ("Is clickbait good for YouTube?", "Misleading clickbait may get clicks but can reduce trust and watch time. Clear benefit-based titles are safer."),
            ("How long should a YouTube title be?", "Keep it readable on mobile and put the most important words near the beginning."),
        ],
    },
    {
        "slug": "meta-description-examples",
        "title": "Meta Description Examples for Tools, Blogs, and Landing Pages",
        "description": "Practical meta description examples you can adapt for SaaS tools, blog posts, and business pages.",
        "keyword": "meta description examples",
        "audience": "website owners and content writers",
        "sections": [
            "A meta description should summarize the benefit of the page in a short sentence.",
            "For a tool page, mention the action users can complete, such as generate, calculate, check, or compare.",
            "For a guide, mention the problem solved and the type of reader who benefits.",
            "Avoid keyword stuffing. Repeating the same phrase makes the snippet look unnatural.",
            "Write descriptions that are accurate because search engines may rewrite snippets when they think another text is more useful.",
            "Review pages with high impressions and low click-through rate as candidates for better descriptions.",
        ],
        "faq": [
            ("Does meta description directly guarantee ranking?", "No. It is mainly useful for explaining the page and improving the search snippet."),
            ("Should each page have a unique meta description?", "Yes. Unique descriptions help users understand why each page exists."),
        ],
    },
    {
        "slug": "hashtag-generator-for-creators",
        "title": "Hashtag Generator for Creators: How to Pick Relevant Tags",
        "description": "Use hashtag ideas without spamming irrelevant tags. Learn a cleaner workflow for social content discovery.",
        "keyword": "hashtag generator for creators",
        "audience": "short-form video creators",
        "sections": [
            "Hashtags should describe the actual topic, audience, and format of your content.",
            "Use a mix of broad, medium, and niche tags so the content can be categorized correctly.",
            "Avoid adding trending hashtags that do not match your content.",
            "Create a saved list of tags for each content pillar, then rotate based on the specific post.",
            "Use the generator as a starting point, not as an automatic final answer.",
            "Measure which posts bring profile visits, saves, or website clicks instead of only views.",
        ],
        "faq": [
            ("How many hashtags should I use?", "Use only enough to describe the content clearly. Quality and relevance matter more than quantity."),
            ("Can hashtags replace good content?", "No. They help categorization, but the post still needs a strong hook and useful value."),
        ],
    },
    {
        "slug": "utm-builder-guide",
        "title": "UTM Builder Guide: Track Campaigns Without Confusion",
        "description": "A simple UTM naming system for marketers who want cleaner analytics.",
        "keyword": "UTM builder",
        "audience": "digital marketers",
        "sections": [
            "UTM links help you see which campaign, channel, or content variation sends visitors to your website.",
            "Create a naming convention before sharing links. Inconsistent names create messy reports.",
            "Use source for the platform, medium for the channel type, and campaign for the marketing push.",
            "Keep campaign names lowercase and use hyphens or underscores consistently.",
            "Do not use UTM parameters for internal links because they can break attribution.",
            "Store important campaign URLs in a spreadsheet so your team can reuse correct naming.",
        ],
        "faq": [
            ("Should I use UTM on every social link?", "Use UTM on campaign links when you need attribution. For casual internal navigation, do not use it."),
            ("What is the most common UTM mistake?", "Inconsistent naming. For example, facebook, Facebook, and fb become separate sources in reports."),
        ],
    },
    {
        "slug": "keyword-density-checker-guide",
        "title": "Keyword Density Checker Guide for Natural SEO Writing",
        "description": "Learn how to use keyword density as a quality signal without over-optimizing your content.",
        "keyword": "keyword density checker",
        "audience": "SEO writers",
        "sections": [
            "Keyword density is not a magic ranking formula. It is a simple check for unnatural repetition.",
            "Read the article out loud after checking density. If it sounds forced, rewrite it.",
            "Use related phrases, examples, and practical explanations instead of repeating the same keyword.",
            "Compare the top repeated words with the actual topic of the page.",
            "If unrelated words dominate the list, the article may need clearer structure.",
            "A useful article solves the searcher's problem better than a page that only repeats a target phrase.",
        ],
        "faq": [
            ("What keyword density is ideal?", "There is no universal ideal. Focus on clarity, topical coverage, and natural writing."),
            ("Can overusing keywords hurt the page?", "It can make the content look low quality and reduce user trust."),
        ],
    },
    {
        "slug": "slug-generator-best-practices",
        "title": "Slug Generator Best Practices for Clean URLs",
        "description": "Create cleaner URL slugs that are readable, short, and easier to share.",
        "keyword": "slug generator",
        "audience": "bloggers and developers",
        "sections": [
            "A URL slug should be short, readable, and related to the page title.",
            "Remove unnecessary words and keep the main topic in the slug.",
            "Use lowercase letters and hyphens between words.",
            "Avoid changing slugs after publication unless you are ready to create redirects.",
            "A clean slug helps users understand the page before they open it.",
            "For tool pages, keep the slug stable and descriptive, such as keyword-density-checker.",
        ],
        "faq": [
            ("Should a slug include the full title?", "No. Use the core topic only. Long slugs are harder to read."),
            ("Can I change a slug later?", "Yes, but use a proper redirect so old links do not break."),
        ],
    },
    {
        "slug": "adsense-ready-website-checklist",
        "title": "AdSense Ready Website Checklist for SaaS Tool Sites",
        "description": "A practical checklist before applying AdSense to a new SaaS tool website.",
        "keyword": "AdSense website checklist",
        "audience": "website publishers",
        "sections": [
            "A useful website should have original content, clear navigation, and a real purpose beyond showing ads.",
            "Add privacy policy, terms, contact page, and about information before applying.",
            "Do not send fake traffic or ask people to click ads.",
            "Create enough helpful pages so the site does not look thin.",
            "Make sure the website works on mobile and loads quickly.",
            "Apply only after the product and content are useful enough for real visitors.",
        ],
        "faq": [
            ("Can I apply with a localhost website?", "No. Use a real domain that Google can crawl."),
            ("Should I add ad placeholders before approval?", "Placeholders for layout are fine, but real ad code should follow account and site approval rules."),
        ],
    },
    {
        "slug": "simple-saas-seo-strategy",
        "title": "Simple SaaS SEO Strategy for New Websites",
        "description": "A beginner-friendly SaaS SEO strategy focused on useful tools, long-tail keywords, and consistent improvement.",
        "keyword": "simple SaaS SEO strategy",
        "audience": "new SaaS builders",
        "sections": [
            "New SaaS websites should start with long-tail searches because broad keywords are usually too competitive.",
            "Each tool page should answer a specific task, not a vague topic.",
            "Add guide pages that explain when to use the tool, examples, mistakes, and workflows.",
            "Create internal links between related tools and guides.",
            "Measure pages with impressions but low clicks, then improve titles and descriptions.",
            "Improve the actual tool based on what users search for and ask after landing on the site.",
        ],
        "faq": [
            ("How long does SEO take?", "It usually takes time because search engines need to discover, crawl, evaluate, and rank pages."),
            ("Should I publish many pages at once?", "Publish enough useful pages to explain the product, then improve quality continuously."),
        ],
    },
    {
        "slug": "word-counter-for-seo-writing",
        "title": "Word Counter for SEO Writing: Better Draft Checks",
        "description": "Use a word counter to review content structure, reading time, and completeness before publishing.",
        "keyword": "word counter for SEO writing",
        "audience": "writers and editors",
        "sections": [
            "A word counter is useful for checking draft structure, but it should not force artificial length.",
            "Compare the draft with the searcher's goal. Some questions need short answers, others need complete tutorials.",
            "Use reading time to set expectations for visitors.",
            "Check whether headings, examples, and FAQ sections make the article easier to scan.",
            "Remove filler sentences that do not answer the user's question.",
            "A clear short article is better than a long page that repeats itself.",
        ],
        "faq": [
            ("Is longer content always better?", "No. The right length depends on the problem, intent, and completeness of the answer."),
            ("Can word count affect SEO?", "Word count alone is not the goal. Usefulness and completeness matter more."),
        ],
    },
]

ACRONYMS = {
    "seo": "SEO", "utm": "UTM", "faq": "FAQ", "ai": "AI", "asmr": "ASMR",
    "api": "API", "pdf": "PDF", "csv": "CSV", "json": "JSON", "url": "URL",
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

def tagify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "", (value or "").strip().lower())
    if not value or len(value) < 2 or value.isdigit():
        return ""
    return "#" + value

def add_tag(tags, value):
    tag = tagify(value)
    if tag and tag not in tags:
        tags.append(tag)

def title_ideas(keyword):
    kw_raw = (keyword or "online tool").strip()
    kw = smart_title(kw_raw)
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
    ]
    return [t.format(kw=kw) for t in templates]

def meta_description(keyword):
    kw = smart_title(keyword or "online tool")
    return (f"Use this free {kw} tool to create faster workflows, improve content quality, "
            f"and save time with a simple browser-based utility.")[:155]

def hashtag_ideas(text, min_tags=5, max_tags=18):
    """
    Generate valid and relevant hashtags from a caption/topic.
    Rules:
    - Always returns at least 5 hashtags when possible.
    - Keeps acronyms valid: ASMR -> #asmr, SEO -> #seo, UTM -> #utm.
    - Does not create broken tags like #smr or #ain.
    - Adds topic-aware tags for common creator/SEO/marketing niches.
    """
    raw = (text or "").strip()
    terms = clean_words(raw)
    tags = []

    if terms:
        # Exact words first. Example: "asmr rain" -> #asmr #rain
        for w in terms[:10]:
            add_tag(tags, w)

        # Useful phrase tags. Example: "asmr rain" -> #asmrrain
        if len(terms) >= 2:
            add_tag(tags, "".join(terms[:2]))
        if len(terms) >= 3:
            add_tag(tags, "".join(terms[:3]))

        # Adjacent combined terms
        for i in range(min(len(terms) - 1, 5)):
            add_tag(tags, terms[i] + terms[i + 1])

        # Topic-aware clusters
        for w in terms:
            for item in HASHTAG_CLUSTERS.get(w, []):
                add_tag(tags, item)

        termset = set(terms)

        if {"asmr", "rain"}.issubset(termset):
            for item in [
                "asmrrain", "rainasmr", "rainsounds", "rainsound", "rainforsleep",
                "sleepasmr", "relaxingrain", "whitenoise", "deepsleep", "calmingvideo",
                "relaxingsounds", "sleepaid"
            ]:
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

    # Fallbacks are used only to reach the minimum count.
    fallback_pool = [
        "contentideas", "creator", "creatorcommunity", "digitalcreator", "marketingtools",
        "productivity", "onlinetools", "contentcreator", "socialmedia", "growth"
    ]
    if any(t in set(terms) for t in ["asmr", "rain", "sleep", "relax"]):
        fallback_pool = [
            "relaxing", "calming", "sleepsounds", "relaxingsounds", "deepsleep",
            "whitenoise", "meditation", "sleepaid", "relaxingvideo", "asmrvideo"
        ] + fallback_pool

    for item in fallback_pool:
        if len(tags) >= min_tags:
            break
        add_tag(tags, item)

    return tags[:max_tags]

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
    sep = "&" if "?" in (url or "") else "?"
    return (url or "https://example.com") + sep + urlencode(params)

def keyword_density(text):
    words = clean_words(text)
    total = len(words) or 1
    counts = Counter(words)
    rows = []
    for word, count in counts.most_common(20):
        rows.append({"word": word, "count": count, "density": round((count / total) * 100, 2)})
    return {"total_words": len(words), "rows": rows}

def slugify(text):
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text or "new-page"

def content_brief(topic, audience=""):
    topic = (topic or "online tool").strip()
    audience = (audience or "beginners").strip()
    return {
        "titles": title_ideas(topic)[:5],
        "meta": meta_description(topic),
        "outline": [
            f"What is {topic}?",
            f"Why {audience} need {topic}",
            f"How to use {topic} step by step",
            "Common mistakes to avoid",
            "Examples and templates",
            "FAQ",
        ],
        "faqs": [
            f"What is the best way to use {topic}?",
            f"Is {topic} suitable for {audience}?",
            f"What mistakes should I avoid when using {topic}?",
            f"Can I use a free {topic} tool?",
        ],
        "internal_links": ["/tools/title-generator", "/tools/meta-description", "/tools/word-counter", "/tools/keyword-density-checker"],
    }

def youtube_description(topic, keywords=""):
    topic = (topic or "useful video").strip()
    tags = hashtag_ideas(topic + " " + keywords)
    return {
        "description": (
            f"In this video, we cover {topic}. Watch until the end for practical tips, examples, "
            f"and a simple workflow you can apply today.\n\n"
            f"Key points:\n- What {topic} means\n- Common mistakes to avoid\n- Step-by-step workflow\n- Practical examples\n\n"
            f"Subscribe for more creator, SEO, and marketing tools."
        ),
        "hashtags": tags[:8],
    }

def faq_generator(topic, audience=""):
    topic = (topic or "online tool").strip()
    audience = (audience or "beginners").strip()
    return [
        {"q": f"What is {topic}?", "a": f"{topic} is a topic or tool that helps {audience} solve a specific workflow faster."},
        {"q": f"Who should use {topic}?", "a": f"{topic} is useful for {audience} who need a simple and repeatable process."},
        {"q": f"Is {topic} free to use?", "a": "This starter tool can be used for free, while advanced features can be added later."},
        {"q": f"How do I get better results with {topic}?", "a": "Use specific input, review the output manually, and match it to the actual audience and intent."},
    ]

def blog_outline(topic, intent="informational"):
    topic = (topic or "online tool").strip()
    return [
        f"H1: {topic.title()}",
        "Intro: Explain the problem and promise a practical answer.",
        f"H2: What is {topic}?",
        "H2: Why this matters for users",
        "H2: Step-by-step workflow",
        "H2: Examples",
        "H2: Common mistakes",
        "H2: FAQ",
        "Conclusion: Summarize the next action.",
    ]

def social_caption(topic, platform="TikTok"):
    topic = (topic or "free online tool").strip()
    return {
        "hook": f"Stop wasting time on {topic}.",
        "caption": f"I made a simple workflow for {topic}. Try it, copy the output, and adjust it for your own content.",
        "cta": "Save this and test it today.",
        "hashtags": hashtag_ideas(topic + " " + platform)[:8],
    }

def adsense_checklist(site_url="", pages_count=0, has_privacy=False, has_terms=False, has_contact=False, has_original_content=False):
    checks = [
        ("Domain public", bool(site_url and not site_url.startswith("http://127."))),
        ("Privacy Policy", bool(has_privacy)),
        ("Terms of Service", bool(has_terms)),
        ("Contact page", bool(has_contact)),
        ("Original useful content", bool(has_original_content)),
        ("Enough pages", int(pages_count or 0) >= 15),
    ]
    score = sum(1 for _, ok in checks if ok)
    return {"score": score, "total": len(checks), "checks": [{"item": n, "ok": ok} for n, ok in checks]}

def faq_schema(items):
    entities = []
    for item in items:
        q = (item.get("q") or "").strip()
        a = (item.get("a") or "").strip()
        if q and a:
            entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, indent=2, ensure_ascii=False)

def robots_txt(domain):
    domain = (domain or "https://example.com").rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n"

def sitemap_xml(urls):
    clean = []
    for u in urls:
        u = (u or "").strip()
        if u:
            clean.append(u)
    body = "\n".join(f"<url><loc>{u}</loc></url>" for u in clean)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>'
