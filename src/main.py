from playwright.sync_api import sync_playwright, Browser, BrowserContext
from settings import PROXY, USER_AGENT, CHROMIUM_WS
from parser import WbPageParser


def _create_new_context(
    browser: Browser,
    proxy: str,
    user_agent: str
) -> BrowserContext:
    """Create new browser context

    Args:
        browser: launched browser
        proxy: proxy server url
        user_agent: User Agent

    Returns:
        BrowserContext: new browser context
    """
    return browser.new_context(
        viewport={"width": 2560, "height": 1920},
        user_agent=user_agent,
        proxy={"server": proxy},
        java_script_enabled=True,
        ignore_https_errors=True,
        extra_http_headers={
            "Accept": "*/*",
            "Accept-Language": "ru-RU, ru;q=0.9, en-US;q=0.8, en;q=0.7, fr;q=0.6",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/"
        }
    ) 

def crawl(url: str, proxy: str, user_agent: str, ws: str) -> list:
    """Parse WB subcategory page and extract filters

    Args:
        url: WB subcategory page url
        proxy: proxy server url
        user_agent: User Agent
        ws: chromium web socket

    Returns:
        list: _description_
    """
    with sync_playwright() as pw:
        browser = pw.chromium.connect(ws)
        context = _create_new_context(browser, proxy, user_agent)
        page = context.new_page()
        try:
            page.goto(url)
            # waite filters side bar
            page.wait_for_selector(
                '.xsubject',
                timeout=10000
            )
            content = page.content()

            # save page html
            file = open('main.html', 'w')
            file.write(content)
            file.close()

            crawler = WbPageParser()
            # extract filters from page html
            items = crawler.parse(url, content)
            context.close()
            browser.close()
            return items
        except Exception:
            context.close()
            browser.close()
            raise


if __name__ == "__main__":
    url = "https://www.wildberries.ru/catalog/dom-i-dacha/zdorove/optika?sort=popular&page=1"
    items = crawl(
        url=url,
        proxy=PROXY,
        user_agent=USER_AGENT,
        ws=CHROMIUM_WS
    )
    print(items)
