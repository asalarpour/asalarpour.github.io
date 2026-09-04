# راهنمای انتشار سایت روی GitHub Pages

این بسته برای مخزن زیر آماده شده است:

```text
asalarpour/asalarpour.github.io
```

آدرس نهایی سایت:

```text
https://asalarpour.github.io/
```

## روش پیشنهادی: GitHub Desktop

1. از نسخهٔ فعلی مخزن یک نسخهٔ پشتیبان نگه دارید. فایل ZIP قدیمی همین کار را انجام می‌دهد.
2. این بسته را از حالت ZIP خارج کنید.
3. در GitHub Desktop مخزن `asalarpour.github.io` را Clone یا باز کنید.
4. گزینهٔ **Repository → Show in Explorer/Finder** را بزنید.
5. همهٔ فایل‌های قدیمی داخل پوشهٔ مخزن را حذف کنید، اما پوشهٔ مخفی `.git` را حذف نکنید.
6. تمام محتویات این بسته را داخل همان پوشه کپی کنید. خود پوشهٔ بیرونی را کپی نکنید؛ فایل `index.html` باید مستقیماً در ریشهٔ مخزن قرار بگیرد.
7. در GitHub Desktop یک Commit با پیام زیر ایجاد کنید:

```text
Replace website with new academic site
```

8. گزینهٔ **Push origin** را بزنید.
9. در GitHub وارد این مسیر شوید:

```text
Repository → Settings → Pages
```

10. در قسمت **Build and deployment**، مقدار **Source** را روی **GitHub Actions** قرار دهید.
11. از تب **Actions** اجرای workflow با نام زیر را بررسی کنید:

```text
Deploy academic website to GitHub Pages
```

پس از سبزشدن workflow، سایت معمولاً ظرف چند دقیقه روی آدرس اصلی نمایش داده می‌شود.

## روش خط فرمان

```bash
git clone https://github.com/asalarpour/asalarpour.github.io.git
cd asalarpour.github.io

# فایل‌های قدیمی را حذف کنید ولی .git را نگه دارید.
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

# سپس محتوای بستهٔ جدید را داخل این پوشه کپی کنید.

git add -A
git commit -m "Replace website with new academic site"
git push origin main
```

## چرا دو روش انتشار داخل بسته وجود دارد؟

فایل‌های HTML آماده در ریشهٔ پروژه قرار دارند؛ بنابراین حالت قدیمی **Deploy from a branch** نیز معمولاً کار می‌کند. در عین حال workflow موجود در `.github/workflows/deploy.yml` بعد از هر تغییر، داده‌ها را اعتبارسنجی می‌کند، سایت را دوباره می‌سازد و سپس منتشر می‌کند. استفاده از GitHub Actions مطمئن‌تر است.

## اتصال دامنهٔ شخصی در آینده

بعداً می‌توانید دامنه‌ای مثل `amirsalarpour.com` را بدون تغییر ساختار سایت به GitHub Pages متصل کنید. در آن مرحله باید دامنه را در Settings → Pages ثبت و فایل `CNAME` را اضافه کنید. تا زمانی که دامنه نخریده‌اید، فایل `CNAME` لازم نیست.
