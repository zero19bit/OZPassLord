# OZ PassLord 🔐

A secure, offline command-line password manager built with Python.  
All passwords are encrypted using AES-256-GCM with a key derived from a master password via Argon2id.  
It works on Linux, macOS, and Windows.

---

## ✨ Features

- **Secure vault** – All data is encrypted with AES-256-GCM. The key is derived from your master password using Argon2id (memory-hard, time-hard).
- **Master password** – Never stored anywhere; if forgotten, data cannot be recovered.
- **Portable & System modes** – Store your vault alongside the program (USB-friendly) or in your user directory.
- **Clipboard auto-clear** – Copied passwords are automatically cleared from the clipboard after a configurable time (default 30 seconds).
- **Password generator** – Generate strong random passwords with adjustable length.
- **Search** – Find entries by title, username, URL, or notes (case-insensitive, table output, detail view by ID).
- **Import/Export** – Exchange data with CSV and JSON formats (export warns about unencrypted files).
- **Configuration management** – View and change settings (vault path, timeouts, editor, etc.) via the `config` command.
- **Change master password** – Update your master password without losing data.
- **Duplicate prevention** – Prevents adding entries with duplicate titles; interactive conflict resolution during import.

---

## 🧱 Code Structure

| File | Purpose |
|------|---------|
| `cli.py` | Command-line interface using Click. Contains all user commands. |
| `vault.py` | Core cryptography: AES-256-GCM encryption/decryption of the vault file, key derivation with Argon2id. |
| `config.py` | Manages configuration file (`config.json`), supports portable & system mode. |
| `generator.py` | Secure password generator using the `secrets` module. |
| `io_handler.py` | Handles CSV/JSON import/export logic. |
| `session.py` | (optional) Session timeout functionality (not used in the main CLI, but kept for future GUI). |

The project follows a clean separation of concerns: the backend logic (`vault`, `config`, `io_handler`, `generator`) is completely independent from the frontend (`cli.py`). This makes it easy to build a GUI version later.

---

## 🔒 Security Details

- **Encryption**: AES-256-GCM (authenticated encryption). The entire vault file is encrypted, including all metadata.
- **Key Derivation**: Argon2id with 64 MB memory, 3 iterations, 4 parallelism lanes.
- **Master Password**: Never stored or cached; required on every command (unless a session timeout mechanism is implemented later).
- **Clipboard**: Passwords are copied to the clipboard and automatically cleared after `clipboard_timeout` seconds.
- **Export Warning**: When exporting to plain CSV/JSON, a clear warning is shown, and user confirmation is required.

---

## 📦 Installation

### Option 1: Pre-built Executable (recommended)
Download the latest `ozpasslord` (or `ozpasslord.exe` for Windows) from the Releases page.

- **Linux/macOS**:  
  chmod +x ozpasslord
  ./ozpasslord init

- **Windows**:  
  Open a terminal in the folder containing `ozpasslord.exe` and run:
  ozpasslord.exe init

*Optional: Move the executable to a directory in your PATH for global access.*

### Option 2: Run from Source (Python 3.8+ required)
git clone https://github.com/yourrepo/ozpasslord.git
cd ozpasslord
pip install -r requirements.txt
python cli.py init

---

## 🚀 Quick Start

```bash
ozpasslord init                     # Create a new vault (choose portable or system)
ozpasslord add --title Gmail --username ali@gmail.com --password MyP@ssw0rd
ozpasslord add --title GitHub --username ali-dev --password git123 --url https://github.com --note "dev account"
ozpasslord list
ozpasslord get Gmail                # Copies password to clipboard, clears after 30s
ozpasslord search gmail             # Case-insensitive search, select ID to view details
ozpasslord generate 24 --show       # Generate a 24-char password and display it
ozpasslord update Gmail --password NewP@ss
ozpasslord delete Gmail             # Confirm with y/n
ozpasslord export myvault.csv       # Export to CSV (JSON also supported)
ozpasslord import myvault.csv       # Import, with interactive duplicate handling
ozpasslord config show              # View current settings
ozpasslord config set session_timeout 600
ozpasslord change-master            # Change your master password
```

---

## ⚙️ Configuration

The configuration file (`config.json`) is stored:
- **Portable mode**: next to the executable.
- **System mode**: in the system’s application directory (`~/.ozpasslord/` on Linux, `%APPDATA%\ozpasslord\` on Windows).

Default settings:
```json
{
    "vault_path": "...",
    "session_timeout": 300,
    "clipboard_timeout": 30,
    "editor": "vim",
    "default_password_length": 20
}
```
Use `ozpasslord config show` to view them and `ozpasslord config set <key> <value>` to change them.

---

## 🌐 Portable vs. System Mode

- **Portable (p)**: Configuration and vault files are stored alongside the program executable. Ideal for USB sticks.
- **System (s)**: Files are saved in a standard, user‑specific directory. Best for permanent installations.

*You choose the mode once during init.*

---

## ⚠️ Important Notes

- **Never forget your master password!** There is no recovery mechanism.
- The `init` command will overwrite an existing vault without warning (a confirmation prompt is planned for v1.1). Always keep backups.
- On Linux, clipboard auto‑copy requires `xclip` (X11) or `wl-clipboard` (Wayland). If missing, the password is shown in the terminal.

---

## 📄 License
MIT License – see LICENSE file.

---

## 🤝 Contributing
Pull requests, issues, and feature requests are welcome.  
For major changes, please open an issue first to discuss what you would like to change.

---
---

# فارسی 🇮🇷
**اوزپس‌لرد – مدیر رمز عبور خط‌فرمانی**

یک ابزار امن و آفلاین برای مدیریت رمزهای عبور که با پایتون نوشته شده است.  
تمام رمزها با استفاده از AES-256-GCM رمزنگاری می‌شوند و کلید رمزنگاری از رمز مستر با کمک Argon2id مشتق می‌شود.  
این برنامه روی لینوکس، مک و ویندوز کار می‌کند.

---

## ✨ امکانات

- **گاوصندوق امن** – داده‌ها با AES-256-GCM رمزنگاری می‌شوند.
- **حالت قابل‌حمل (Portable) و سیستمی (System)** – گاوصندوق را کنار خود برنامه یا در پوشهٔ خانگی ذخیره کنید.
- **پاک‌سازی خودکار کلیپ‌بورد** – رمزهای کپی شده پس از مدت قابل تنظیم (پیش‌فرض ۳۰ ثانیه) پاک می‌شوند.
- **تولیدکنندهٔ رمز تصادفی** – رمزهای قوی با طول دلخواه بسازید.
- **جستجو** – جستجوی بی‌حساسیت به حروف در عنوان، نام کاربری، آدرس و یادداشت‌ها.
- **ورود/خروج (Import/Export)** – پشتیبانی از CSV و JSON با هشدار امنیتی هنگام خروجی.
- **مدیریت تنظیمات** – مشاهده و تغییر مسیر گاوصندوق، تایم‌اوت‌ها و … با دستور `config`.
- **جلوگیری از ثبت تکراری** – عنوان‌های تکراری در `add` رد می‌شوند؛ در `import` تعامل حل تعارض وجود دارد.

---

## 🧱 ساختار کد

| فایل | وظیفه |
|------|---------|
| `cli.py` | رابط خط‌فرمان با کتابخانهٔ Click |
| `vault.py` | رمزنگاری/رمزگشایی با AES-GCM و استخراج کلید با Argon2id |
| `config.py` | مدیریت فایل پیکربندی (حالت Portable/System) |
| `generator.py` | تولید رمز تصادفی امن |
| `io_handler.py` | توابع ورودی/خروجی CSV و JSON |
| `session.py` | (اختیاری) مدیریت نشست برای قفل خودکار (برای نسخهٔ GUI نگه داشته شده) |

لایهٔ منطق (backend) کاملاً از رابط کاربری جدا شده است و می‌توان بعداً یک نسخهٔ گرافیکی به آن افزود.

---

## 🔒 نکات امنیتی

- **رمزنگاری**: کل فایل با AES-256-GCM رمزنگاری می‌شود.
- **کلید**: با Argon2id (حافظه ۶۴MB، ۳ تکرار) از رمز مستر ساخته می‌شود.
- **رمز مستر**: هرگز ذخیره نمی‌شود؛ فراموشی آن مساوی با از دست رفتن همهٔ داده‌هاست.
- **کلیپ‌بورد**: رمزها به‌طور خودکار پس از `clipboard_timeout` ثانیه پاک می‌شوند.
- **هشدار خروجی**: هنگام صدور فایل متنی، هشدار داده می‌شود که فایل رمزنگاری‌نشده است.

---

## 📦 نصب و راه‌اندازی

### روش ۱: فایل اجرایی آماده (پیشنهادی)
آخرین نسخهٔ `ozpasslord` را از صفحهٔ Releases دانلود کنید.

- **لینوکس/مک**:
  chmod +x ozpasslord
  ./ozpasslord init

- **ویندوز**:
  در پوشهٔ فایل دانلودی، ترمینال را باز کنید و دستور زیر را بزنید:
  ozpasslord.exe init

*(می‌توانید فایل اجرایی را به یک مسیر در PATH منتقل کنید تا از همه‌جا در دسترس باشد.)*

### روش ۲: اجرای مستقیم سورس (نیاز به پایتون ۳.۸+)
git clone https://github.com/yourrepo/ozpasslord.git
cd ozpasslord
pip install -r requirements.txt
python cli.py init

---

## 🚀 شروع سریع

```shell
ozpasslord init                     # ساخت گاوصندوق جدید
ozpasslord add --title Gmail --username ali@gmail.com --password MyP@ssw0rd
ozpasslord add --title GitHub --username ali-dev --password git123 --url https://github.com --note "dev account"
ozpasslord list
ozpasslord get Gmail                # رمز در کلیپ‌بورد کپی می‌شود و بعد از ۳۰ ثانیه پاک می‌شود
ozpasslord search gmail             # جستجوی بی‌حساسیت به حروف، انتخاب ID برای جزئیات
ozpasslord generate 24 --show       # تولید رمز ۲۴ کاراکتری و نمایش آن
ozpasslord update Gmail --password NewP@ss
ozpasslord delete Gmail             # تأیید با y/n
ozpasslord export myvault.csv       # خروجی CSV (JSON هم پشتیبانی می‌شود)
ozpasslord import myvault.csv       # ورود با مدیریت تعاملی رکوردهای تکراری
ozpasslord config show              # نمایش تنظیمات فعلی
ozpasslord config set session_timeout 600
ozpasslord change-master            # تغییر رمز مستر
```

---

## ⚙️ تنظیمات

فایل `config.json` در حالت Portable کنار فایل اجرایی و در حالت System در پوشهٔ استاندارد سیستم ذخیره می‌شود.

تنظیمات پیش‌فرض:
```json
{
    "vault_path": "...",
    "session_timeout": 300,
    "clipboard_timeout": 30,
    "editor": "vim",
    "default_password_length": 20
}
```
با `ozpasslord config show` آن‌ها را ببینید و با `ozpasslord config set <key> <value>` تغییر دهید.

---

## ⚠️ نکات مهم

- **هرگز رمز مستر خود را فراموش نکنید!** راهی برای بازیابی وجود ندارد.
- دستور `init` گاوصندوق موجود را بدون هشدار بازنویسی می‌کند (این مشکل در نسخهٔ ۱.۱ برطرف خواهد شد). همیشه پشتیبان تهیه کنید.
- در لینوکس، برای پشتیبانی از کلیپ‌بورد، باید `xclip` (در X11) یا `wl-clipboard` (در Wayland) نصب باشد؛ در غیر این صورت رمز در ترمینال نمایش می‌یابد.

---

## 📄 مجوز
این پروژه تحت مجوز MIT منتشر شده است.

---

## 🤝 مشارکت
پیشنهادها، گزارش اشکال و درخواست‌های ادغام (Pull Request) خوش‌آمدند.  
لطفاً پیش از اعمال تغییرات اساسی، یک Issue باز کنید تا در مورد آن بحث شود.
