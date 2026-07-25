import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin

async def scrape_single_page(browser, url):
    result = {
        "url": url,
        "status": "failed",
        "title": None,
        "text": None,
        "links":[],
        "error": None
    }

    try:
        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        )

        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)


        result["title"] = await page.title()

        body = page.locator("body")
        result["text"] = await body.inner_text(timeout=10000)

        hrefs = await page.locator("a").evaluate_all(
            """
            elements => elements.map(
                e => e.href
            )
            """
        )
        clean_links = []
        for link in hrefs:
            if link:
                absolute_url = urljoin(url,link)
                clean_links.append(absolute_url)

        result["links"] = list(set(clean_links))

        result["status"] = "success"

        await page.close()

    except Exception as e:
        result["error"] = str(e)

    return result



async def scrape_websites(urls, concurrency=5):
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        semaphore = asyncio.Semaphore(concurrency)

        async def worker(url):
            async with semaphore:
                return await scrape_single_page(browser,url)

        tasks = [worker(url) for url in urls]

        results = await asyncio.gather(*tasks)

        await browser.close()

    return results