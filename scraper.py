import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.thesaasnews.com"
CATEGORY_URL = f"{BASE_URL}/news"


class Scraper:
    def __init__(self, concurrency=50):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.session = None

    async def fetch_html(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    async def get_series_links(self):
        html = await self.fetch_html(CATEGORY_URL)
        soup = BeautifulSoup(html, 'html.parser')
        nav_section = soup.find("div", class_="secondary-navigation")
        if not nav_section:
            return []

        list_items = nav_section.find_all("li")[:-1]  # exclude last
        return [li.find("a")['href'] for li in list_items if li.find("a")]

    async def get_all_articles_from_category(self, cat_url):
        article_links = []
        next_page = cat_url

        while next_page:
            print(f"Scraping page: {next_page}")
            html = await self.fetch_html(next_page)
            soup = BeautifulSoup(html, 'html.parser')
            tags = soup.select("a.blog-listing-snippet")

            for tag in tags:
                href = tag.get("href")
                if href:
                    full_url = BASE_URL + href if href.startswith("/") else href
                    article_links.append(full_url)

            next_btn = soup.find("a", class_="page-next")
            if next_btn and next_btn.get("href"):
                next_page = BASE_URL + next_btn.get("href")
            else:
                next_page = None

        return article_links

    async def fetch_article_data(self, url):
        async with self.semaphore:
            try:
                html = await self.fetch_html(url)
                soup = BeautifulSoup(html, 'html.parser')

                article = {
                    "url": url,
                    "headline": soup.find("title").text.strip() if soup.find("title") else "",
                    "funding_date": "",
                    "company": "",
                    "round": "",
                    "software_category": ""
                }

                content_div = soup.find("div", class_="rich-text")
                if content_div:
                    text = content_div.get_text(" ", strip=True)

                    def search(pattern):
                        match = re.search(pattern, text, re.IGNORECASE)
                        return match.group(1).strip() if match else ""

                    article["funding_date"] = search(r"Funding Date[:\s]+([A-Za-z]+ \d{4})")
                    article["company"] = search(r"Company[:\s]+([\w\s\-\.,&]+)")
                    article["round"] = search(r"Round[:\s]+(Series [A-Fa-f])")
                    article["software_category"] = search(r"Software Category[:\s]+([\w\s/]+)")

                return article

            except Exception as e:
                print(f"Error scraping {url}: {e}")
            return None

    async def scrape_all(self):
        async with aiohttp.ClientSession() as self.session:
            category_paths = await self.get_series_links()
            print(f"Found {len(category_paths)} categories")

            category_tasks = [
                self.get_all_articles_from_category(
                    path if path.startswith("http") else BASE_URL + path
                )
                for path in category_paths
            ]
            all_article_lists = await asyncio.gather(*category_tasks)
            all_article_urls = [url for sublist in all_article_lists for url in sublist]
            print(f"\nTotal articles to fetch: {len(all_article_urls)}\n")

            article_tasks = [self.fetch_article_data(url) for url in all_article_urls]
            all_data = await asyncio.gather(*article_tasks)

            cleaned_data = [d for d in all_data if d is not None]
            print(f"Fetched {len(cleaned_data)} article records.")
            return cleaned_data
