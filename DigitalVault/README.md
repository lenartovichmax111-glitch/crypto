# DigitalVault

Навчальний вебзастосунок: HTML/CSS/JavaScript + FastAPI + SQLite + JWT. Текст нотаток шифрується у браузері AES-GCM за паролем, який не надсилається серверу. Назви нотаток не шифруються.

## Запуск у VS Code (PowerShell)

У першому терміналі:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JWT_SECRET = [Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
uvicorn main:app --reload
```

Якщо PowerShell забороняє активацію середовища, замість активації виконайте `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` і `.\.venv\Scripts\python.exe -m uvicorn main:app --reload`.

У другому терміналі з кореня DigitalVault:

```powershell
cd frontend
py -m http.server 5500 --bind 127.0.0.1
```

Відкрийте http://127.0.0.1:5500. Документація API: http://127.0.0.1:8000/docs.

## Важливо

- Це навчальний прототип, а не перевірений для продуктивного використання менеджер секретів.
- JWT зберігається тільки в оперативній пам'яті сторінки; перезавантаження сторінки вимагає повторного входу.
- Пароль шифрування не відновлюється. Якщо його забути, розшифрувати нотатки неможливо.
- У робочому середовищі потрібні HTTPS, захист від перебору паролів, CSRF/XSS-аудит, належне управління секретами та додаткові перевірки.
