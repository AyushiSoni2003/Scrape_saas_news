from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, Session , declarative_base
from datetime import datetime

# --- Models ---
Base = declarative_base()

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

# --- Database Setup ---
DATABASE_URL = "sqlite:///./articles.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# --- Save Functions ---
def save_articles(db: Session, articles: list[dict]):
    for item in articles:
        # Create a new Article instance
        article = Article(
            headline=item["headline"],
            url=item["url"],
            publication_date=item.get("publication_date", datetime.utcnow()),
            category=item.get("category", "Unknown"),
            sentiment=item.get("sentiment", "neutral")
        )

        db.merge(article)
    db.commit()

def update_statistics(db: Session):
    counts = db.query(Article.category, func.count().label("count")).group_by(Article.category).all()
    db.query(ArticleStatistics).delete()
    for category, count in counts:
        stat = ArticleStatistics(category=category, count=count)
        db.add(stat)
    db.commit()
