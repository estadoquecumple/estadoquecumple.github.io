from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.shared.config import settings

engine = create_engine(settings().database_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def session_scope():
    db = Session()
    try:
        yield db
    finally:
        db.close()
