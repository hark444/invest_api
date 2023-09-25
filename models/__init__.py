from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import settings


engine = create_engine(settings.DATABASE.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SessionLocal = scoped_session(session)
Base = declarative_base()

redis = Redis(host=settings.DATABASE.REDIS_HOST, port=settings.DATABASE.REDIS_PORT, db=2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
