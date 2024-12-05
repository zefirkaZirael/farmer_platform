from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Farmer(Base):
    __tablename__ = 'farmers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


class Buyers(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Подключение к базе данных
from config import settings
engine = create_engine(settings.DATABASE_URL())

# Создание таблиц
Base.metadata.create_all(engine)
