# راهنمای به‌روزرسانی سایت

محتوای اصلی سایت داخل پوشهٔ `data` قرار دارد. فایل‌های HTML خروجی هستند و بهتر است مستقیماً ویرایش نشوند.

بعد از هر تغییر این دستور را اجرا کنید:

```bash
python3 scripts/build_site.py
```

سپس تغییرات را Commit و Push کنید. GitHub Actions نیز هنگام انتشار دوباره همین build و validation را اجرا می‌کند.

---

## ۱. تغییر Google Scholar، GitHub، LinkedIn، ایمیل یا CV

فایل زیر را باز کنید:

```text
data/profile.json
```

لینک‌های حرفه‌ای در بخش `links` قرار دارند:

```json
{
  "id": "scholar",
  "label": "Google Scholar",
  "url": "https://scholar.google.com/citations?user=PPyF4hEAAAAJ&hl=en",
  "external": true
}
```

شناسه‌های زیر را نگه دارید، چون سایت برای انتخاب آیکون و اعتبارسنجی از آن‌ها استفاده می‌کند:

```text
scholar
github
linkedin
email
cv
```

برای ایمیل از قالب زیر استفاده کنید:

```text
mailto:asalarp@clemson.edu
```

فایل PDF رزومه در این مسیر است:

```text
assets/files/Amir_Salarpour_CV.pdf
```

برای جایگزینی رزومه فقط PDF جدید را دقیقاً با همین نام روی فایل قبلی کپی کنید. در این حالت لازم نیست هیچ لینکی را عوض کنید.

---

## ۲. اضافه‌کردن مقاله با دستور آماده

در ریشهٔ سایت اجرا کنید:

```bash
python3 scripts/add_publication.py
```

اسکریپت عنوان، نویسندگان، سال، venue، لینک مقاله، PDF، کد و سایر اطلاعات را می‌پرسد، رکورد JSON را می‌سازد و سایت را دوباره build می‌کند.

نام `Amir Salarpour` را دقیقاً همین‌طور وارد کنید؛ سایت آن را در فهرست نویسندگان به‌صورت خودکار bold می‌کند.

### روش دستی

فایل زیر را کپی کنید:

```text
data/publications/_template.json
```

نسخهٔ جدید را با نامی مانند زیر ذخیره کنید:

```text
data/publications/2027-my-new-paper.json
```

نمونهٔ رکورد:

```json
{
  "id": "my-new-paper",
  "title": "My New Paper",
  "authors": [
    "Amir Salarpour",
    "Coauthor Name"
  ],
  "year": 2027,
  "venue_short": "CVPR",
  "venue": "IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2027.",
  "type": "Conference paper",
  "status": "Accepted",
  "featured": true,
  "order": 1,
  "topics": [
    "Autonomous driving",
    "Adversarial robustness"
  ],
  "note": "",
  "award": "",
  "image": "",
  "links": {
    "paper": "https://...",
    "pdf": "https://...pdf",
    "code": "https://github.com/...",
    "project": "https://...",
    "doi": "https://doi.org/...",
    "bibtex": ""
  }
}
```

فیلد `featured` تعیین می‌کند مقاله در صفحهٔ اصلی ظاهر شود یا نه. بهتر است در مجموع فقط حدود ۶ تا ۸ مقاله featured باشند.

لینک‌های خالی نمایش داده نمی‌شوند. ترتیب پیشنهادی لینک‌ها:

- `paper`: صفحهٔ رسمی مقاله، arXiv abstract یا صفحهٔ ناشر
- `pdf`: لینک مستقیم PDF
- `code`: مخزن GitHub
- `project`: صفحهٔ پروژه
- `doi`: لینک کامل DOI با `https://doi.org/`
- `bibtex`: فایل BibTeX محلی یا لینک معتبر

---

## ۳. اضافه‌کردن خبر

روش ساده:

```bash
python3 scripts/add_news.py
```

یا فایل زیر را دستی ویرایش کنید:

```text
data/news.json
```

نمونه:

```json
{
  "date": "2027-03-15",
  "label": "Mar 2027",
  "kind": "Publication",
  "text": "Our paper was accepted to CVPR 2027."
}
```

خبرها هنگام build بر اساس تاریخ مرتب می‌شوند.

---

## ۴. اضافه‌کردن پروژه

روش ساده:

```bash
python3 scripts/add_project.py
```

یا فایل زیر را ویرایش کنید:

```text
data/projects.json
```

هر پروژه می‌تواند عنوان، وضعیت، بازهٔ زمانی، حامی مالی، نقش، خلاصه و موضوعات خودش را داشته باشد. ساختار پروژه از همین حالا برای زمانی که هیئت علمی و صاحب گروه پژوهشی شوید آماده است.

---

## ۵. تغییر متن معرفی و عنوان شغلی

فایل:

```text
data/profile.json
```

فیلدهای مهم:

```text
role
affiliation
lab
location
tagline
intro
bio
```

وقتی هیئت علمی شدید، معمولاً کافی است `role`، `affiliation` و متن `bio` را عوض کنید. ساختار صفحات نیازی به بازنویسی ندارد.

---

## ۶. تغییر حوزه‌های پژوهشی

فایل:

```text
data/research.json
```

هر موضوع پژوهشی یک عنوان، توضیح و چند کلیدواژه دارد. برای حذف یا اضافه‌کردن یک حوزه فقط یک object را در آرایهٔ `themes` تغییر دهید.

---

## ۷. تغییر عکس پروفایل

فایل‌های فعلی:

```text
assets/images/profile-320.webp
assets/images/profile-640.webp
assets/images/profile-320.jpg
assets/images/profile-640.jpg
```

برای بهترین سازگاری، نسخهٔ WebP و JPG را با همان نام‌ها نگه دارید. تصویر باید مربع باشد. اندازهٔ 640×640 برای نسخهٔ اصلی کافی است.

---

## ۸. تست قبل از انتشار

```bash
python3 scripts/build_site.py
python3 -m http.server 8000
```

سپس این آدرس را باز کنید:

```text
http://localhost:8000
```

صفحات اصلی را روی موبایل و دسکتاپ بررسی کنید:

```text
/
/research/
/publications/
/teaching/
/service/
/news/
```

اگر JSON ناقص، شناسهٔ مقاله تکراری، لینک نامعتبر یا تصویر گم‌شده باشد، build متوقف می‌شود و خطا را دقیق نمایش می‌دهد.


## اصلاحات نگهداری در v3.1

تنظیم تعداد آیتم‌های صفحهٔ اصلی در `data/site.json`:

```json
"home_publication_limit": 6,
"home_news_limit": 4,
"home_project_limit": 2
```

فقط پروژه‌هایی با `featured: true` به صفحهٔ اصلی می‌آیند. فهرست خالی پروژه‌ها مجاز است.
پروژه‌ها در صفحهٔ Research نمایش داده می‌شوند؛ این نسخه صفحهٔ جداگانهٔ هر پروژه،
پنل ورود، یا دیتابیس سروری تولید نمی‌کند.

برای پیوندزدن نام کوتاه مقاله در خبر، فیلد `link_text` را اضافه کنید؛ مثلاً
`"link_text": "GATE"`. شناسهٔ `publication` لینک اصلی را تعیین می‌کند.

آزمون‌های سریع:

```bash
python3 scripts/test_site.py
python3 scripts/build_site.py --output dist
python3 scripts/check_site.py --site dist
```

برای جلوگیری از پاک‌شدن فایل‌های شخصی، پوشهٔ خروجی باید خالی یا یک خروجیِ قبلی
همین نسخه باشد. پوشه‌های نامرتبط با `--output` بازنویسی نمی‌شوند.
