import asyncio
import json

from app.search.search import search_companies
from app.utils.url_filters import filter_company_urls
from app.classifier.url_classifier import classify_results
from app.pipeline.website_pipeline import process_websites

MAX_SEARCH_RESULT = 30
SCRAPER_CONCURRENCY = 5

async def main():
    query = input("Enter your lead search query: ").strip()
    print("\nSearching...\n")
    search_results = search_companies(query, max_results=MAX_SEARCH_RESULT)
    filtered_results = filter_company_urls(search_results)
    classified_results = classify_results(filtered_results)

    company_results = [result for result in classified_results if result["type"]=="company"]

    if not company_results:
        print("No company websites found.")
        return

    websites = [result["url"] for result in company_results]
    print(f"Found {len(websites)} company websites.")
    print("Scraping websites...")

    leads = await process_websites(websites=websites, search_query=query, source_url=None, concurrency=SCRAPER_CONCURRENCY,)
    print(f"\nGenerated {len(leads)} leads\n")

    print(json.dumps(leads,indent=4,ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())