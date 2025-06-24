from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    publication_date = Column(DateTime)
    category = Column(String)

class ArticleStatistics(Base):
    __tablename__ = 'article_statistics'

    id = Column(Integer, primary_key=True)
    category = Column(String, unique=True)
    count = Column(Integer)
