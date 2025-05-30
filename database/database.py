from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5437/pomodoro")
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session


