import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.growth import (
    hashtag_ideas, title_ideas, meta_description, slugify, keyword_density,
    word_counter, build_utm, content_brief, youtube_description, faq_generator,
    blog_outline, social_caption, adsense_checklist, faq_schema, robots_txt, sitemap_xml
)

def must(condition, message):
    if not condition:
        print("[FAIL]", message)
        sys.exit(1)
    print("[OK]", message)

tags = hashtag_ideas("asmr rain")
print("asmr rain =>", " ".join(tags))
must(len(tags) >= 5, "hashtag generator returns at least 5 tags")
must("#asmr" in tags, "hashtag keeps #asmr")
must("#rain" in tags, "hashtag keeps #rain")
must("#smr" not in tags and "#ain" not in tags, "no broken #smr/#ain")
must(any(t in tags for t in ["#asmrrain", "#rainasmr", "#rainsounds"]), "adds topic-aware ASMR/rain hashtags")

empty_tags = hashtag_ideas("")
print("empty input =>", " ".join(empty_tags))
must(len(empty_tags) >= 5, "hashtag fallback returns at least 5 tags")

titles = title_ideas("asmr rain")
print("titles sample =>", titles[0])
must(len(titles) >= 5, "title generator returns multiple titles")
must("ASMR Rain" in titles[0], "title generator preserves ASMR acronym")

meta = meta_description("utm builder")
print("meta sample =>", meta)
must("UTM Builder" in meta, "meta generator preserves UTM acronym")
must(len(meta) <= 155, "meta description length is safe")

wc = word_counter("hello world. this is a test.")
print("word count =>", wc)
must(wc["words"] == 6, "word counter counts words")

utm = build_utm("https://example.com", "google", "organic", "test")
print("utm =>", utm)
must("utm_source=google" in utm and "utm_campaign=test" in utm, "UTM builder valid")

density = keyword_density("seo seo tools for creators")
print("density sample =>", density)
must(density["total_words"] >= 3 and density["rows"], "keyword density runs")

slug = slugify("Best Free SEO Tools!")
print("slug sample =>", slug)
must(slug == "best-free-seo-tools", "slug generator valid")

brief = content_brief("youtube title generator", "creators")
must("titles" in brief and "outline" in brief and "faqs" in brief, "content brief valid")

yt = youtube_description("asmr rain", "sleep relaxing")
must("description" in yt and len(yt["hashtags"]) >= 5, "YouTube description valid")

faq = faq_generator("UTM builder", "marketers")
must(len(faq) >= 4 and "q" in faq[0] and "a" in faq[0], "FAQ generator valid")

outline = blog_outline("keyword density checker")
must(len(outline) >= 5 and outline[0].startswith("H1:"), "blog outline valid")

social = social_caption("free SEO tools", "TikTok")
must("hook" in social and len(social["hashtags"]) >= 5, "social caption valid")

check = adsense_checklist("https://example.com", 20, True, True, True, True)
must(check["score"] >= 5, "AdSense checklist valid")

schema = faq_schema([{"q": "What is this?", "a": "A test answer."}])
must('"FAQPage"' in schema and '"Question"' in schema, "FAQ schema valid")

robots = robots_txt("https://example.com")
must("Sitemap:" in robots, "robots.txt generator valid")

sitemap = sitemap_xml(["https://example.com/"])
must("<urlset" in sitemap and "<loc>https://example.com/</loc>" in sitemap, "sitemap builder valid")

print("TOOLS QUALITY CHECK PASSED")
