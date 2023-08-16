import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(".env")


def get_quotes(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            # proxy={"server": proxy}
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto(page_url, wait_until="domcontentloaded")
        print(f'visiting {page_url}')
        print(page.title())
        page.wait_for_selector("span[class='text']")
        quotes = page.locator(".quote").all()
        quotes_list = []
        next_page_btn_visible = True
        while next_page_btn_visible:
            next_page_btn_selector = page.locator("a[href^='/js-delayed/page/']", has_text="Next ")
            for i, elem in enumerate(quotes):
                text = page.locator(".text").nth(i).text_content()
                quotes_list.append(text)
                print(text)
                by = page.locator(".author").nth(i)
                print(by.text_content())
                tags = page.locator(".tags").nth(i).all_inner_texts()
                print(tags)
            next_page_btn_selector.click()
            page.wait_for_load_state("domcontentloaded")
            if next_page_btn_selector.is_hidden():
                next_page_btn_visible = False
        browser.close()


if __name__ == "__main__":
    url = os.environ.get("INPUT_URL")
    # proxy_server = os.environ.get("PROXY")
    get_quotes(url)
