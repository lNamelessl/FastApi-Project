# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from app import schema
# from app.config import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker,declarative_base
# from app.Database import get_db, Base
# from alembic import command



# SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

# engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


# TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# # Base = declarative_base()

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db
        
#     yield TestClient(app)
        