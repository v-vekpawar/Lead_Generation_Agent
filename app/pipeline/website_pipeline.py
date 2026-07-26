import asyncio

from app.scraper.async_scraper import scrape_websites

from app.extractor.email_extractor import extract_emails
from app.extractor.phone_extractor import extract_phones
from app.extractor.link_classifier import classify_links
from app.extractor.social_extractor import extract_social_links
from app.extractor.company_name_extractor import extract_company_name

from app.pipeline.lead_builder import build_lead

async def process_scraped_website(scraped_result: dict, source_url: str) -> dict:
    """Process one scraped website into a Lead"""

    website = scraped_result["url"]

    if scraped_result["status"] != "success":
        return {
            "company_name": "",
            "website": website,
            "emails": [],
            "phones": [],
            "socials": {
                "linkedin": [],
                "facebook": [],
                "instagram": [],
                "twitter": [],
                "youtube": [],
                "github": [],
                "medium": [],
                "telegram": [],
                "discord": [],
            },
            "source_url": source_url,
            "status": "failed",
            "error": scraped_result.get("error"),
        }

    try:
        text = scraped_result["text"]
        html = scraped_result["html"]
        links = scraped_result["links"]

        emails = extract_emails(text, links)

        phones = extract_phones(text)

        classified_links = classify_links(links)

        socials = extract_social_links(classified_links["social_links"])

        company_name = extract_company_name(html, website)

        lead = build_lead(
            website=website,
            source_url=source_url,
            company_name=company_name,
            emails=emails,
            phones=phones,
            socials=socials,
        )

        return lead

    except Exception as e:

        return {
            "company_name": "",
            "website": website,
            "emails": [],
            "phones": [],
            "socials": {
                "linkedin": [],
                "facebook": [],
                "instagram": [],
                "twitter": [],
                "youtube": [],
                "github": [],
                "medium": [],
                "telegram": [],
                "discord": [],
            },
            "source_url": source_url,
            "status": "failed",
            "error": str(e),
        }

async def process_websites(websites: list[str], source_url: str, concurrency: int=5,) -> list[dict]:
    """
    Complete pipeline.

    Websites
        ↓
    Concurrent Scraping
        ↓
    Concurrent Extraction
        ↓
    Leads
    """

    if not websites:
        return []

    scraped_results = await scrape_websites(websites, concurrency=concurrency)

    tasks = [process_scraped_website(scraped, source_url) for scraped in scraped_results]

    leads = await asyncio.gather(*tasks)

    return leads