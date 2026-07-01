"""
إعداد قاعدة البيانات — SQLAlchemy async.

يحتوي هذا الملف على:
- engine: الاتصال الأساسي بقاعدة البيانات
- AsyncSession: الجلسة اللي تستخدمها كل الـ queries
- Base: الكلاس الأساسي لكل الـ models
- get_db: الـ dependency اللي يوفر session لكل request وينهيها بعده
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

# ─────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────

# engine = نقطة الاتصال الواحدة بقاعدة البيانات
# pool_pre_ping=True = يتحقق أن الاتصال حي قبل كل استخدام
# echo=settings.DEBUG = يطبع الـ SQL queries في بيئة التطوير فقط
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# SessionLocal = factory لإنشاء sessions
# expire_on_commit=False = لا تبطل الـ objects بعد commit
#   (مهم في async لأننا قد نحتاج نقرأ البيانات بعد الـ commit)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ─────────────────────────────────────────────
# Base Model
# ─────────────────────────────────────────────

class Base(DeclarativeBase):
    """
    الكلاس الأساسي لكل جداول قاعدة البيانات.
    كل model يرث منه عشان SQLAlchemy يتعرف عليه.
    """
    pass


# ─────────────────────────────────────────────
# Dependency
# ─────────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency — يوفر database session لكل request.

    yield = نفتح الـ session، ننفذ الـ route، ثم نغلق الـ session
    بغض النظر إذا نجح الـ route أو رفع exception.

    الاستخدام في الـ router:
        @router.get("/")
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
