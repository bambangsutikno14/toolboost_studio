import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.growth import (
    TOOLS, CREATOR_TOOL_SLUGS,
    hashtag_ideas, title_ideas, meta_description, slugify, keyword_density,
    word_counter, build_utm, content_brief, youtube_description, faq_generator,
    blog_outline, social_caption, adsense_checklist, faq_schema, robots_txt, sitemap_xml,
    creator_content_pack, shorts_script, thumbnail_text_maker, content_calendar, clip_idea_generator
)

def must(condition, message):
    if not condition:
        print("[FAIL]", message)
        sys.exit(1)
    print("[OK]", message)

must(len(TOOLS) >= 21, "V7 has expanded tool set")
must(TOOLS[0]["slug"] == "creator-content-pack", "Creator Content Pack is flagship tool")
must(all(slug in [t["slug"] for t in TOOLS] for slug in CREATOR_TOOL_SLUGS), "all creator tools registered")

pack = creator_content_pack("asmr rain", "YouTube Shorts", "United States viewers", "relaxing", "growth")
print("content pack titles =>", pack["titles"][:2])
must("titles" in pack and len(pack["titles"]) >= 8, "content pack returns title set")
must("script" in pack and len(pack["script"]["scenes"]) >= 5, "content pack includes short script")
must(len(pack["hashtags"]) >= 8, "content pack includes hashtags")
must(len(pack["upload_checklist"]) >= 6, "content pack includes upload checklist")

script = shorts_script("asmr rain", "YouTube Shorts", "45", "relaxing", "United States viewers")
must(len(script["scenes"]) >= 5 and "caption" in script, "shorts script valid")
must(len(script["hashtags"]) >= 5, "shorts script includes hashtags")

thumb = thumbnail_text_maker("youtube growth for beginners", "YouTube Shorts", "curiosity")
must(len(thumb["variants"]) >= 5 and len(thumb["layout_notes"]) >= 4, "thumbnail text maker valid")

cal = content_calendar("asmr rain", "YouTube Shorts", "7", "beginner creators", "growth")
must(len(cal["days"]) == 7 and "workflow" in cal, "content calendar generates 7 days")

clips = clip_idea_generator("First, choose one idea. Then write a short hook. Next, prepare the caption and hashtags. Finally, upload and track results.", "YouTube Shorts", "creator workflow")
must(len(clips["ideas"]) >= 3 and len(clips["editing_notes"]) >= 4, "clip idea generator valid")

tags = hashtag_ideas("asmr rain")
print("asmr rain =>", " ".join(tags))
must(len(tags) >= 5, "hashtag generator returns at least 5 tags")
must("#asmr" in tags, "hashtag keeps #asmr")
must("#rain" in tags, "hashtag keeps #rain")
must("#smr" not in tags and "#ain" not in tags, "no broken #smr/#ain")
must(any(t in tags for t in ["#asmrrain", "#rainasmr", "#rainsounds"]), "adds topic-aware ASMR/rain hashtags")

titles = title_ideas("asmr rain")
print("titles sample =>", titles[:3])
must(len(titles) >= 10, "title generator returns strong option set")
must("ASMR Rain" in titles[0], "title generator preserves ASMR acronym")
must(all(len(t) <= 68 for t in titles), "titles keep practical search length")

meta = meta_description("utm builder")
print("meta sample =>", meta)
must("UTM Builder" in meta, "meta generator preserves UTM acronym")
must(len(meta) <= 155, "meta description length is safe")

wc = word_counter("hello world. this is a test.")
must(wc["words"] == 6 and "reading_time_minutes" in wc, "word counter counts and estimates time")

utm = build_utm("https://example.com", "Google Ads", "Paid Search", "Test Campaign")
must("utm_source=google_ads" in utm and "utm_campaign=test_campaign" in utm, "UTM builder normalizes campaign naming")

density = keyword_density("seo seo tools for creators")
must(density["total_words"] >= 3 and density["rows"] and "status" in density["rows"][0], "keyword density runs with status")

slug = slugify("Best Free SEO Tools!")
must(slug == "best-free-seo-tools", "slug generator valid")

brief = content_brief("youtube title generator", "creators")
must("titles" in brief and "outline" in brief and "quality_notes" in brief, "content brief valid and quality-aware")

yt = youtube_description("asmr rain", "sleep relaxing")
must("description" in yt and len(yt["hashtags"]) >= 5 and "Key points" in yt["description"], "YouTube description valid")

faq = faq_generator("UTM builder", "marketers")
must(len(faq) >= 5 and "q" in faq[0] and "a" in faq[0], "FAQ generator valid")
must("UTM Builder" in faq[0]["q"], "FAQ generator preserves UTM Builder capitalization")

outline = blog_outline("keyword density checker")
must(len(outline) >= 8 and outline[0].startswith("H1:"), "blog outline valid")

social = social_caption("free SEO tools", "TikTok")
must("hook" in social and len(social["hashtags"]) >= 5, "social caption valid")

check = adsense_checklist("https://example.com", 20, True, True, True, True)
must(check["score"] >= 7, "AdSense checklist valid")

schema = faq_schema([{"q": "What is this?", "a": "A test answer."}])
must('"FAQPage"' in schema and '"Question"' in schema, "FAQ schema valid")

robots = robots_txt("https://example.com")
must("Sitemap:" in robots, "robots.txt generator valid")

sitemap = sitemap_xml(["https://example.com/"])
must("<urlset" in sitemap and "<loc>https://example.com/</loc>" in sitemap, "sitemap builder valid")

print("TOOLS QUALITY CHECK PASSED")
