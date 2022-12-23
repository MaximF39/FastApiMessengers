from sqlmodel import create_engine, SQLModel, Session

from db.models.type_messenger import type_messenger_migrate
from migrate import create_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},  # for only sqlite check_same_thread
    echo=True
)

def migrate_db():
    with Session(engine) as session:
        type_messenger_migrate(session)
        create_user(session)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
