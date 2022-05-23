import databases
from sqlalchemy.ext.declarative import declarative_base

from settings import settings

database = databases.Database(settings.database_url)

Base = declarative_base()