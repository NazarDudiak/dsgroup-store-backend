# Store backend

Django REST API and Django Admin for a small catalogue (up to 100 products). The admin is the content workspace: categories, products, images, availability, SEO metadata and incoming orders.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations catalog && python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `/admin/` to manage the shop. Public API is at `/api/v1/`.

## First catalogue and deployment

For an immediately usable demo catalogue run `python manage.py seed_demo`. Product photos are uploaded in the product form in `/admin/`.

For containers, copy `.env.example` to `.env`, set a production `SECRET_KEY`, then run `docker compose up --build -d`. Create the initial admin account with `docker compose exec api python manage.py createsuperuser` and optionally seed sample content with `docker compose exec api python manage.py seed_demo`.
