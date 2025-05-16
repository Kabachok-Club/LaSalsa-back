from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME  # noqa: E402

# 👇 Настройка подключения (проверь путь!)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 👇 Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)

# 👇 Асинхронный сессионный фабрикат
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# 👇 Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# 👇 Зависимость для FastAPI (yield, а не return!)
async def get_async_session():
    async with async_session_maker() as session:
        yield session
