from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime
from textblob import TextBlob

# --- SQLAlchemy Base & Engine Setup ---
Base = declarative_base()
DATABASE_URL = "sqlite:///./articles.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Models ---
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    publication_date = Column(DateTime)
    category = Column(String)
    sentiment = Column(String, default="neutral")

class ArticleStatistics(Base):
    __tablename__ = 'article_statistics'
    id = Column(Integer, primary_key=True)
    category = Column(String, unique=True)
    count = Column(Integer)

# --- Database Manager Class ---
class DatabaseManager:
    def __init__(self, db: Session):
        self.db = db

    def analyze_sentiment(self, text: str) -> str:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"

    def save_articles(self, articles: list[dict]):
        for item in articles:
            existing = self.db.query(Article).filter_by(url=item["url"]).first()
            if existing:
                continue  # Skip duplicate

            sentiment = item.get("sentiment") or self.analyze_sentiment(item["headline"])

            article = Article(
                headline=item["headline"],
                url=item["url"],
                publication_date=item.get("publication_date", datetime.utcnow()),
                category=item.get("category", "Unknown"),
                sentiment=sentiment
            )
            self.db.add(article)

        self.db.commit()

    def update_statistics(self):
        self.db.query(ArticleStatistics).delete()
        counts = self.db.query(Article.category, func.count().label("count")).group_by(Article.category).all()
        for category, count in counts:
            stat = ArticleStatistics(category=category, count=count)
            self.db.add(stat)
        self.db.commit()

# --- Utility ---
def init_db():
    Base.metadata.create_all(bind=engine)
