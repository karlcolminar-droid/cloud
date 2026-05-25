# Photo Album Management (Cloud Render)

This project is a Django-based Photo Album Management application with Cloudinary media storage and production configuration suitable for Render.com deployment.

Key features
- Class-based views for list, create, update, delete
- Role-based access control (Album Admin group + owner checks)
- Cloudinary for media storage via `django-cloudinary-storage`
- PostgreSQL-ready configuration via `dj-database-url`

Quick setup (local)

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Create a `.env` file with these variables:

```
SECRET_KEY=your-secret
DEBUG=True
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

3. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Deploying to Render (summary)

- Create a new Web Service on Render from this repository.
- Set the Build Command: `pip install -r requirements.txt`
- Start Command / Procfile will run: `gunicorn recipe_project.wsgi`
- Add environment variables on Render: `SECRET_KEY`, `DATABASE_URL` (managed Postgres), `CLOUDINARY_*` credentials, `ALLOWED_HOSTS`, `DEBUG=False`.
- Run `python manage.py migrate` via a Deploy Hook or `render shell` after initial deploy.

Notes
- Do NOT commit secrets to the repository. Use Render's environment variables.
# cloud
