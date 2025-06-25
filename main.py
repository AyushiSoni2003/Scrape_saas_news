import asyncio
from scraper import Scraper
from processor import DataProcessor
from models import SessionLocal, init_db, DatabaseManager

async def main():
    # Step 1: Scrape data using Scraper class
    scraper = Scraper()
    scraped_data = await scraper.scrape_all()

    if scraped_data:
        print(f"\nProcessing {len(scraped_data)} articles...\n")

        # Step 2: Process data using DataProcessor class
        processor = DataProcessor()
        processed_data = processor.clean_data(scraped_data)  # Returns a DataFrame

        # Step 3: Convert DataFrame to list of dicts
        processed_dicts = processed_data.to_dict(orient="records")

        for item in processed_dicts[:5]:
            print(item)

        # Step 4: Initialize DB, save articles and update statistics
        init_db()
        db = SessionLocal()
        try:
            # Filter duplicates manually if needed
            seen_urls = set()
            unique_articles = []
            for article in processed_dicts:
                if article["url"] not in seen_urls:
                    unique_articles.append(article)
                    seen_urls.add(article["url"])

            # Use DatabaseManager class
            db_manager = DatabaseManager(db)
            db_manager.save_articles(unique_articles)
            print("\n Articles saved to the database.")

            print("\n Updating category statistics...")
            db_manager.update_statistics()
            print("Data saved and statistics updated successfully.")
        finally:
            db.close()

if __name__ == "__main__":
    asyncio.run(main())
