# api/migrate_db.py

from sqlalchemy import create_engine

# from api.models.task import Base
import api.models.task as task_models

Base = task_models.Base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()