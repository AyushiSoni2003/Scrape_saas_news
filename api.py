from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Article, ArticleStatistics, SessionLocal, init_db , DatabaseManager
from pydantic import BaseModel
from datetime import datetime
from scraper import Scraper
from processor import DataProcessor

app = FastAPI(title="SaaS News API")

# --- Pydantic Schemas ---
class ArticleSchema(BaseModel):
    id: int
    headline: str
    url: str
    publication_date: datetime
    category: str
    sentiment: str

    class Config:
        orm_mode = True

class ArticleCreateSchema(BaseModel):
    headline: str
    url: str
    publication_date: datetime
    category: str
    sentiment: Optional[str] = "neutral" # Optional in case manual POST

class StatsSchema(BaseModel):
    category: str
    count: int

    class Config:
        orm_mode = True

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Initialize DB ---
init_db()

# --- API Endpoints ---

# 1. GET /articles
@app.get("/articles", response_model=List[ArticleSchema])
def get_articles(
    category: Optional[str] = Query(None),
    date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if category:
        query = query.filter(Article.category == category)
    if date:
        query = query.filter(Article.publication_date >= date)
    articles = query.all()
    return articles

# 2. GET /article/{article_id}
@app.get("/article/{article_id}", response_model=ArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# 3. POST /articles
@app.post("/articles", response_model=ArticleSchema)
def create_article(article: ArticleCreateSchema, db: Session = Depends(get_db)):
    new_article = Article(**article.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# 4. GET /article-statistics
@app.get("/article-statistics", response_model=List[StatsSchema])
def get_statistics(db: Session = Depends(get_db)):
    stats = db.query(ArticleStatistics).all()
    return stats

@app.post("/scrape")
async def scrape_and_store(db: Session = Depends(get_db)):
    scraper = Scraper()
    raw_data = await scraper.scrape_all()

    if not raw_data:
        raise HTTPException(status_code=500, detail="No data scraped")

    processor = DataProcessor()
    df = processor.clean_data(raw_data)
    articles = df.to_dict(orient="records")

    manager = DatabaseManager(db)
    manager.save_articles(articles)
    manager.update_statistics()

    return {"message": "Scraping complete", "article_count": len(articles)}