# یادداشت بررسی سایت‌های اعضای هیئت علمی

این فهرست از نسخهٔ قبلی به‌عنوان یادداشت الهام طراحی حفظ شده است. دادهٔ خام اندازه‌گیری CSS، نشانی دقیق صفحات و گزارش مرورگر برای این ۴۰ نام در بستهٔ قبلی موجود نبود؛ بنابراین این فایل یک benchmark اندازه‌گیری‌شده و قابل بازتولید نیست. اندازه‌های آزموده‌شدهٔ نسخهٔ فعلی و محدودیت‌های تست در AUDIT_FA.md ثبت شده‌اند.

## فهرست نام‌های ثبت‌شده در یادداشت قبلی

### Stanford University

Diyi Yang، Dan Jurafsky، Christopher Manning، Christopher Ré، Chelsea Finn، Percy Liang، James Zou، Michael Bernstein، Emma Brunskill، Tatsunori Hashimoto، Dorsa Sadigh، Stefano Ermon و Jure Leskovec.

### MIT

Jacob Andreas، Aleksander Mądry، Kaiming He، Regina Barzilay، Song Han، Dina Katabi، Tommi Jaakkola و Phillip Isola.

### Carnegie Mellon University

Aditi Raghunathan، Deepak Pathak، Deva Ramanan، Ruslan Salakhutdinov، Graham Neubig، Zico Kolter، Zachary Lipton و Hoda Heidari.

### University of Washington

Pang Wei Koh، Hannaneh Hajishirzi، Dieter Fox، Luke Zettlemoyer، Shwetak Patel و Ali Farhadi.

### سایر دانشگاه‌ها

Yisong Yue از Caltech، Pranav Rajpurkar از Harvard، Dhruv Batra از Georgia Tech، Saining Xie از NYU و Dawn Song از UC Berkeley.

## اصول پیشنهادی طراحی در یادداشت قبلی

1. نام معمولاً نقش عنوان صفحه را دارد، نه headline تبلیغاتی؛ به همین دلیل اندازهٔ آن باید مشخص ولی کنترل‌شده باشد.
2. عنوان شغلی و دانشگاه بلافاصله زیر نام و با اندازه‌ای نزدیک به متن عادی می‌آیند.
3. بسیاری از سایت‌های موفق یک یا دو جملهٔ مستقیم دربارهٔ پژوهش دارند و از slogan بزرگ دوری می‌کنند.
4. لینک‌های Scholar، GitHub، CV و Email باید در اولین viewport قابل مشاهده باشند.
5. فهرست مقاله‌ها معمولاً متنی و فشرده است؛ کارت‌های بزرگ برای هر مقاله فضای زیادی تلف می‌کنند.
6. بخش‌های پژوهشی با تیتر، یک توضیح کوتاه و خطوط جداکننده بهتر از کارت‌های متعدد عمل می‌کنند.
7. عرض محدود محتوا و فضای سفید کنترل‌شده، خوانایی را بیشتر از افکت، gradient یا animation بالا می‌برد.
8. در موبایل، عکس و هویت باید فشرده شوند و navigation به منوی واضح تبدیل شود؛ متن نباید برای حفظ طراحی دسکتاپ کوچک یا بریده شود.

## مقادیر تاریخی نسخهٔ v3، نه نسخهٔ اصلاح‌شدهٔ v3.1

| عنصر | دسکتاپ | موبایل 390px |
|---|---:|---:|
| نام | 36px | حدود 29px |
| عکس | 178px | 94px |
| عنوان بخش | حداکثر حدود 30px | حدود 24px |
| عنوان شغلی | حدود 15px | حدود 14px |
| متن معرفی | حدود 15px | حدود 14px |
| ارتفاع هدر | 58px | 56px |
| حداکثر عرض محتوا | 1020px | عرض صفحه منهای 28px |

این اعداد median آماری CSS سایت‌های بررسی‌شده نیستند؛ پس از مشاهدهٔ سلسله‌مراتب و تراکم آن‌ها، برای محتوای همین سایت انتخاب و سپس روی چند viewport آزمایش شده‌اند.
