import os

BRAND = {
    "name": os.getenv("BRAND_NAME", os.getenv("SITE_NAME", "ToolBoost Studio")),
    "short": os.getenv("BRAND_SHORT", "ToolBoost"),
    "tagline": os.getenv("BRAND_TAGLINE", "Free Creator, SEO, and Marketing Tools"),
    "positioning": os.getenv("BRAND_POSITIONING", "Simple browser tools for creators, writers, marketers, and small businesses."),
    "mission": "Help creators, writers, marketers, and small businesses finish repetitive content and SEO tasks faster with simple browser-based tools.",
    "audience": "creators, SEO writers, social media teams, solo founders, and small businesses",
}

INTERNAL_LINKS = [
    {"label": "Creator Content Pack", "url": "/tools/creator-content-pack"},
    {"label": "Shorts Script Generator", "url": "/tools/shorts-script-generator"},
    {"label": "Thumbnail Text Maker", "url": "/tools/thumbnail-text-maker"},
    {"label": "Content Calendar Generator", "url": "/tools/content-calendar-generator"},
    {"label": "SEO Title Generator", "url": "/tools/title-generator"},
    {"label": "Guides", "url": "/guides"},
]

TOOL_SEEDS = {
    "title-generator": {
        "examples": [
            ("rain sound for sleep", "Best Rain Sound for Sleep: Relaxing Audio for Deep Rest"),
            ("free invoice generator", "Free Invoice Generator for Small Business Owners"),
            ("youtube title ideas", "YouTube Title Ideas That Make Your Videos Clearer"),
            ("keyword density checker", "Keyword Density Checker for Natural SEO Writing"),
        ],
        "faq": [
            ("What makes a good SEO title?", "A good title makes the topic clear, matches search intent, and gives users a reason to click without misleading them."),
            ("Should I use the exact keyword?", "Use the main keyword naturally, preferably near the beginning, but keep the title readable."),
            ("Can I use generated titles directly?", "Use them as draft options, then edit based on the actual page, video, or campaign."),
            ("How many title ideas should I test?", "Generate several options and compare clarity, benefit, and search intent before choosing one."),
        ],
    },
    "meta-description": {
        "examples": [
            ("free SEO tools", "Use free SEO tools to plan titles, descriptions, keywords, and campaign links faster."),
            ("UTM builder", "Build clean UTM links for campaign tracking with a simple browser-based URL builder."),
            ("word counter", "Count words, characters, and reading time for articles, captions, and student writing."),
            ("hashtag generator", "Generate relevant hashtags from a topic or caption for social content planning."),
        ],
        "faq": [
            ("What is a meta description?", "It is a short page summary that can appear as a search snippet and help users decide whether to visit."),
            ("Does it guarantee ranking?", "No. It mainly helps explain the page and may improve the quality of the search snippet."),
            ("How long should it be?", "Keep it concise and useful. Focus on the page benefit, not repeated keywords."),
            ("Should every page have one?", "Yes. Each indexable page should have a unique description that matches its content."),
        ],
    },
    "hashtag-generator": {
        "examples": [
            ("free tools for creators", "#FreeTools #Creators #Productivity #Marketing"),
            ("rain sound sleep video", "#RainSound #SleepMusic #RelaxingAudio #DeepSleep"),
            ("small business SEO tips", "#SmallBusiness #SEOTips #MarketingTools #Growth"),
            ("youtube shorts title ideas", "#YouTubeShorts #CreatorTools #VideoTips #ContentIdeas"),
        ],
        "faq": [
            ("How many hashtags should I use?", "Use only enough to describe the topic, audience, and format clearly."),
            ("Should I use trending hashtags?", "Only use trending hashtags when they are genuinely relevant to the content."),
            ("Do hashtags replace good content?", "No. They help categorization, but the content still needs a strong hook and value."),
            ("Can I reuse the same hashtags?", "You can reuse core niche tags, but adjust them to match each post."),
        ],
    },
    "word-counter": {
        "examples": [
            ("Paste a 900-word article", "Words: 900 | Reading time: about 4-5 minutes"),
            ("Paste a short caption", "Words: 32 | Characters: 190"),
            ("Paste product copy", "Words and characters counted for quick editing"),
            ("Paste FAQ answers", "Estimated reading time and length checked"),
        ],
        "faq": [
            ("Is longer content always better?", "No. The right length depends on the user problem and the completeness of the answer."),
            ("Why count reading time?", "Reading time helps set user expectations and can improve content planning."),
            ("Can I use it for captions?", "Yes. It works for articles, captions, product copy, and student writing."),
            ("Does word count directly improve SEO?", "No. Usefulness, clarity, and completeness matter more than length alone."),
        ],
    },
    "utm-builder": {
        "examples": [
            ("example.com + source google + medium organic", "https://example.com?utm_source=google&utm_medium=organic&utm_campaign=main_campaign"),
            ("landing page + facebook + social + launch", "Campaign URL with consistent UTM naming"),
            ("newsletter campaign", "Trackable URL for email analytics"),
            ("creator bio link campaign", "URL tagged for social profile clicks"),
        ],
        "faq": [
            ("What is a UTM link?", "It is a URL with tracking parameters that helps analytics tools identify traffic sources."),
            ("Should I use UTM on internal links?", "No. UTM is for external campaign links; internal use can break attribution."),
            ("What is the common mistake?", "Inconsistent naming, such as facebook, fb, and Facebook being used for the same source."),
            ("Can small businesses use UTM?", "Yes. UTM links are useful for simple campaigns, newsletters, ads, and social posts."),
        ],
    },
    "keyword-density-checker": {
        "examples": [
            ("Paste SEO article", "Shows repeated words and density percentage"),
            ("Paste landing page copy", "Finds unnatural repetition"),
            ("Paste blog draft", "Checks whether the topic is focused"),
            ("Paste product description", "Identifies overused terms"),
        ],
        "faq": [
            ("What is keyword density?", "It is the percentage of how often a word appears compared with the total counted words."),
            ("Is there an ideal density?", "There is no universal ideal. Focus on natural writing and helpful coverage."),
            ("Can overusing keywords hurt quality?", "Yes. It can make content feel forced and reduce trust."),
            ("How should I use this result?", "Use it as a quality check, then rewrite unnatural repetition with clearer examples."),
        ],
    },
    "slug-generator": {
        "examples": [
            ("Best Free SEO Tools for Small Business", "best-free-seo-tools-for-small-business"),
            ("How to Build UTM Links", "how-to-build-utm-links"),
            ("YouTube Title Ideas for Shorts", "youtube-title-ideas-for-shorts"),
            ("Keyword Density Checker Guide", "keyword-density-checker-guide"),
        ],
        "faq": [
            ("What is a URL slug?", "It is the readable part of a page URL, usually based on the page topic."),
            ("Should slugs be short?", "Yes. Keep them readable, lowercase, and focused on the main topic."),
            ("Can I change a slug later?", "Yes, but use redirects so old links do not break."),
            ("Should I include the full title?", "No. Use the core topic, not every word from the title."),
        ],
    },
    "content-brief-generator": {
        "examples": [
            ("Topic: YouTube title generator", "Titles, meta description, outline, FAQ, and internal links"),
            ("Topic: UTM builder for small business", "Practical article brief for marketers"),
            ("Topic: word counter for students", "Outline and FAQ for search-focused page"),
            ("Topic: hashtag generator", "Content brief for social creator audience"),
        ],
        "faq": [
            ("What is a content brief?", "It is a writing plan that defines title ideas, search intent, outline, FAQ, and supporting links."),
            ("Who should use it?", "Writers, marketers, creators, and site owners who want more focused content."),
            ("Does a brief replace research?", "No. It speeds planning, but you should still add examples, experience, and facts."),
            ("Can it help SEO?", "It helps organize useful content around a clear user problem and intent."),
        ],
    },
}

GENERIC_FAQ = [
    ("Is this tool free?", "Yes. The starter version is free to use and can be expanded with premium features later."),
    ("Can I use the output directly?", "Use the output as a draft. Review it manually so it matches your audience, search intent, and brand voice."),
    ("Who is this tool for?", "It is designed for creators, writers, marketers, founders, and small business owners."),
    ("How can this page attract organic users?", "It targets a specific long-tail problem, provides a useful tool, and includes tutorial, examples, FAQ, and internal links."),
]

def default_examples(tool_name, keyword):
    return [
        (keyword, f"Free {keyword.title()} Tool for Faster Workflows"),
        (f"best {keyword}", f"Best {keyword.title()} Examples for Beginners"),
        (f"how to use {keyword}", f"How to Use {keyword.title()} in Minutes"),
        (f"{keyword} for small business", f"{keyword.title()} for Small Business Workflows"),
    ]

def get_tool_content(slug, tool_name, keyword):
    seed = TOOL_SEEDS.get(slug, {})
    examples = seed.get("examples", default_examples(tool_name, keyword))
    faq = seed.get("faq", GENERIC_FAQ)
    return {
        "tutorial": [
            f"{tool_name} helps users complete a specific workflow quickly without opening a complicated dashboard.",
            f"Start with a clear input such as '{keyword}', review the generated output, and adjust it for your audience.",
            "For better results, use specific inputs, avoid generic wording, and add your own experience before publishing.",
            "This page includes examples, FAQ, and related links so users understand the workflow, not only the form.",
        ],
        "examples": [{"input": i, "output": o} for i, o in examples],
        "faq": [{"q": q, "a": a} for q, a in faq],
        "internal_links": INTERNAL_LINKS,
    }
