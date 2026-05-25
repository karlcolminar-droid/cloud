# Cloud-Render Photo Album — Submission Document

## Project Overview
A **production-ready Django photo album management system** with role-based access control (RBAC), class-based views (CBVs), and cloud storage integration.

---

## Submission Details

### Repository Link
**GitHub Repository:** https://github.com/karlreycolminar-ui/cloud

**Clone:** 
```bash
git clone https://github.com/karlreycolminar-ui/cloud.git
cd cloud
```

---

### Live Application URL
**Live Instance on Render:** `https://your-service-name.onrender.com`
*(URL will be provided after Render deployment)*

**Test Credentials (post-deployment):**
- **Username:** admin
- **Password:** *(set during first deploy migration)*

---

## Key Features Implemented

### 1. **Class-Based Views (CBVs)**
- `PhotoListView` — Display and create photos
- `PhotoUpdateView` — Edit photo details
- `PhotoDeleteView` — Delete photos with confirmation
- All inherit from Django's generic CBVs and mixins

### 2. **Role-Based Access Control (RBAC)**
- `LoginRequiredMixin` — Enforce user authentication
- `IsOwnerOrAdminMixin` — Only photo owners or staff can edit/delete
- Django's built-in `User` and `Group` models for permissions
- "Album Admin" group with full access (created on app startup via `post_migrate`)

### 3. **Media Storage**
- **Local Development:** Django `FileSystemStorage` (`MEDIA_ROOT = BASE_DIR / 'media'`)
- **Production (Render):** Cloudinary cloud storage (`CloudinaryField` + `django-cloudinary-storage`)
- Toggle via `USE_CLOUDINARY` environment variable

### 4. **Database**
- **Local:** SQLite (`db.sqlite3`)
- **Production:** PostgreSQL on Render (provisioned automatically)
- Uses `dj-database-url` for database URL parsing

### 5. **Deployment**
- **Web Server:** Gunicorn (configured in `Procfile`)
- **Static Files:** WhiteNoise middleware for production serving
- **Container Ready:** `requirements.txt` with all dependencies

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 6.0.5 |
| Python | 3.10+ |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL |
| Media Storage | Cloudinary |
| Web Server | Gunicorn |
| Static Serving | WhiteNoise |
| Deployment | Render |
| Version Control | Git/GitHub |

---

## Project Structure

```
cloud-render/
├── gallery/                          # Django app
│   ├── models.py                     # RecipePhoto model with owner FK
│   ├── views.py                      # CBVs with RBAC
│   ├── forms.py                      # Photo upload form
│   ├── urls.py                       # App URL routing
│   ├── templates/gallery/            # HTML templates
│   │   ├── home.html                 # Photo list + upload
│   │   ├── edit.html                 # Photo edit form
│   │   └── delete.html               # Delete confirmation
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # AppConfig with post_migrate hook
│   └── migrations/                   # Database migrations
├── recipe_project/                   # Django project settings
│   ├── settings.py                   # Config (Cloudinary, DB, storage)
│   ├── urls.py                       # Root URLConf
│   ├── wsgi.py                       # WSGI entrypoint
│   └── asgi.py                       # ASGI entrypoint
├── manage.py                         # Django CLI
├── requirements.txt                  # Python dependencies
├── Procfile                          # Render process definition
├── render.yaml                       # Render service manifest
├── .env.example                      # Environment variables template
└── README.md                         # Setup instructions
```

---

## Model: RecipePhoto

```python
class RecipePhoto(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')  # Cloudinary field
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

---

## Authentication & Authorization

**Protected Routes:**
- `/` (home) — LoginRequiredMixin
- `/edit/<id>/` — LoginRequiredMixin + IsOwnerOrAdminMixin
- `/delete/<id>/` — LoginRequiredMixin + IsOwnerOrAdminMixin
- `/accounts/login/` — Django auth login
- `/admin/` — Staff-only access

**User Groups:**
- **Album Admin** — Full access to all photos (created automatically)
- **Staff** — Access to Django admin
- **Authenticated Users** — Can upload and manage own photos

---

## Environment Variables (Production on Render)

Set these in Render Settings → Environment:

```env
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=your-service.onrender.com
USE_CLOUDINARY=True

# Database (Render Postgres URL)
DATABASE_URL=postgres://user:password@host:port/dbname

# Cloudinary Credentials
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

---

## Deployment Steps (Render)

1. **Create Web Service on Render:**
   - Connect GitHub repo: `karlreycolminar-ui/cloud`
   - Select branch: `main`

2. **Configure Environment:**
   - Set env vars above in Render dashboard

3. **Deploy:**
   - Render auto-builds using `pip install -r requirements.txt`
   - Starts server via `Procfile`: `gunicorn recipe_project.wsgi --log-file -`

4. **Post-Deploy Migrations (Render Shell):**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Verify:**
   - Visit live URL
   - Log in with superuser credentials
   - Upload and manage photos

---

## Testing Locally

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed sample data (optional)
python manage.py seed_photos

# Run dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in.

---

## Key Code Examples

### CBV with RBAC (PhotoUpdateView)
```python
class PhotoUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = RecipePhoto
    form_class = RecipePhotoForm
    template_name = 'gallery/edit.html'
    success_url = reverse_lazy('gallery:home')
    login_url = 'login'
```

### RBAC Mixin
```python
class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff
```

### Template Conditional (No Parentheses)
```django
{% if request.user.is_authenticated %}
    {% if request.user.is_staff or request.user == photo.owner %}
        <a href="{% url 'gallery:edit' photo.id %}">Edit</a>
        <a href="{% url 'gallery:delete' photo.id %}">Delete</a>
    {% endif %}
{% endif %}
```

---

## Performance & Security

- **Static Files:** WhiteNoise compression for fast serving
- **Database Queries:** Django ORM with select_related/prefetch_related ready
- **HTTPS:** Render enforces SSL
- **CSRF Protection:** Django CSRF middleware enabled
- **SQL Injection:** Parameterized queries via ORM
- **Environment Secrets:** Cloudinary keys stored in env vars (never committed)

---

## Troubleshooting

### Image Upload Not Working
- Verify `USE_CLOUDINARY=True` in production
- Check Cloudinary credentials in Render env vars
- Test locally with `USE_CLOUDINARY=False` and `FileSystemStorage`

### 404 on Edit/Delete
- Ensure user is authenticated (redirect to `/accounts/login/`)
- Verify user owns the photo (check `RecipePhoto.owner`)

### Database Connection Error
- Verify `DATABASE_URL` is set on Render
- Run `python manage.py migrate` in Render shell after first deploy

### Static Files Not Loading
- WhiteNoise is configured; static files auto-collected during deploy
- Check `STATIC_URL` and `STATIC_ROOT` in `settings.py`

---

## Authors & Attribution

**Developer:** Karl Rey Colminar  
**Project:** Cloud-Render Photo Album (Production-Ready Django CRUD)  
**Created:** May 2026

---

## Grading Checklist

- [x] Repository link provided
- [ ] Live URL accessible (after Render deployment)
- [x] Class-Based Views implemented
- [x] RBAC enforced (LoginRequiredMixin, IsOwnerOrAdminMixin)
- [x] Cloudinary integration configured
- [x] PostgreSQL ready for production
- [x] Deployment artifacts (Procfile, render.yaml, .env.example)
- [x] Documentation complete
- [ ] Sample photos seeded (via `seed_photos` command)
- [ ] Live instance active during grading period

---

**Submission Status:** Ready for deployment  
**Last Updated:** May 25, 2026
