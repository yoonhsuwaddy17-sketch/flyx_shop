# FlyX Flask Shop — Railway-ready (with SQLite Orders)
- Brand: **FlyX**
- Quote: **"Xpress Yourself With FlyX"**
- Payments: **KPay, WavePay, AYAPay (placeholders)**
- DB: **SQLite** (`flyx.db`) with Products & Orders
- Admin: `/admin` (password via `ADMIN_PASSWORD`, default `flyxadmin`)

## Run locally (Windows)
Double-click `start_local.bat` or run:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set ADMIN_PASSWORD=flyxadmin
python app.py
```
Open http://127.0.0.1:5000

## Deploy on Railway (24/7)
1. Push this folder to GitHub
2. Railway → New Project → Deploy from GitHub → select repo
3. Done. Uses `Procfile`/`railway.json` with Gunicorn.

## Notes
- Upload `static/uploads/logo.jpg` to show logo in header.
- Prices are in **MMK (Ks)**.
- Admin can add products, view orders, and update status (Pending/Confirmed/Shipped/Delivered/Canceled).
