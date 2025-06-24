import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import Base, get_async_session
from app.dependencies import verify_firebase_token
from app.main import app

print("== ROUTES ==")
for route in app.routes:
    print(route.path)

@pytest.fixture(scope="function")
async def client():
    TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_async_session():
        async with session_maker() as session:
            yield session
    
    async def override_verify_firebase_token():
        user = {'uid': 'test_user_123'}
        yield user

    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[verify_firebase_token] = override_verify_firebase_token

    # Очистка БД — до теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # сам клиент
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Очистка БД — после теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
