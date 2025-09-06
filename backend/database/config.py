from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_engine = "postgresql"
db_host = "localhost:5432"
db_user = "admin"
db_password = "password"
db_name = "aigile"

full_url = f"{db_engine}://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(full_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables that extend Base if they don't exist"""
    Base.metadata.create_all(bind=engine)


# Create tables on module import
# create_tables()

print(get_db())
