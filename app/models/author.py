from sqlalchemy import Column, Table, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base, database


class AuthorManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

#    def get_total_count(self):
#        query = self.table.count()
#        return await database.fetch_val(query)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")

    objects: AuthorManager = None


Author.objects = AuthorManager(model_cls=Author)