#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

TOOLS = [
    ("SEO Title Generator", "title-generator", "youtube title generator", "Generate better title ideas for videos, blogs, and landing pages."),
    ("Meta Description Generator", "meta-description", "meta description generator", "Create concise search snippets for webpages."),
    ("Hashtag Generator", "hashtag-generator", "hashtag generator", "Generate relevant hashtag ideas from captions or topics."),
    ("Word Counter", "word-counter", "word counter", "Count words, characters, and estimated reading time."),
    ("UTM Builder", "utm-builder", "UTM builder", "Build trackable campaign URLs."),
    ("Keyword Density Checker", "keyword-density-checker", "keyword density checker", "Check repeated words in SEO drafts."),
    ("Slug Generator", "slug-generator", "slug generator", "Create clean URL slugs from titles."),
    ("Content Brief Generator", "content-brief-generator", "content brief generator", "Build a simple article outline and FAQ plan."),
    ("YouTube Description Generator", "youtube-description-generator", "youtube description generator", "Generate YouTube description drafts."),
    ("FAQ Generator", "faq-generator", "faq generator", "Generate helpful FAQ ideas."),
    ("Blog Outline Generator", "blog-outline-generator", "blog outline generator", "Generate blog outlines."),
    ("Social Caption Generator", "social-caption-generator", "social caption generator", "Generate social captions."),
    ("AdSense Readiness Checklist", "adsense-readiness-checklist", "adsense readiness checklist", "Check site readiness."),
    ("FAQ Schema JSON-LD Generator", "faq-schema-generator", "faq schema generator", "Generate FAQ schema JSON-LD."),
    ("Robots.txt Generator", "robots-generator", "robots txt generator", "Generate robots.txt."),
    ("Sitemap URL Builder", "sitemap-url-builder", "sitemap url builder", "Generate sitemap XML."),
]

def tutorial(name, keyword):
    return [
        f"{name} membantu menyelesaikan pekerjaan kecil yang sering diulang oleh creator, writer, dan marketer.",
        f"Masukkan topik utama seperti '{keyword}', lalu gunakan hasilnya sebagai draft awal.",
        "Pilih hasil yang paling akurat, edit sesuai konteks brand, lalu gunakan pada halaman atau konten Anda.",
        "Untuk hasil terbaik, tambahkan contoh nyata, manfaat yang jelas, dan hindari klaim berlebihan.",
    ]

def examples(keyword):
    return {"input": keyword, "output": [f"Free {keyword.title()} Tool for Faster Workflows", f"How to Use a {keyword.title()} in Minutes", f"Best {keyword.title()} Examples for Beginners"]}

def faq(name, keyword):
    return [
        {"q": f"What is {name}?", "a": f"{name} is a simple browser-based tool for working with {keyword} tasks faster."},
        {"q": "Is this tool free?", "a": "Yes. The starter version is free to use and can be expanded with premium features later."},
        {"q": "Can I use the output directly?", "a": "Use the output as a draft. Review it manually so it matches your content, audience, and intent."},
        {"q": "How can this page attract organic users?", "a": "It targets a specific long-tail problem, provides a useful tool, and includes tutorial, examples, and FAQ."},
    ]

def article_for_tool(name, slug, keyword, desc):
    return {
        "title": f"{name}: Practical Guide and Examples",
        "slug": f"{slug}-guide",
        "keyword": keyword,
        "description": desc,
        "sections": [
            f"{name} is useful when users need a fast answer without opening a complicated dashboard.",
            "The best tool pages are not empty generators. They explain the workflow, show examples, and help users choose the right output.",
            "Before publishing, add original screenshots, real use cases, and short notes from your own testing.",
            "After the site is online, check Search Console to see which queries bring impressions and improve the page based on that data.",
        ],
        "faq": faq(name, keyword),
    }

def main():
    tools = []
    articles = []
    calendar = [["day", "keyword", "page_type", "title", "target_url"]]
    for i, (name, slug, keyword, desc) in enumerate(TOOLS, start=1):
        item = {
            "name": name,
            "slug": slug,
            "keyword": keyword,
            "description": desc,
            "tutorial": tutorial(name, keyword),
            "example": examples(keyword),
            "faq": faq(name, keyword),
            "internal_links": ["/tools/title-generator", "/tools/meta-description", "/tools/word-counter", "/guides"],
        }
        tools.append(item)
        art = article_for_tool(name, slug, keyword, desc)
        articles.append(art)
        calendar.append([i, keyword, "tool-guide", art["title"], f"/tools/{slug}"])
    (OUT / "tools.json").write_text(json.dumps(tools, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "articles.json").write_text(json.dumps(articles, indent=2, ensure_ascii=False), encoding="utf-8")
    with (OUT / "content_calendar.csv").open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(calendar)
    print("Generated:")
    print(OUT / "tools.json")
    print(OUT / "articles.json")
    print(OUT / "content_calendar.csv")
    print("Done at", datetime.now().isoformat(timespec="seconds"))

if __name__ == "__main__":
    main()
