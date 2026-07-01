"""
نظام الترجمة (i18n) لـ identity feature.

الآلية:
1. المستخدم يرسل Accept-Language header: "ar" أو "en"
2. get_locale() يقرأ الـ header ويحدد اللغة
3. t() تجيب الرسالة المترجمة من ملفات JSON

ملفات الترجمة:
    locales/ar.json  ← الرسائل بالعربي
    locales/en.json  ← الرسائل بالإنجليزي

طريقة الاستخدام في الـ service:
    from src.features.identity.i18n import t
    raise ValidationError(t("otp.email_already_verified", locale))

طريقة الاستخدام في الـ router:
    from src.features.identity.i18n import get_locale
    locale: str = Depends(get_locale)
"""

import json
from functools import lru_cache
from pathlib import Path

from fastapi import Header

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

SUPPORTED_LOCALES = {"ar", "en"}
DEFAULT_LOCALE = "en"

# مسار مجلد ملفات الترجمة
LOCALES_DIR = Path(__file__).parent / "locales"


# ─────────────────────────────────────────────
# Loader
# ─────────────────────────────────────────────

@lru_cache(maxsize=None)
def _load_locale(locale: str) -> dict:
    """
    يحمّل ملف الترجمة من الـ disk.

    @lru_cache = يحمّل كل ملف مرة واحدة فقط ويخزنه في الذاكرة.
    هذا مهم لأن قراءة الـ disk بطيئة ولا نريدها في كل request.

    إذا الملف غير موجود → يرجع dict فارغ (يرجع الـ key كـ fallback).
    """
    locale_file = LOCALES_DIR / f"{locale}.json"

    if not locale_file.exists():
        return {}

    with open(locale_file, encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────
# Core Translation Function
# ─────────────────────────────────────────────

def t(key: str, locale: str = DEFAULT_LOCALE) -> str:
    """
    يرجع الرسالة المترجمة للـ key المحدد.

    key = مسار منقط في ملف JSON
    مثال: "otp.email_already_verified" → translations["otp"]["email_already_verified"]

    Fallback:
    1. إذا اللغة غير مدعومة → يستخدم الإنجليزي
    2. إذا الـ key غير موجود في اللغة المطلوبة → يحاول الإنجليزي
    3. إذا غير موجود في الإنجليزي → يرجع الـ key نفسه (fallback أخير)

    مثال:
        t("auth.invalid_credentials", "ar") → "الإيميل أو كلمة المرور غير صحيحة"
        t("auth.invalid_credentials", "en") → "Invalid email or password"
        t("auth.invalid_credentials", "fr") → "Invalid email or password"  ← fallback للإنجليزي
    """
    # نتأكد أن اللغة مدعومة
    if locale not in SUPPORTED_LOCALES:
        locale = DEFAULT_LOCALE

    # نجلب ملف الترجمة
    translations = _load_locale(locale)

    # نتنقل في الـ nested dict بالـ key المنقط
    # مثال: "otp.email_already_verified" → translations["otp"]["email_already_verified"]
    value = _get_nested(translations, key)

    # إذا لم يوجد في اللغة المطلوبة → نحاول الإنجليزي
    if value is None and locale != DEFAULT_LOCALE:
        fallback_translations = _load_locale(DEFAULT_LOCALE)
        value = _get_nested(fallback_translations, key)

    # إذا لم يوجد أصلاً → نرجع الـ key نفسه (لسهولة debugging)
    return value if value is not None else key


def _get_nested(data: dict, key: str) -> str | None:
    """
    يتنقل في dict متداخل بمسار منقط.

    مثال:
        data = {"otp": {"sent_email": "OTP sent"}}
        key  = "otp.sent_email"
        → "OTP sent"
    """
    keys = key.split(".")
    current = data

    for k in keys:
        if not isinstance(current, dict) or k not in current:
            return None
        current = current[k]

    return current if isinstance(current, str) else None


# ─────────────────────────────────────────────
# FastAPI Dependency
# ─────────────────────────────────────────────

def get_locale(
    accept_language: str = Header(default="en", alias="Accept-Language"),
) -> str:
    """
    FastAPI Depends() — يقرأ Accept-Language header ويرجع اللغة المناسبة.

    يدعم الصيغ التالية:
        Accept-Language: ar
        Accept-Language: ar-SA         ← يأخذ "ar" فقط
        Accept-Language: ar,en;q=0.9   ← يأخذ أول لغة

    إذا اللغة غير مدعومة → يرجع الإنجليزي (DEFAULT_LOCALE).

    الاستخدام في الـ router:
        @router.post("/signup")
        async def signup(
            payload: UserSignup,
            locale: str = Depends(get_locale),
            db: AsyncSession = Depends(get_db),
        ):
            return await service.create_user(db, payload, locale)
    """
    if not accept_language:
        return DEFAULT_LOCALE

    # نأخذ أول لغة فقط (قبل الفاصلة)
    # مثال: "ar,en;q=0.9" → "ar"
    primary = accept_language.split(",")[0].strip()

    # نأخذ الـ language code فقط (قبل الـ dash)
    # مثال: "ar-SA" → "ar"
    lang_code = primary.split("-")[0].strip().lower()

    # نتحقق أن اللغة مدعومة
    return lang_code if lang_code in SUPPORTED_LOCALES else DEFAULT_LOCALE
