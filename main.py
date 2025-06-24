import asyncio
from scraper import main as scrape_main
from processor import cleaned_data  # assuming you’ll process the data here
from models import SessionLocal , init_db, save_articles, update_statistics

async def main():
    # Step 1: Scrape data
    scraped_data = await scrape_main()  # this runs the async main from scraper.py

    if scraped_data:
        print(f"\nProcessing {len(scraped_data)} articles...\n")
        processed_data = cleaned_data(scraped_data)

        #  Convert DataFrame to list of dicts before saving
        processed_dicts = processed_data.to_dict(orient="records")

        for item in processed_data[:5]:
            print(item)

        # Step 2: Initialize the database and save to database
        init_db()
        db = SessionLocal()
        try:
            save_articles(db, processed_dicts)
            print("\nArticles saved to the database.\n")
            
            print("Updating category statistics...")
            update_statistics(db)

            print("Data saved and statistics updated successfully.")
            
        finally:
            db.close()

if __name__ == "__main__":
    asyncio.run(main())
