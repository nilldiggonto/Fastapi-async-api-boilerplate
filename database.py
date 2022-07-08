from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = "postgresql://postgres:nill1234@localhost/blogdb"

# engine = create_async_engine(DATABASE_URL, future=True, echo=True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
            return getattr(self._session, name)

    def init(self):
            self._engine = create_async_engine("postgresql+asyncpg://postgres:nill1234@localhost:5432/blogdb",future=True,echo=True,)
            self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

db=AsyncDatabaseSession()



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # DATABASE_URL = "sqlite:///sql.db"
# POSTGRESQL_DATABASE_URL = "postgresql://postgres:nill1234@localhost:5432/fastdb_eco"
# engine = create_engine(
#     POSTGRESQL_DATABASE_URL#,connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base = declarative_base()
# https://ahmed-nafies.medium.com/tutorial-fastapi-with-sqlalchemy-async-orm-and-alembic-2fa68102f82d