import json
import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv(".env")


def get_quotes(page_url):
    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(page_url, wait_until="domcontentloaded")
        print(f'Visiting {page_url}')

        page.wait_for_selector("span[class='text']")
        quotes = page.locator(".quote").all()
        next_page_btn_visible = True

        while next_page_btn_visible:
            print("Starting scrapping the page...")
            next_page_btn_selector = page.locator("a[href^='/js-delayed/page/']", has_text="Next ")
            for i, elem in enumerate(quotes):
                quote_data = {}
                text = page.locator(".text").nth(i).text_content()
                text = text.strip('“').strip('”')
                quote_data["text"] = text
                by = page.locator(".author").nth(i).text_content()
                quote_data["by"] = by

                tags_string = page.locator(".tags").nth(i).inner_text()
                tags = tags_string.replace("Tags: ", "").split()
                quote_data["tags"] = tags

                results.append(quote_data)

            next_page_btn_selector.click()
            page.wait_for_load_state("domcontentloaded")

            if next_page_btn_selector.is_hidden():
                next_page_btn_visible = False

        browser.close()

    with open("output.json", "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    url = os.environ.get("INPUT_URL")
    get_quotes(url)
