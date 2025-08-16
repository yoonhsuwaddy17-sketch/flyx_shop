web: gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:$PORT app:app
web: python app.py
name: flyx_shop
services:
  - name: web
    type: web
    src: .
    run: python app.py
    env:
      - name: SECRET_KEY
        value: flyx_secret_key
      - name: ADMIN_PASSWORD
        value: flyxadmin
