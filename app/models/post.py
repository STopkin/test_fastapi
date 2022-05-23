from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base, database


class PostManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

#    def get_total_count(self):
#        query = self.table.count()
#        return await database.fetch_val(query)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("Author", back_populates="posts")
    objects: PostManager = None


Post.objects = PostManager(model_cls=Post)
