# Portfolio Backend API

## 1. Umumiy ma'lumot
Portfolio Backend - bu shaxsiy portfolioni boshqarish uchun ishlab chiqilgan REST API. Backend `Django` va `Django REST Framework` asosida qurilgan bo'lib, sertifikatlar, ko'nikmalar va portfoliodagi loyihalar haqidagi ma'lumotlarni o'qish uchun ommaviy (autentifikatsiyasiz) endpointlarni taqdim etadi. API stateless, faqat `GET` so'rovlarini qo'llab-quvvatlaydi va frontend ilovalar tomonidan to'g'ridan-to'g'ri iste'mol qilinadi.

## 2. Arxitektura va modullar
- `main` ilovasi modellarning, serializerlarning va `ListAPIView` generik klasslari orqali qurilgan endpointlarning markazi hisoblanadi.
- Media fayllar Cloudinary'da saqlanadi (`django-cloudinary-storage`), fayl nomlari `helpers.SaveMediaFile` orqali UUID bilan ajratiladi.
- Swagger/Redoc hujjatlari `drf-yasg` yordamida servis qilinadi.
- `django-cors-headers` CORS siyosatini boshqaradi, sozlamalar `.env` yordamida parametrik.

## 3. Texnologiyalar
- Python 3.12+
- Django 4.2.25
- Django REST Framework 3.16.1
- PostgreSQL (asosiy ma'lumotlar bazasi)
- Gunicorn + WhiteNoise (ishlab chiqarish serveri va statik fayllarni tarqatish)
- Qo'shimcha paketlar ro'yxati: `requirements.txt`

## 4. Katalog tuzilmasi
```
Portfolio_backend/
|-- portfolio/
|   |-- manage.py
|   |-- main/              # Sertifikat, skill va portfolio API'lari
|   \-- portfolio/         # Loyihaning global sozlamalari
|-- requirements.txt
|-- Procfile
\-- README.md
```
Statik fayllar `static/`, yig'ilgan fayllar `staticfiles/` va media fayllar `media/` kataloglarida saqlanadi (ishlab chiqarishda Cloudinary URL'lari qaytariladi).

## 5. Mahalliy ishga tushirish
1. Repozitoriyani klonlang va katalogga kiring.
2. Virtual muhit yarating:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Bog'liqliklarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
4. `.env` faylini tayyorlang (6-bo'limga qarang).
5. Migratsiyalarni bajaring:
   ```bash
   python portfolio/manage.py migrate
   ```
6. Lokal serverni ishga tushiring:
   ```bash
   python portfolio/manage.py runserver
   ```
   API manzili: `http://127.0.0.1:8000/main/...`

## 6. Muhit o'zgaruvchilari
| O'zgaruvchi             | Tavsif                                        | Standart qiymat |
|-------------------------|-----------------------------------------------|-----------------|
| `SECRET_KEY`            | Django maxfiy kaliti                          | test qiymat     |
| `DEBUG`                 | `True/False`                                  | `True`          |
| `POSTGRES_DB`           | Ma'lumotlar bazasi nomi                       | `portfolio`     |
| `POSTGRES_USER`         | Ma'lumotlar bazasi foydalanuvchisi            | `postgres`      |
| `POSTGRES_PASSWORD`     | Ma'lumotlar bazasi paroli                     | `postgres`      |
| `POSTGRES_HOST`         | Ma'lumotlar bazasi hosti                      | `localhost`     |
| `POSTGRES_PORT`         | Ma'lumotlar bazasi porti                      | `5432`          |
| `CSRF_TRUSTED_ORIGINS`  | Vergul bilan ajratilgan ruxsat etilgan hostlar| `https://api.jaloliddindev.uz` |
| `CORS_ALLOWED_ORIGINS`  | Frontend domenlari (vergul bilan)             | `http://localhost:3000`, `https://jaloliddindev.uz`, ... |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary hisob nomi                         | -               |
| `CLOUDINARY_API_KEY`    | Cloudinary API kaliti                         | -               |
| `CLOUDINARY_API_SECRET` | Cloudinary sir kaliti                         | -               |

`django-environ` bu o'zgaruvchilarni o'qiydi. Agar ma'lumotlar bazasiga SSL talab qilinmasa, `DATABASES["default"]["OPTIONS"]["sslmode"]` sozlamasini moslang.

## 7. Ma'lumotlar modellari
### Sertificate (`main.models.Sertificate`)
| Maydon | Tip | Izoh |
|--------|-----|------|
| `id`   | AutoField | Yagona identifikator |
| `img`  | FileField | Sertifikat rasmi, SVG yoki raster ruxsat etiladi |

### Skill (`main.models.Skill`)
| Maydon | Tip | Izoh |
|--------|-----|------|
| `id`          | AutoField | Yagona identifikator |
| `title`       | CharField (255) | Ko'nikma nomi |
| `description` | TextField | Tavsif (markdown qo'llanilmaydi) |
| `image`       | FileField | Ikona yoki rasm |

### Portfolio (`main.models.Portfolio`)
| Maydon | Tip | Izoh |
|--------|-----|------|
| `id`            | AutoField | Yagona identifikator |
| `title`         | CharField (255) | Loyiha nomi |
| `description`   | TextField | Loyiha haqida batafsil ma'lumot |
| `features`      | JSONField | Loyiha imkoniyatlari (odatda satrlar ro'yxati) |
| `tech_stack`    | JSONField | Texnologiyalar ro'yxati (`db_column="techstack"`) |
| `image`         | FileField | Loyiha rasmi |
| `github_link`   | URLField | GitHub repozitoriyasi |
| `in_link`       | URLField | Qo'shimcha havola (masalan, demo) |
| `tg_link`       | URLField | Telegram profili |
| `linkedin_link` | URLField | LinkedIn profili |
| `link`          | URLField | Loyiha sayti |

Barcha maydonlarda `blank=True, null=True` qo'llangan, shuning uchun admin panelda to'ldirilmagan qiymatlar xato bermaydi.

## 8. API ko'rinishi
- Bazaviy prefiks: lokalda `http://127.0.0.1:8000/main/`, ishlab chiqarishda `https://api.jaloliddindev.uz/main/`.
- Javoblar ro'yxat (`list`) ko'rinishida, elementlar `id` bo'yicha o'sish tartibida qaytadi.
- Javob sarlavha va sarlavhasiz holatda `HTTP 200 OK`.
- Xato holatlarida DRF standart strukturasidan foydalaniladi (masalan, `{"detail": "Not found."}`).

### 8.1. `GET /main/serticates/`
- **Tavsif:** Sertifikatlar ro'yxati.
- **Response 200:** sertifikat obyektlari ro'yxati.
```json
[
  {
    "id": 1,
    "img": "https://res.cloudinary.com/<cloud-name>/image/upload/v.../certificate.png"
  }
]
```

### 8.2. `GET /main/skills/`
- **Tavsif:** Ko'nikma kartochkalari.
- **Response 200:**
```json
[
  {
    "id": 3,
    "title": "Backend Development",
    "description": "Django va FastAPI bilan REST xizmatlari",
    "image": "https://res.cloudinary.com/<cloud-name>/image/upload/v.../skill.png"
  }
]
```

### 8.3. `GET /main/portfolios/`
- **Tavsif:** Portfolio loyihalari va havolalar.
- **Response 200:**
```json
[
  {
    "id": 5,
    "title": "Portfolio Platformasi",
    "description": "Frontend va backend integratsiyasi bilan shaxsiy sayt",
    "features": [
      "Mahalliy va ishlab chiqarish muhitiga moslashuvchan",
      "To'liq REST API",
      "CORS va Swagger integratsiyasi"
    ],
    "tech_stack": ["Django", "DRF", "PostgreSQL"],
    "image": "https://res.cloudinary.com/<cloud-name>/image/upload/v.../cover.png",
    "github_link": "https://github.com/username/portfolio",
    "in_link": null,
    "tg_link": "https://t.me/username",
    "linkedin_link": "https://www.linkedin.com/in/username/",
    "link": "https://jaloliddindev.uz"
  }
]
```

## 9. Serializatsiya va validatsiya
- Har bir model uchun `ModelSerializer` ishlatiladi (`views.SerticateSerializer`, `SkillSerializer`, `PortfolioSerializer`).
- Fayl maydonlari `validators.validate_image_or_svg` orqali tekshiriladi:
  - Kengaytmalar: `.gif`, `.jpg`, `.jpeg`, `.png`, `.svg`, `.webp`
  - SVG fayllarda `<svg` tegi mavjudligi tekshiriladi.
  - Raster fayllarda `Pillow` yordamida `Image.verify()` bajariladi.

## 10. Swagger va interaktiv hujjat
- `GET /swagger/` - Swagger UI
- `GET /swagger<format>/` - JSON/YAML sxema
- `GET /redoc/` - Redoc UI
`drf_yasg` token yoki autentifikatsiya talab qilmaydi, `AllowAny` ruxsatlari bilan ishlaydi.

## 11. Xavfsizlik va CORS
- `REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = AllowAny` - barcha endpointlar o'qishga ochiq.
- CORS domenlari `.env` orqali boshqariladi.
- `SECURE_PROXY_SSL_HEADER` va `USE_X_FORWARDED_HOST` sozlamalari reverse-proxy ortidan ishlashni qo'llab-quvvatlaydi.
- Agar kelajakda autentifikatsiya qo'shilsa, `rest_framework_simplejwt` allaqachon talabnomada mavjud.

## 12. Admin va ma'lumot bilan ishlash
- Admin panel: `/admin/`
- `SertificateAdmin`, `SkillAdmin`, `PortfolioAdmin` orqali filtr, qidiruv va tartiblash mavjud.
- Fayl maydonlari Cloudinary URL'larini qaytaradi, shu sababli admin formasi orqali yuklangan fayllar darhol tashqi CDN'da saqlanadi.

## 13. Deploy bo'yicha ko'rsatmalar
1. PostgreSQL instansiyasini tayyorlang va `.env` ga ulanish ma'lumotlarini yozing.
2. `python portfolio/manage.py migrate` va zarur bo'lsa `createsuperuser`.
3. Statik fayllarni yig'ing:
   ```bash
   python portfolio/manage.py collectstatic --noinput
   ```
4. Gunicorn orqali ishga tushiring (`Procfile`):  
   `web: gunicorn --chdir portfolio portfolio.wsgi:application`
5. Reverse proxy (Nginx) yoki Platform-as-a-Service SSL ni boshqaradi.

## 14. Test va keyingi qadamlarga tavsiyalar
- `main/tests.py` hozircha bo'sh, DRF API testlarini qo'shish tavsiya etiladi.
- CI/CD pipeline'da migratsiyalar va `collectstatic` avtomatlashtirilsin.
- CORS va CSRF sozlamalarini ishlab chiqarish domenlariga moslashtirib, `DEBUG=False` rejimida sinovdan o'tkazing.
- Kelajakda:
  - JWT autentifikatsiyasini (Simple JWT) faollashtirish
  - Ma'lumotlarni POST/PUT orqali boshqarish uchun qo'shimcha endpointlar
  - Throttling va caching qatlamini joriy qilish

Portfolio Backend shu holatda frontend ilovalar uchun to'liq o'qish rejimida xizmat ko'rsatadi va yangi funksionallik qo'shishga tayyor.
