import asyncio
from scraper import main as scrape_main
from processor import cleaned_data  # assuming you’ll process the data here

async def main():
    scraped_data = await scrape_main()  # this runs the async main from scraper.py

    if scraped_data:
        print(f"\nProcessing {len(scraped_data)} articles...\n")
        processed_data = cleaned_data(scraped_data)

        # You can add saving logic here if needed
        # e.g., save_to_sqlite(processed_data) or save_to_csv(processed_data)

        for item in processed_data[:5]:
            print(item)

if __name__ == "__main__":
    asyncio.run(main())
