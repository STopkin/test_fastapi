from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base, database


class PostManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

    async def create_post(self, author_id: int, title: str):
        from .author import Author
        if await Author.objects.find_by_id(author_id):
            return await database.fetch_one(self.table.insert().values(author_id=author_id, title=title).
                                            returning(self.table.c.id))
        return None


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("Author", back_populates="posts")
    objects: PostManager = None


Post.objects = PostManager(model_cls=Post)
