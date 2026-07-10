from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = "mysql+pymysql://root:maiphuong@localhost:3306/truck_rental_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def db_session():
    db = SessionLocal()
    try:
        with db.begin():
            yield db
    finally:
        db.close()


if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
