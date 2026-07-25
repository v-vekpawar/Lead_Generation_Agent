import re

SOCIAL_DOMAINS = [
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com"
]

CONTACT_KEYWORDS = [
    "contact",
    "about",
    "reach",
    "connect"
]

def classify_links(links):
    result = {
        "social_links": [],
        "contact_links": [],
        "other_links": []
    }

    for link in links:
        link_lower = link.lower()

        if any(domain in link_lower for domain in SOCIAL_DOMAINS):
            result["social_links"].append(link)

        elif any(word in link_lower for word in CONTACT_KEYWORDS):
            result["contact_links"].append(link)

        else:
            result["other_links"].append(link)

    return result