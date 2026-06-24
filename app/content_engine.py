
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime
from html.parser import HTMLParser

STOPWORDS = set("""
the and or for with from your you are how to of a an in on is best free yang dan untuk dengan dari ke di ini itu atau cara buat online tool generator checker builder secara lebih agar dalam pada sebagai bisa akan atau untuk by it as at be this that can not is are was were
""".split())

TOOLS = [
    {
        "slug": "title-generator",
        "name": "SEO Title Generator",
        "category": "SEO Content",
        "input_label": "Keyword / topik",
        "input_placeholder": "example: free invoice generator",
        "result_type": "list",
        "summary": "Buat variasi judul SEO yang jelas, natural, dan cocok untuk artikel, landing page, atau video.",
        "intent": "creator, blogger, marketer",
        "example_input": "youtube title generator for shorts",
        "example_output": "Free YouTube Title Generator for Shorts\nHow to Create Better YouTube Shorts Titles\nYouTube Shorts Title Ideas for Beginner Creators",
        "keywords": ["seo title generator", "youtube title generator", "blog title ideas"],
    },
    {
        "slug": "meta-description",
        "name": "Meta Description Generator",
        "category": "SEO Content",
        "input_label": "Keyword / topik halaman",
        "input_placeholder": "example: keyword density checker",
        "result_type": "text",
        "summary": "Buat meta description singkat untuk menjelaskan manfaat halaman di hasil pencarian.",
        "intent": "SEO writer, website owner",
        "example_input": "free keyword density checker",
        "example_output": "Use this free keyword density checker to review repeated words, improve SEO drafts, and make your content clearer before publishing.",
        "keywords": ["meta description generator", "seo meta description", "search snippet generator"],
    },
    {
        "slug": "hashtag-generator",
        "name": "Hashtag Generator",
        "category": "Social Media",
        "input_label": "Caption / topik konten",
        "input_placeholder": "example: simple SEO tips for small business",
        "result_type": "tags",
        "summary": "Buat hashtag relevan dari caption atau topik untuk membantu kategorisasi konten sosial.",
        "intent": "TikTok, Instagram, YouTube Shorts creator",
        "example_input": "free SEO tools for small business owners",
        "example_output": "#SeoTools #SmallBusiness #Marketing #ContentCreator #Productivity",
        "keywords": ["hashtag generator", "social media hashtags", "creator hashtags"],
    },
    {
        "slug": "word-counter",
        "name": "Word Counter",
        "category": "Writing",
        "input_label": "Teks",
        "input_placeholder": "Paste article, caption, essay, or landing page copy",
        "result_type": "metrics",
        "summary": "Hitung kata, karakter, kalimat, dan estimasi waktu baca untuk mengecek kualitas draft.",
        "intent": "writer, student, editor",
        "example_input": "This is a simple draft for a marketing page.",
        "example_output": "Words: 9 | Characters: 44 | Reading time: 1 min",
        "keywords": ["word counter", "character counter", "reading time calculator"],
    },
    {
        "slug": "utm-builder",
        "name": "UTM Builder",
        "category": "Marketing Analytics",
        "input_label": "Campaign URL data",
        "input_placeholder": "Fill URL, source, medium, campaign",
        "result_type": "text",
        "summary": "Buat URL tracking campaign agar traffic dari social, email, dan iklan lebih mudah dianalisis.",
        "intent": "digital marketer, advertiser, small business",
        "example_input": "URL: https://example.com | source: tiktok | medium: social | campaign: launch",
        "example_output": "https://example.com?utm_source=tiktok&utm_medium=social&utm_campaign=launch",
        "keywords": ["utm builder", "campaign url builder", "utm generator"],
    },
    {
        "slug": "keyword-density-checker",
        "name": "Keyword Density Checker",
        "category": "SEO Audit",
        "input_label": "Artikel / copywriting",
        "input_placeholder": "Paste draft content here",
        "result_type": "table",
        "summary": "Cek kata yang paling sering muncul agar tulisan tidak terlihat spam keyword dan tetap natural.",
        "intent": "SEO writer, blogger, editor",
        "example_input": "SEO tools help SEO writers review SEO drafts.",
        "example_output": "seo: 3 times, tools: 1 time, writers: 1 time",
        "keywords": ["keyword density checker", "keyword stuffing checker", "seo writing checker"],
    },
    {
        "slug": "slug-generator",
        "name": "Slug Generator",
        "category": "Technical SEO",
        "input_label": "Judul halaman",
        "input_placeholder": "example: Best Free SEO Tools for Small Business",
        "result_type": "text",
        "summary": "Ubah judul menjadi URL slug yang pendek, rapi, dan mudah dibaca.",
        "intent": "blogger, developer, SEO specialist",
        "example_input": "Best Free SEO Tools for Small Business",
        "example_output": "best-free-seo-tools-small-business",
        "keywords": ["slug generator", "url slug generator", "seo friendly url"],
    },
    {
        "slug": "content-brief-generator",
        "name": "Content Brief Generator",
        "category": "Content Planning",
        "input_label": "Topik artikel",
        "input_placeholder": "example: youtube title generator",
        "result_type": "brief",
        "summary": "Buat brief konten otomatis berisi judul, outline, FAQ, dan internal link ideas.",
        "intent": "content writer, SEO team, marketer",
        "example_input": "youtube title generator for beginners",
        "example_output": "Title ideas, outline, FAQ, related tools, and meta description.",
        "keywords": ["content brief generator", "seo content brief", "article outline generator"],
    },
    {
        "slug": "youtube-description-generator",
        "name": "YouTube Description Generator",
        "category": "Video SEO",
        "input_label": "Judul / topik video",
        "input_placeholder": "example: relaxing rain sound for sleep",
        "result_type": "text",
        "summary": "Buat deskripsi video YouTube yang rapi dengan hook, ringkasan, CTA, dan hashtag.",
        "intent": "YouTube creator",
        "example_input": "relaxing rain sound for sleep",
        "example_output": "Enjoy relaxing rain sound for sleep, study, and deep focus. Use headphones for a calm ambience. Subscribe for more relaxing audio.",
        "keywords": ["youtube description generator", "video description generator", "youtube seo tool"],
    },
    {
        "slug": "faq-generator",
        "name": "FAQ Generator",
        "category": "Content Planning",
        "input_label": "Produk / topik",
        "input_placeholder": "example: free UTM builder",
        "result_type": "list",
        "summary": "Buat ide FAQ untuk memperkuat halaman tool, artikel, dan landing page.",
        "intent": "SEO writer, product marketer",
        "example_input": "free UTM builder",
        "example_output": "What is a UTM builder?\nWhen should I use UTM parameters?\nWhat is the most common UTM mistake?",
        "keywords": ["faq generator", "seo faq ideas", "faq schema content"],
    },
    {
        "slug": "blog-outline-generator",
        "name": "Blog Outline Generator",
        "category": "Writing",
        "input_label": "Topik blog",
        "input_placeholder": "example: how to track social media campaigns",
        "result_type": "list",
        "summary": "Buat outline artikel yang terstruktur dari intro sampai FAQ.",
        "intent": "blogger, SEO writer",
        "example_input": "how to track social media campaigns",
        "example_output": "Introduction\nWhy tracking matters\nUTM setup\nCommon mistakes\nFAQ",
        "keywords": ["blog outline generator", "article outline", "seo outline generator"],
    },
    {
        "slug": "social-caption-generator",
        "name": "Social Caption Generator",
        "category": "Social Media",
        "input_label": "Topik posting",
        "input_placeholder": "example: free keyword density checker",
        "result_type": "text",
        "summary": "Buat caption singkat untuk TikTok, Threads, LinkedIn, atau Instagram.",
        "intent": "social media creator, founder",
        "example_input": "free keyword density checker",
        "example_output": "I built a free keyword density checker to help writers spot repeated words before publishing. Try it and make your SEO drafts cleaner.",
        "keywords": ["social caption generator", "caption ideas", "post caption generator"],
    },
    {
        "slug": "adsense-checklist-generator",
        "name": "AdSense Readiness Checklist Generator",
        "category": "Monetization",
        "input_label": "Jenis website",
        "input_placeholder": "example: free SEO tools website",
        "result_type": "checklist",
        "summary": "Buat checklist kesiapan sebelum mengajukan website ke AdSense.",
        "intent": "publisher, indie hacker",
        "example_input": "free SEO tools website",
        "example_output": "Privacy page, Terms page, Contact page, original content, no fake traffic, sitemap, mobile friendly.",
        "keywords": ["adsense checklist", "website monetization checklist", "adsense approval"],
    },
    {
        "slug": "faq-schema-generator",
        "name": "FAQ Schema JSON-LD Generator",
        "category": "Technical SEO",
        "input_label": "FAQ text",
        "input_placeholder": "Format: Question? Answer. One FAQ per line.",
        "result_type": "code",
        "summary": "Ubah daftar FAQ menjadi JSON-LD schema yang rapi untuk halaman yang memiliki FAQ terlihat.",
        "intent": "SEO specialist, developer",
        "example_input": "What is SEO? SEO means search engine optimization.",
        "example_output": "{ '@context': 'https://schema.org', '@type': 'FAQPage', ... }",
        "keywords": ["faq schema generator", "json ld faq", "structured data tool"],
    },
    {
        "slug": "robots-txt-generator",
        "name": "Robots.txt Generator",
        "category": "Technical SEO",
        "input_label": "Domain",
        "input_placeholder": "example: https://example.com",
        "result_type": "code",
        "summary": "Buat robots.txt sederhana dengan sitemap untuk website tool.",
        "intent": "developer, website owner",
        "example_input": "https://example.com",
        "example_output": "User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml",
        "keywords": ["robots.txt generator", "sitemap robots", "technical seo tool"],
    },
    {
        "slug": "sitemap-url-builder",
        "name": "Sitemap URL Builder",
        "category": "Technical SEO",
        "input_label": "Daftar URL, satu per baris",
        "input_placeholder": "https://example.com/\nhttps://example.com/tools/title-generator",
        "result_type": "code",
        "summary": "Ubah daftar URL menjadi XML sitemap sederhana.",
        "intent": "developer, website owner",
        "example_input": "https://example.com/\nhttps://example.com/contact",
        "example_output": "<?xml version='1.0'?><urlset>...</urlset>",
        "keywords": ["sitemap generator", "xml sitemap builder", "url sitemap tool"],
    },
]

EXTRA_KEYWORDS = [
    "free seo title generator for bloggers",
    "youtube title ideas for shorts",
    "meta description examples for tool pages",
    "keyword density checker for seo writing",
    "slug generator for blog titles",
    "utm builder for small business campaigns",
    "content brief generator for seo writers",
    "youtube description generator for relaxing music",
    "faq generator for landing pages",
    "blog outline generator for beginners",
    "social caption generator for creators",
    "adsense readiness checklist for new websites",
    "faq schema generator json ld",
    "robots txt generator for small websites",
    "sitemap url builder online",
    "free creator tools for social media",
    "simple saas seo strategy for new websites",
    "how to avoid keyword stuffing",
    "how to write better meta descriptions",
    "how to track campaign links with utm",
]


def site_domain():
    return os.getenv("SITE_DOMAIN", "http://127.0.0.1:8000").rstrip("/")


def clean_words(text):
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def title_case(text):
    return " ".join(w.capitalize() for w in re.findall(r"[a-z0-9]+", text or "online tool"))


def slugify(text):
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text) or "new-page"


def title_ideas(topic):
    raw = (topic or "online tool").strip()
    kw = title_case(raw)
    return [
        f"Free {kw} Tool for Faster Workflows",
        f"How to Use {kw} Without Wasting Time",
        f"{kw}: Simple Guide and Examples",
        f"Best {kw} Ideas for Beginners",
        f"{kw} Checklist: Avoid Common Mistakes",
        f"Create Better Results With This {kw} Tool",
        f"{kw} Examples You Can Use Today",
        f"Simple {kw} Workflow for Small Teams",
    ]


def meta_description(topic):
    kw = (topic or "online tool").strip()
    return (f"Use this free {kw} tool to save time, create clearer output, and improve your content workflow with simple browser-based automation.")[:155]


def hashtag_ideas(text):
    tags = []
    for w in clean_words(text)[:12]:
        tag = "#" + w.title()
        if tag not in tags:
            tags.append(tag)
    for d in ["#SaaS", "#Productivity", "#Marketing", "#CreatorTools", "#SEO"]:
        if d not in tags:
            tags.append(d)
    return tags[:15]


def word_counter(text):
    words = re.findall(r"\b\w+\b", text or "")
    sentences = len(re.findall(r"[.!?]+", text or "")) or 1
    return {
        "Words": len(words),
        "Characters": len(text or ""),
        "Estimated sentences": sentences,
        "Reading time": f"{max(1, round(len(words) / 200))} min",
    }


def build_utm(form):
    url = form.get("url") or "https://example.com"
    params = {
        "utm_source": form.get("source") or "google",
        "utm_medium": form.get("medium") or "organic",
        "utm_campaign": form.get("campaign") or "main_campaign",
    }
    if form.get("term"):
        params["utm_term"] = form.get("term")
    if form.get("content"):
        params["utm_content"] = form.get("content")
    sep = "&" if "?" in url else "?"
    return url + sep + urllib.parse.urlencode(params)


def keyword_density(text):
    words = clean_words(text)
    total = len(words) or 1
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return [
        {"word": word, "count": count, "density": round(count / total * 100, 2)}
        for word, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:25]
    ]


def content_brief(topic, audience="beginners"):
    topic = (topic or "online tool").strip()
    audience = (audience or "beginners").strip()
    return {
        "titles": title_ideas(topic)[:5],
        "meta": meta_description(topic),
        "outline": [
            f"What is {topic}?",
            f"Why {audience} need it",
            "Step-by-step workflow",
            "Examples and templates",
            "Common mistakes",
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


def youtube_description(topic):
    topic = (topic or "new video").strip()
    tags = " ".join(hashtag_ideas(topic)[:6])
    return f"""{title_case(topic)}

Use this video to learn, relax, plan, or improve your workflow around {topic}. This description is structured to help viewers understand the value quickly.

What you will get:
- Clear explanation of {topic}
- Practical examples you can reuse
- Simple next steps

If this helped you, save the video and subscribe for more useful tools and workflows.

{tags}"""


def faq_questions(topic):
    topic = (topic or "this tool").strip()
    return [
        f"What is {topic}?",
        f"How do I use {topic}?",
        f"Who should use {topic}?",
        f"Is {topic} free?",
        f"What mistakes should I avoid with {topic}?",
        f"Can {topic} improve my workflow?",
    ]


def outline(topic):
    topic = (topic or "online tool").strip()
    return [
        f"Introduction to {topic}",
        "Who this is for",
        "Step-by-step workflow",
        "Examples",
        "Common mistakes",
        "Recommended tools",
        "FAQ",
        "Next steps",
    ]


def social_caption(topic):
    topic = (topic or "a useful free tool").strip()
    return f"I built a simple free tool for {topic}. It helps you save time, create cleaner output, and avoid repetitive manual work. Try it, test the result, and improve your workflow today."


def adsense_checklist(topic):
    topic = (topic or "website").strip()
    return [
        f"The {topic} has a clear purpose beyond showing ads.",
        "Every main page contains original helpful content.",
        "Privacy Policy, Terms, Contact, and About pages are available.",
        "Navigation works on desktop and mobile.",
        "Sitemap and robots.txt are accessible.",
        "No fake traffic, paid-to-click, auto-click, or misleading ad placement is used.",
        "Pages load quickly and are readable on mobile.",
        "The site has real users or a realistic acquisition plan.",
    ]


def faq_schema(text):
    pairs = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if "?" in line:
            q, a = line.split("?", 1)
            pairs.append((q.strip() + "?", a.strip() or "Add your answer here."))
    if not pairs:
        pairs = [("What is this page about?", "This page answers common questions about the topic.")]
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def robots_txt(domain):
    domain = (domain or site_domain()).rstrip("/")
    if not domain.startswith("http"):
        domain = "https://" + domain
    return f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n"


def sitemap_xml(urls_text):
    urls = [u.strip() for u in (urls_text or "").splitlines() if u.strip()]
    if not urls:
        urls = [site_domain() + "/"]
    today = datetime.utcnow().date().isoformat()
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    return f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n{body}\n</urlset>"


def compute_tool(slug, form):
    text = form.get("text") or form.get("topic") or form.get("keyword") or ""
    if slug == "title-generator":
        return {"type": "list", "value": title_ideas(text)}
    if slug == "meta-description":
        return {"type": "text", "value": meta_description(text)}
    if slug == "hashtag-generator":
        return {"type": "tags", "value": hashtag_ideas(text)}
    if slug == "word-counter":
        return {"type": "metrics", "value": word_counter(text)}
    if slug == "utm-builder":
        return {"type": "text", "value": build_utm(form)}
    if slug == "keyword-density-checker":
        return {"type": "table", "value": keyword_density(text)}
    if slug == "slug-generator":
        return {"type": "text", "value": slugify(text)}
    if slug == "content-brief-generator":
        return {"type": "brief", "value": content_brief(form.get("topic") or text, form.get("audience") or "beginners")}
    if slug == "youtube-description-generator":
        return {"type": "text", "value": youtube_description(text)}
    if slug == "faq-generator":
        return {"type": "list", "value": faq_questions(text)}
    if slug == "blog-outline-generator":
        return {"type": "list", "value": outline(text)}
    if slug == "social-caption-generator":
        return {"type": "text", "value": social_caption(text)}
    if slug == "adsense-checklist-generator":
        return {"type": "checklist", "value": adsense_checklist(text)}
    if slug == "faq-schema-generator":
        return {"type": "code", "value": faq_schema(text)}
    if slug == "robots-txt-generator":
        return {"type": "code", "value": robots_txt(text)}
    if slug == "sitemap-url-builder":
        return {"type": "code", "value": sitemap_xml(text)}
    return {"type": "text", "value": "Tool not found."}


def tool_by_slug(slug):
    return next((t for t in TOOLS if t["slug"] == slug), None)


def related_tools(slug, limit=4):
    tool = tool_by_slug(slug)
    if not tool:
        return TOOLS[:limit]
    same = [t for t in TOOLS if t["slug"] != slug and t["category"] == tool["category"]]
    others = [t for t in TOOLS if t["slug"] != slug and t not in same]
    return (same + others)[:limit]


def tool_content(tool):
    name = tool["name"]
    topic = tool["keywords"][0]
    tutorial = [
        f"Open the {name} and enter a specific topic instead of a broad phrase.",
        "Review the generated output and remove anything that does not match your audience or intent.",
        "Use the result as a starting point, then add your own brand voice, examples, and proof.",
        "Publish only after checking that the page or post genuinely helps the reader.",
    ]
    faq = [
        (f"What is {name}?", f"{name} is a browser-based tool that helps with {tool['summary'].lower()}"),
        (f"Who should use {name}?", f"This tool is useful for {tool['intent']} who need faster workflows without complicated software."),
        ("Can I copy the result directly?", "Use the result as a draft. Edit it with your own context, examples, and judgment before publishing."),
        ("Is this tool free?", "Yes. The starter version is free and runs in the browser."),
        ("How can I get better output?", "Use a specific input, mention the audience, and avoid one-word prompts."),
    ]
    return {"tutorial": tutorial, "faq": faq, "topic": topic}


def generate_article_from_keyword(keyword, index=0):
    keyword = (keyword or "online tool").strip()
    title = title_ideas(keyword)[index % len(title_ideas(keyword))]
    slug = slugify(keyword)
    description = meta_description(keyword)
    main_tool = TOOLS[index % len(TOOLS)]
    sections = [
        {
            "heading": f"Why {keyword} matters",
            "paragraphs": [
                f"People search for {keyword} because they want a faster way to complete a specific task. A strong page should solve that task immediately, then explain the workflow clearly.",
                "The best tool pages are not just input boxes. They include examples, common mistakes, and next steps so visitors understand how to use the output correctly.",
            ],
        },
        {
            "heading": "Step-by-step workflow",
            "paragraphs": [
                "Start with a narrow input that describes the audience, platform, and desired result.",
                "Generate several outputs, compare them, and keep the version that is clearest for the user intent.",
                "Edit the final result manually. Add real examples, product details, and proof that only you can provide.",
            ],
        },
        {
            "heading": "Example input and output",
            "paragraphs": [
                f"Example input: {main_tool['example_input']}",
                f"Example output: {main_tool['example_output']}",
            ],
        },
        {
            "heading": "Common mistakes",
            "paragraphs": [
                "Do not publish generic output without review. Thin, repetitive pages usually do not build trust.",
                "Avoid copying competitor text. Use competitor pages only to understand search intent, missing features, and content gaps.",
            ],
        },
    ]
    faq = [
        (f"Is {keyword} free to use?", "The starter tool is free. Advanced features can be added later when users request them."),
        (f"Can {keyword} help SEO?", "It can support the workflow, but rankings depend on usefulness, originality, technical quality, and real user value."),
        ("Should I use AI output without editing?", "No. AI or template output should be reviewed, improved, and made specific before publishing."),
        ("What should I do after generating output?", "Test the result with a real page, post, or campaign, then improve it based on user feedback."),
    ]
    return {
        "slug": slug,
        "title": title,
        "keyword": keyword,
        "description": description,
        "tool_slug": main_tool["slug"],
        "sections": sections,
        "faq": faq,
    }


def all_articles():
    articles = []
    for i, tool in enumerate(TOOLS):
        articles.append(generate_article_from_keyword(tool["keywords"][0], i))
    for i, keyword in enumerate(EXTRA_KEYWORDS, start=len(articles)):
        article = generate_article_from_keyword(keyword, i)
        if not any(a["slug"] == article["slug"] for a in articles):
            articles.append(article)
    return articles


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.title = ""
        self.meta_description = ""
        self.headings = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"title", "h1", "h2", "h3"}:
            self.current = tag
        if tag == "meta" and attrs.get("name", "").lower() == "description":
            self.meta_description = attrs.get("content", "")[:240]

    def handle_endtag(self, tag):
        if tag == self.current:
            self.current = None

    def handle_data(self, data):
        text = " ".join(data.split())
        if not text or not self.current:
            return
        if self.current == "title" and not self.title:
            self.title = text[:160]
        elif self.current in {"h1", "h2", "h3"}:
            self.headings.append({"tag": self.current, "text": text[:180]})


def allowed_by_robots(url, user_agent="ADSENSE_SAAS_AUTO_ResearchBot"):
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return False


def scrape_reference(url, user_agent="ADSENSE_SAAS_AUTO_ResearchBot"):
    if not allowed_by_robots(url, user_agent=user_agent):
        return {"url": url, "ok": False, "error": "Blocked or unknown by robots.txt"}
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            content_type = res.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return {"url": url, "ok": False, "error": f"Not HTML: {content_type}"}
            html = res.read(300000).decode("utf-8", errors="ignore")
        parser = HeadingParser()
        parser.feed(html)
        return {"url": url, "ok": True, "title": parser.title, "meta_description": parser.meta_description, "headings": parser.headings[:30]}
    except Exception as exc:
        return {"url": url, "ok": False, "error": str(exc)}


def gap_ideas_from_references(refs):
    words = []
    for ref in refs:
        if not ref.get("ok"):
            continue
        words.extend(clean_words(ref.get("title", "")))
        words.extend(clean_words(ref.get("meta_description", "")))
        for h in ref.get("headings", []):
            words.extend(clean_words(h.get("text", "")))
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    top = [w for w, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20]]
    ideas = []
    for word in top[:10]:
        ideas.append(f"Add a practical example about {word}.")
    ideas.extend([
        "Add a comparison table that explains when to use each related tool.",
        "Add a real before-after example from your own workflow.",
        "Add FAQ answers based on questions from users or communities.",
    ])
    return ideas[:12]
