# Portfolio Backend

## Umumiy ma'lumot
Portfolio Backend — bu shaxsiy portfolioni boshqarish uchun ishlab chiqilgan Django REST API. Loyiha sertifikatlar, ko'nikmalar va bajarilgan loyihalar haqidagi ma'lumotlarni saqlaydi hamda ularni frontend yoki tashqi servislar uchun HTTP orqali beradi. API REST paradigmasiga tayanadi va ruxsatni cheklashsiz (AllowAny) faqat o'qish (GET) amallarini taklif etadi.

## Texnologiyalar va bog'liqliklar
- `Python 3.12+`
- `Django 5.1.3`
- `Django REST Framework 3.15.2`
- `PostgreSQL` (asosiy ma'lumotlar bazasi)
- `django-environ` — konfiguratsiya boshqaruvi
- `django-cors-headers` — CORS sozlamalari
- `drf-yasg` — Swagger/Redoc dokumentatsiyasi
- `gunicorn` — ishlab chiqarish serveri

Barcha asosiy kutubxonalar `requirements.txt` faylida keltirilgan.

## Katalog tuzilmasi
```
Portfolio_backend/
├── portfolio/               # Django manba kodi
│   ├── manage.py
│   ├── main/                # Asosiy ilova (sertifikat, skill, portfolio)
│   └── portfolio/           # Loyihaning global sozlamalari
├── requirements.txt
└── Procfile                 # Gunicorn uchun ishga tushirish skripti
```

`main` ilovasi barcha API va ma'lumot modellarini o'z ichiga oladi. Statik va media fayllar mos ravishda `static/`, `staticfiles/` va `media/` kataloglariga yoziladi.

## O'rnatish va ishga tushirish
1. Reponi klonlang va loyihaning ildiz katalogiga o'ting.
2. Virtual muhit yarating va faollashtiring:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Bog'liqliklarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
4. `.env` faylini yarating (quyidagi bo'limga qarang).
5. Migratsiyalarni ishga tushiring:
   ```bash
   python portfolio/manage.py migrate
   ```
6. Mahalliy serverni yoqing:
   ```bash
   python portfolio/manage.py runserver
   ```
   Server odatda `http://127.0.0.1:8000/` manzilida ishlaydi.

### Ishlab chiqarish
Railway yoki o'xshash platformada `Procfile` `gunicorn --chdir portfolio ...` buyrug'i orqali deploy qilinadi. `PORT` muhiti o'zgaruvchisi platforma tomonidan taqdim etiladi.

## Muhit o'zgaruvchilari (.env)
| O'zgaruvchi             | Tavsif                                      | Standart |
|-------------------------|---------------------------------------------|----------|
| `SECRET_KEY`            | Django maxfiy kaliti                        | demo qiymat |
| `DEBUG`                 | `True/False` — debug rejimi                 | `True` |
| `POSTGRES_DB`           | Ma'lumotlar bazasi nomi                     | `portfolio` |
| `POSTGRES_USER`         | Ma'lumotlar bazasi foydalanuvchisi          | `postgres` |
| `POSTGRES_PASSWORD`     | Ma'lumotlar bazasi paroli                   | `postgres` |
| `POSTGRES_HOST`         | Ma'lumotlar bazasi hosti                    | `localhost` |
| `POSTGRES_PORT`         | Ma'lumotlar bazasi porti                    | `5432` |
| `CSRF_TRUSTED_ORIGINS`  | Vergul bilan ajratilgan ruxsat berilgan hostlar | `https://api.jaloliddindev.uz` |
| `CORS_ALLOWED_ORIGINS`  | Vergul bilan ajratilgan frontend manzillar  | `http://localhost:3000`, `https://jaloliddindev.uz`, ... |

`django-environ` bu qiymatlarni avtomatik o'qiydi. QA yoki ishlab chiqarish davrida SSL talabi (`sslmode=require`) yo'q qilinishi kerak bo'lsa, mos ravishda ma'lumotlar bazasi sozlamalarini moslashtiring.

## Statik va media fayllar
- `STATIC_URL = /static/`
- `MEDIA_URL = /media/`

Gunicorn + WhiteNoise static fayllarni xizmat qiladi. Media fayllar foydalanuvchi yuklagan fayllar uchun `media/` ichida saqlanadi. Model maydonlari orqali qaytarilgan URL'lar `MEDIA_URL` bilan boshlanadi (masalan, `/media/portfolio_images/<uuid>/<filename>`). Frontend to'liq URL`ni qurish uchun domenni qo'shishi kerak.

## API manzillari
Asosiy prefiks: `http://<HOST>/main/` (masalan, lokalda `http://127.0.0.1:8000/main/`). Barcha endpointlar `GET` so'rovlarini qabul qiladi va ro'yxat ko'rinishida ma'lumot qaytaradi.

### 1. Sertifikatlar
- **URL:** `GET /main/serticates/`
- **Tavsif:** Sertifikatlar ro'yxatini qaytaradi.
- **Namunaviy javob:**
  ```json
  [
    {
      "id": 1,
      "img": "http://127.0.0.1:8000/media/sertificate_images/5f8c6f30-9fc9-43d4-8cd7-3297df/example.png"
    }
  ]
  ```

### 2. Ko'nikmalar (Skills)
- **URL:** `GET /main/skills/`
- **Tavsif:** Ko'nikmalar va ularning tavsiflari.
- **Namunaviy javob:**
  ```json
  [
    {
      "id": 3,
      "title": "Backend Development",
      "description": "Django va FastAPI bilan REST xizmatlari",
      "image": "http://127.0.0.1:8000/media/skill_images/8a1d8e90-5f51-4e3b-8c53-a930/icon.png"
    }
  ]
  ```

### 3. Portfolio loyihalari
- **URL:** `GET /main/portfolios/`
- **Tavsif:** Loyiha kartalari, havolalar va asosiy xususiyatlar.
- **Namunaviy javob:**
  ```json
  [
    {
      "id": 5,
      "title": "Portfolio Platformasi",
      "description": "Frontend va backend integratsiyasi bilan shaxsiy sayit",
      "features": [
        "Mahalliy va ishlab chiqarish muhitiga moslashuvchan",
        "To'liq REST API",
        "CORS va Swagger integratsiyasi"
      ],
      "image": "http://127.0.0.1:8000/media/portfolio_images/3ad9c54d-1ef1-4fc3-8483-6ad0/cover.png",
      "github_link": "https://github.com/username/portfolio",
      "in_link": null,
      "tg_link": "https://t.me/username",
      "linkedin_link": "https://www.linkedin.com/in/username/",
      "link": "https://jaloliddindev.uz"
    }
  ]
  ```

> **Eslatma:** `features` maydoni `models.JSONField` orqali saqlanadi. Amaliyotda bu ko'pincha stringlar ro'yxati yoki obyektlar ro'yxati ko'rinishida bo'ladi. Frontend ushbu ma'lumotni mos ravishda parse qilishi kerak.

## Ma'lumotlar modellari
- **Sertificate**
  - `id`: butun son (autoincrement)
  - `img`: `ImageField`, sertifikat rasmi (ixtiyoriy)
- **Skill**
  - `id`: butun son
  - `title`: 255 belgigacha bo'lgan matn
  - `description`: matn, batafsil izoh
  - `image`: `ImageField`, ko'nikma ikonasi
- **Portfolio**
  - `id`: butun son
  - `title`, `description`: loyihaning nomi va izohi
  - `features`: JSON (masalan, stringlar ro'yxati)
  - `image`: loyihaning muqova rasmi
  - `github_link`, `in_link`, `tg_link`, `linkedin_link`, `link`: tashqi havolalar (`URLField`)

Model maydonlari `blank=True, null=True` sifatida yaratilgan, shu sababli barcha maydonlar ixtiyoriydir. Admin panel orqali ma'lumot kiritishda ularning bo'sh qoldirilishi xato bermaydi.

## Swagger va hujjatlar
- Swagger UI: `GET /swagger/`
- Swagger JSON: `GET /swagger.json` yoki `GET /swagger.yaml`
- ReDoc: `GET /redoc/`

Swagger sahifasi `drf-yasg` yordamida avtomatik generatsiya qilinadi va API ni test qilish hamda client kutubxonalarga eksport qilishni osonlashtiradi.

## Xavfsizlik va CORS
- `CORS_ALLOWED_ORIGINS` orqali frontend domenlari belgilangan.
- Agar `*` ko'rsatilsa, `CORS_ALLOW_ALL_ORIGINS = True` bo'ladi.
- `CSRF_TRUSTED_ORIGINS` orqali foydalanuvchi interfeysi domenlari qo'shiladi.
- REST API hozircha autentifikatsiya talab qilmaydi (`AllowAny`). Kelajakda `rest_framework_simplejwt` kutubxonasi yordamida JWT autentifikatsiyasini qo'shish mumkin (kutubxona `requirements.txt` da mavjud).

## Test va keyingi qadamlarga oid eslatmalar
- `main/tests.py` hozir bo'sh; API uchun DRF testlarini qo'shish tavsiya etiladi.
- Media fayllarini boshqarish uchun CDN yoki bulut (masalan, S3) integratsiyasi `django-storages` orqali amalga oshirilishi mumkin.
- CI/CD jarayonida migratsiyalarni avtomatik ishga tushirish va `collectstatic` buyrug'ini qo'shish lozim.

## Deploy bo'yicha tezkor ro'yxat
- Ma'lumotlar bazasi uchun PostgreSQL instansiyasini tayyorlash (`PORT`, `HOST`, `USER`, `PASSWORD`).
- Muhit o'zgaruvchilarini platformaga kiritish.
- `python manage.py migrate` va zarur bo'lsa `createsuperuser`.
- Statik fayllarni yig'ish: `python manage.py collectstatic --noinput`.
- `gunicorn --chdir portfolio portfolio.wsgi:application` buyrug'i orqali servisni ishga tushirish.

Shu bilan backend API to'liq ishlashga tayyor bo'ladi va frontend tomonidan bemalol iste'mol qilinadi.
