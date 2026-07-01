"""
إعدادات التطبيق — تُقرأ من environment variables أو ملف .env

لا تُكتب أي secrets هنا — هذا الملف يحدد أسماء المتغيرات وأنواعها فقط.
القيم الفعلية تكون في .env (للتطوير) أو في secrets manager (للإنتاج).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ── التطبيق ──────────────────────────────
    APP_NAME: str = "Beyn"
    DEBUG: bool = False

    # ── قاعدة البيانات ────────────────────────
    DATABASE_URL: str

    # ── JWT ──────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    # مدة صلاحية الـ access token بالدقائق — قصير عمداً لأمان أكثر
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    # مدة صلاحية الـ refresh token بالأيام — طويل للراحة
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Authentica (OTP) ──────────────────────
    # AUTHENTICA_BASE_URL = الـ URL الأساسي لـ API الخاص بحسابك في Authentica
    # AUTHENTICA_API_KEY  = مفتاح الـ API من لوحة Authentica
    AUTHENTICA_BASE_URL: str | None = None
    AUTHENTICA_API_KEY: str | None = None

    # ── Cloudflare R2 (صور المستخدمين) ────────
    # R2_ACCOUNT_ID      = رقم حسابك في Cloudflare
    # R2_ACCESS_KEY_ID   = من R2 → Manage R2 API Tokens
    # R2_SECRET_ACCESS_KEY = نفس المصدر
    # R2_BUCKET_NAME     = اسم الـ bucket اللي أنشأته
    # R2_PUBLIC_URL      = الـ domain العام للـ bucket (من إعدادات الـ bucket)
    R2_ACCOUNT_ID: str | None = None
    R2_ACCESS_KEY_ID: str | None = None
    R2_SECRET_ACCESS_KEY: str | None = None
    R2_BUCKET_NAME: str | None = None
    R2_PUBLIC_URL: str | None = None

    # ── Cal.com ───────────────────────────────
    CALCOM_API_KEY: str | None = None
    CALCOM_CLIENT_ID: str | None = None
    CALCOM_CLIENT_SECRET: str | None = None

    # ── SMTP (الإيميل) ─────────────────────────
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM_ADDRESS: str | None = None

    # ── Redis (Celery tasks) ──────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # يتجاهل أي متغيرات غير معرّفة هنا بدل ما يرفع خطأ
    )


# instance واحد مشترك في كل التطبيق
# الاستيراد: from src.core.config import settings
settings = Settings()
