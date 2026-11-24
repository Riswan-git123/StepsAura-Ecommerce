# StepsAura

StepsAura is a Django shoe store application.

## Local setup

1. Create and activate a Python virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Set `DJANGO_SECRET_KEY` and any other values from `.env.example` in your shell or IDE environment.
4. Run `python manage.py migrate` and `python manage.py runserver`.

The storefront inserts its catalog from `storeapp/collections.py` when the home page is first opened.

## Deploy to Vercel

Import this repository into Vercel with the Django project root (the directory containing `manage.py`) as the Root Directory. Vercel detects Django and serves collected static assets from `STATIC_ROOT`.

Set these environment variables for Production in Vercel:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`: a newly generated, private random secret
- `DJANGO_ALLOWED_HOSTS`: `.vercel.app` and any custom domain
- `CSRF_TRUSTED_ORIGINS`: `https://<your-project>.vercel.app` and any custom domain
- `DATABASE_URL`: a managed PostgreSQL connection URL

Run `python manage.py migrate` against the managed PostgreSQL database before using the deployed store. Production startup requires `DATABASE_URL`; Vercel's function filesystem is read-only apart from temporary storage, so SQLite is development-only. The Git ignore rules exclude the local database and virtual environment.
