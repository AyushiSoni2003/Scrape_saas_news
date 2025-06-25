Logical Flow
#----------------------------------------------------
Scraping (scraper.py)
#------------------------
Uses aiohttp for asynchronous requests and BeautifulSoup for parsing HTML.

Iterates through multiple pages of funding announcements.

Extracts relevant details like headline, URL, date, category, round, and company.

Processing (processor.py)
#---------------------------
Converts raw scraped data to a Pandas DataFrame.

Strips unwanted whitespace, fixes URL formatting, and parses dates.

Categorizes articles into groups like AI/ML, Product Updates, etc.

Performs sentiment analysis on headlines using TextBlob.

Database Storage (models.py)
#--------------------------------
SQLAlchemy models for:

Article: stores each article's metadata.

ArticleStatistics: stores counts of articles by category.

ORM manages interaction with SQLite or other RDBMS.

REST API (api.py)
#------------------------
Built with FastAPI.

Endpoints:

GET /articles: Get all or filtered articles.

GET /article/{id}: Get a specific article.

POST /articles: Add an article (used for testing/manual input).

GET /article-statistics: Get category-wise counts.

Main Controller (main.py)
#----------------------------
Runs the pipeline:

Scrapes → Processes → Stores in DB → Updates statistics

External Dependencies
#----------------------------------------------------
aiohttp - For making asynchronous HTTP requests to scrape multiple pages faster
beautifulsoup4 - Parses HTML to extract required elements from the news pages
fastapi - Serves the REST API endpoints
sqlalchemy - ORM for defining and interacting with database tables
pandas - Data cleaning, transformation, and analysis
textblob - Sentiment analysis of headlines
pydantic - Data validation and serialization in FastAPI
