# SaaS News Scraper API

A Python-based SaaS news scraping system that collects startup funding articles from [TheSaaSNews.com](https://thesaasnews.com), processes and categorizes them, performs sentiment analysis, stores the data in a database, and exposes it via a FastAPI REST API.

---

## Features

- Asynchronous web scraping using `aiohttp` and `BeautifulSoup4`
- Text cleaning and data transformation with `pandas`
- Sentiment analysis with `TextBlob`
- Category grouping
- SQLAlchemy-based SQLite database
- FastAPI-powered RESTful API
- Modular Object-Oriented Architecture

---

## Project Structure

```
SaaS News Scraper/
│
├── scraper.py          # Web scraping logic
├── processor.py        # Data cleaning and transformation
├── models.py           # SQLAlchemy models and DB structure
├── api.py              # FastAPI app with endpoints
├── main.py             # Orchestration script: scrape → process → save
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── documentation.md    # Internal logic documentation
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AyushiSoni2003/Scrape_saas_news.git
cd Scrape_saas_news
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Running the Application

### 1. Run the scraping and data processing pipeline

```bash
python main.py
```

### 2. Start the FastAPI server

```bash
uvicorn api:app --reload
```

Visit the API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

- `GET /articles`: Get all articles or filter by category/date
- `GET /article/{id}`: Get a specific article by ID
- `POST /articles`: Manually add an article (optional)
- `GET /article-statistics`: Get count of articles by category

---

## Dependencies

Key Python packages used:

- `aiohttp` - Async HTTP client
- `beautifulsoup4` - HTML parser
- `pandas` - Data manipulation
- `textblob` - Sentiment analysis
- `sqlalchemy` - ORM for database
- `fastapi` - Web framework for APIs
- `pydantic` - Data validation with FastAPI

---

## Notes

- Default DB is SQLite
- Ensure a stable internet connection during scraping
- Can be extended to scrape more categories or websites

---

## Screenshots

### ✅ Scraping & Processing Output
![scraping-success](https://github.com/user-attachments/assets/18327072-21af-4f23-a851-b96d59a78c16)


### 📊 FastAPI Swagger UI
![swagger-ui](https://github.com/user-attachments/assets/18215754-225a-422d-a5ae-95784c142597)



### 📦 Sample API Response
![api-response](https://github.com/user-attachments/assets/c812fad8-aeee-40c3-9b89-a5bcda0dd934)



## License

MIT License

---

## Author

Ayushi Soni – Built as part of a Python internship assignment.
