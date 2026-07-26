
SOCIAL_TEMPLATE = {
    "linkedin": [],
    "facebook": [],
    "instagram": [],
    "twitter": [],
    "youtube": [],
    "github": [],
    "medium": [],
    "telegram": [],
    "discord": [],
}

def build_lead(*, website: str, search_query: str, source_url: str | None, company_name: str, emails: list[str], phones: list[str], socials: dict,) -> dict:
    """Build a lead object"""

    merged_socials = {platform: socials.get(platform, []).copy() for platform in SOCIAL_TEMPLATE}

    lead = {
        "company_name": company_name,
        "website": website,
        "emails": sorted(set(emails)),
        "phones": sorted(set(phones)),
        "socials": merged_socials,
        "search_query": search_query,
        "source_url": source_url,
        "status": "success",
    }

    return lead