import asyncio

import browser
import browser.test
import injection
from config import CONFIG, context_data

BROWSER_CONFIG = CONFIG["browser"]

if __name__ == "__main__":

    async def main():
        """
        Main method to test the IPTV authentication.
        """
        await browser.process(
            injector=injection.injector,
            start_url=BROWSER_CONFIG["start_url"],
            end_url=BROWSER_CONFIG["end_url"],
            args=BROWSER_CONFIG["args"],
            headers=BROWSER_CONFIG["headers"],
            headless=False,
        )
        context_data["Channel"] = sorted(
            context_data["Channel"], key=lambda x: x["user_id"]
        )

    asyncio.run(main())
