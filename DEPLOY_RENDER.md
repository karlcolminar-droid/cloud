Deploying to Render

This project includes `render.yaml` to define the Web Service. Follow these steps to deploy:

1. Push the repository to GitHub (see `scripts/publish.sh`).
2. Create a new Web Service on Render, connect to your GitHub repo, or import the `render.yaml` during service creation.
3. In the Render dashboard, set the environment variables (Settings -> Environment):
   - `SECRET_KEY` (random strong value)
   - `DEBUG` = `False`
   - `DATABASE_URL` (Render Postgres URL)
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
   - `ALLOWED_HOSTS` (comma-separated hostnames)
4. Ensure the Build Command is `pip install -r requirements.txt` and Start Command is `gunicorn recipe_project.wsgi --log-file -` (Procfile already included).
5. After the first deploy, open Render's console or use a deploy hook to run migrations:

```bash
# via Render shell (or from your machine using render CLI)
python manage.py migrate
python manage.py createsuperuser
```

6. Optional: Add Render health checks and automatic deploys from the `main` branch.

If you want, I can generate a GitHub Actions workflow that runs tests and runs `python manage.py migrate` on deploy, but you must provide a Render API key to allow automatic operations.
