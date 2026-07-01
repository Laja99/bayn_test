# ─────────────────────────────────────────────
# Dockerfile — Beyn Identity Service
# ─────────────────────────────────────────────
#
# بناء الصورة:
#   docker build -t beyn-identity .
#
# تشغيل محلي:
#   docker run -p 8000:8000 --env-file .env beyn-identity
#
# ─────────────────────────────────────────────

# المرحلة 1: تثبيت الـ dependencies
# نستخدم image منفصلة للبناء حتى لا تدخل أدوات البناء في الصورة النهائية
FROM python:3.12-slim AS builder

WORKDIR /app

# نثبت build tools اللي تحتاجها بعض المكتبات (مثل bcrypt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# نخزن الـ requirements في طبقة منفصلة
# Docker يعيد استخدام هذه الطبقة إذا لم يتغير requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─────────────────────────────────────────────
# المرحلة 2: الصورة النهائية
# ─────────────────────────────────────────────

FROM python:3.12-slim

WORKDIR /app

# نثبت libpq للاتصال بـ PostgreSQL في runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# ننسخ الـ packages المثبتة من مرحلة البناء
COPY --from=builder /install /usr/local

# ننسخ الكود
COPY src/ ./src/

# مستخدم غير root للأمان — لا نشغل التطبيق كـ root
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# الـ port الداخلي
EXPOSE 8000

# healthcheck — Docker يتحقق أن التطبيق يعمل كل 30 ثانية
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

# أمر التشغيل
# --workers 1 في Docker عشان نتحكم بالـ scaling من الخارج (Kubernetes/ECS)
# --host 0.0.0.0 عشان يقبل connections من خارج الـ container
CMD ["uvicorn", "src.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]
