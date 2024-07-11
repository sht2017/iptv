from playwright.async_api import (
    Browser,
    Page,
    async_playwright,
)

from . import remote_injector


async def process(
    injector: remote_injector.Injector,
    start_url: str,
    end_url: str,
    args: list | None = None,
    headers: dict | None = None,
    headless: bool = True,
):
    async with async_playwright() as playwright:
        browser: Browser = await playwright.chromium.launch(
            args=args, headless=headless
        )
        page: Page = await browser.new_page()

        await remote_injector.inject(page, injector)
        if headers:
            await page.set_extra_http_headers(headers)

        await page.goto(start_url)

        await page.wait_for_url(url=end_url, wait_until="domcontentloaded")
        await browser.close()
