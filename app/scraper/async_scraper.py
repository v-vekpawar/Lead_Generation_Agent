import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright

PAGE_TIMEOUT = 30000
WAIT_AFTER_LOAD = 2000
TEXT_TIMEOUT = 10000

async def scrape_single_page(browser, url):
    page = None

    result = {
        "url": url,
        "status": "failed",
        "title": None,
        "html": None,
        "text": None,
        "links": [],
        "error": None,
    }

    try:
        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            )
        )

        await page.goto(url, timeout=PAGE_TIMEOUT, wait_until="domcontentloaded",)
        await page.wait_for_timeout(WAIT_AFTER_LOAD)

        result["title"] = await page.title()
        result["html"] = await page.content()

        body = page.locator("body")
        result["text"] = await body.inner_text(timeout=TEXT_TIMEOUT)

        hrefs = await page.locator("a").evaluate_all(
            """
            elements => elements.map(e => e.href)
            """
        )

        clean_links = []
        for link in hrefs:
            if not link:
                continue
            clean_links.append(urljoin(url, link))

        result["links"] = list(dict.fromkeys(clean_links))
        result["status"] = "success"

    except Exception as e:
        result["error"] = str(e)

    finally:
        if page is not None:
            await page.close()

    return result


async def scrape_websites(urls, concurrency=5,):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        semaphore = asyncio.Semaphore(concurrency        )

        async def worker(url):
            async with semaphore:
                return await scrape_single_page(browser, url,)

        tasks = [worker(url) for url in urls]

        results = await asyncio.gather(*tasks)

        await browser.close()

    return results

async def scrape_website(url: str):
    results = await scrape_websites([url])
    return results[0]