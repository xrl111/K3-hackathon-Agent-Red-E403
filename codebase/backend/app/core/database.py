from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings
import app.models  # noqa: F401

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)


def create_db_and_tables() -> None:
    """Create all SQLite tables registered in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)



def get_session() -> Generator[Session, None, None]:
    """Dependency to inject database session into router."""
    with Session(engine) as session:
        yield session

