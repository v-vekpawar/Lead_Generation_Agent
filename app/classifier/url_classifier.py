from urllib.parse import urlparse

DIRECTORY_DOMAINS = [
    "clutch.co",
    "goodfirms.co",
    "designrush.com",
    "f6s.com",
    "topdevelopers.co",
    "ensun.io",
    "superbcompanies.com",
    "digitalagencynetwork.com"
]

BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "linkedin.com",
    "medium.com",
    "twitter.com",
    "x.com"
]

AD_PATTERNS = [
    "aclick",
    "googleadservices",
    "doubleclick",
    "adservice"
]

DIRECTORY_KEYWORDS = [
    "top",
    "best",
    "companies",
    "agencies",
    "directory",
    "ranking",
    "reviews",
    "list"
]

ARTICLE_KEYWORDS = [
    "blog",
    "article",
    "guide",
    "top-",
    "best-",
    "ranking",
    "2025",
    "2026"
]

COMPANY_KEYWORDS = [
    "about",
    "services",
    "contact",
    "solutions",
    "agency",
    "studio"
]

def get_domain(url: str):
    domain = urlparse(url).netloc.lower()
    return domain.replace("www.", "")

def calculate_scores(result: dict):
    url = result.get("url", "").lower()
    title = result.get("title", "").lower()
    domain = get_domain(url)

    scores = {
        "company": 0,
        "directory": 0,
        "article": 0,
        "irrelevant": 0
    }

    # Ads / tracking URLs
    for pattern in AD_PATTERNS:
        if pattern in url:
            scores["irrelevant"] += 20

    # Blocked domains
    for blocked in BLOCKED_DOMAINS:
        if blocked in domain:
            scores["irrelevant"] += 20

    # Directory domains
    for directory in DIRECTORY_DOMAINS:
        if directory in domain:
            scores["directory"] += 15

    combined_text = f"{title} {url}"

    # Article signals
    for keyword in ARTICLE_KEYWORDS:
        if keyword in combined_text:
            scores["article"] += 2

    # Blog path is strong evidence
    if "/blog/" in url:
        scores["article"] += 5

    if "/article/" in url:
        scores["article"] += 5

    # Directory signals
    for keyword in DIRECTORY_KEYWORDS:
        if keyword in combined_text:
            scores["directory"] += 1

    # Company signals
    for keyword in COMPANY_KEYWORDS:
        if keyword in title:
            scores["company"] += 2

    if "company" in url and "companies" not in url:
        scores["company"] += 3

    if "agency" in url and "agencies" not in url:
        scores["company"] += 3

    return scores

def classify_url(result: dict):
    scores = calculate_scores(result)
    category = max(
        scores,
        key=scores.get
    )

    highest_score = scores[category]
    total_score = sum(scores.values())

    if total_score == 0:
        return {
            **result,
            "type": "unknown",
            "confidence": 0.0,
            "scores": scores
        }
    
    confidence = round(
        highest_score / total_score,
        2
    )

    if confidence < 0.5:
        category = "unknown"

    return {
        **result,
        "type": category,
        "confidence": confidence,
        "scores": scores
    }

def classify_results(results):
    return [
        classify_url(item)
        for item in results
    ]