from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func, select

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("Author", back_populates="posts") 
    
    
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) 
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")
    posts_count = column_property(select(func.count(Post.id)).
        where(Post.author_id==id).
        correlate_except(Post).
        scalar_subquery())
