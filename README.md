# دليل ملفات المشروع

| الملف | الوظيفة |
|-------|---------|
| `main.py` | نقطة دخول التطبيق، يسجل كل الـ routers ويشغل FastAPI |
| `core/config.py` | كل الـ environment variables (DB, JWT, Daily.co) عبر Pydantic Settings |
| `core/database.py` | إعداد SQLAlchemy engine والـ session factory + `get_db` dependency |
| `core/base_models.py` | الـ Base class مع UUID و created_at و updated_at، ترث منه كل الـ models |
| `core/security.py` | hash/verify password + إنشاء وقراءة JWT tokens |
| `core/events/__init__.py` | يحول المجلد لـ Python package |
| `core/events/dispatcher.py` | نظام الإشارات: subscribe و emit، يفصل الـ features عن بعض |
| `core/events/handlers.py` | يسجل كل الـ listeners في مكان واحد (مستورد مرة واحدة في main.py) |
| `features/identity/__init__.py` | يحول المجلد لـ Python package |
| `features/identity/models.py` | جدول Users و Profiles في قاعدة البيانات |
| `features/identity/schemas.py` | Pydantic schemas للـ request والـ response (Register, Login, Token) |
| `features/identity/service.py` | Business logic: تسجيل مستخدم، تسجيل دخول، جلب بروفايل |
| `features/identity/router.py` | FastAPI endpoints: POST /register، POST /login، GET /users/{id} |
| `features/meetings/__init__.py` | يحول المجلد لـ Python package |
| `features/meetings/models.py` | جدول Meetings مع daily_room_url و nda_required |
| `features/meetings/schemas.py` | Pydantic schemas: MeetingCreate و MeetingResponse |
| `features/meetings/service.py` | Business logic: إنشاء meeting، استدعاء Daily.co، التحقق من الحد الأقصى 3 rooms |
| `features/meetings/router.py` | FastAPI endpoints: POST /meetings، GET /meetings/{id}، GET /meetings/{id}/token |
| `features/collaboration/__init__.py` | يحول المجلد لـ Python package |
| `features/collaboration/service.py` | إدارة الـ WebSocket connections وحفظ الرسائل in-memory |
| `features/collaboration/router.py` | WebSocket endpoint: WS /chat/{room_id} + GET /chat/{room_id}/history |
| `integrations/__init__.py` | يحول المجلد لـ Python package |
| `integrations/daily_service.py` | Adapter لـ Daily.co API: create_room، get_token، delete_room |
| `common/__init__.py` | يحول المجلد لـ Python package |
| `common/exceptions.py` | Custom exceptions: NotFoundError، UnauthorizedError، ForbiddenError + FastAPI handlers |
| `tests/features/test_identity.py` | Unit tests لـ register و login |
| `tests/features/test_meetings.py` | Unit tests لإنشاء meeting والتحقق من الـ constraints |
| `tests/integrations/test_daily.py` | Unit tests لـ Daily.co adapter مع mocking |