import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.thesaasnews.com"
CATEGORY_URL = f"{BASE_URL}/news"


# Step 1: Get All Category Links (Except Last One)
async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_series_links(session):
    html = await fetch_html(session, CATEGORY_URL)
    soup = BeautifulSoup(html, 'html.parser')
    nav_section = soup.find("div", class_="secondary-navigation")
    if not nav_section:
        return []

    list_items = nav_section.find_all("li")[:-1]  # exclude last
    return [li.find("a")['href'] for li in list_items if li.find("a")]


# Step 2: Get All Paginated Article Links from One Category
async def get_all_articles_from_category(session, cat_url):
    article_links = []
    next_page = cat_url

    while next_page:
        print(f"Scraping page: {next_page}")
        html = await fetch_html(session, next_page)
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


# Step 3: Extract Article Data
async def fetch_article_data(session, url,semaphore):
    async with semaphore:
        
        try:
            html = await fetch_html(session, url)
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


# Step 4: Main Async Routine
async def main():
    semaphore = asyncio.Semaphore(50)  # Controls concurrency level

    async with aiohttp.ClientSession() as session:
        category_paths = await get_series_links(session)
        print(f"Found {len(category_paths)} categories")

        # Create concurrent tasks for all category pages
        category_tasks = [
            get_all_articles_from_category(session, path if path.startswith("http") else BASE_URL + path)
            for path in category_paths
        ]

        # Run all category tasks in parallel
        all_article_lists = await asyncio.gather(*category_tasks)

        # Flatten list of lists
        all_article_urls = [url for sublist in all_article_lists for url in sublist]

        print(f"\nTotal articles to fetch: {len(all_article_urls)}\n")

        # Fetch all articles concurrently
        article_tasks = [fetch_article_data(session, url, semaphore) for url in all_article_urls]
        all_data = await asyncio.gather(*article_tasks)

        # Cleaned result
        cleaned_data = [d for d in all_data if d is not None]
        print(f"Fetched {len(cleaned_data)} article records.")

        for record in cleaned_data[:5]:  # show sample
            print(record)

        return cleaned_data


# Run
if __name__ == "__main__":
    scraped_data = asyncio.run(main())
