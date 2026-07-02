# My Site - Django Blog Project

A Django-based web application featuring a blog system. It is fully configured for deployment on Render, utilizing WhiteNoise for static file serving and Backblaze B2 for media storage in production.

## Features

- **Blog App**: Core functionality for managing and displaying blog posts.
- **Environment Management**: Configuration managed via `.env` files using `django-environ`.
- **Production Ready**: 
  - Uses `dj-database-url` for easy database configuration in production (e.g., PostgreSQL on Render).
  - Integrated `WhiteNoise` for efficient serving of static assets.
  - Backblaze B2 integration using `django-storages` and `boto3` for handling user-uploaded media files securely.
- **Automated Build Script**: Includes a `build.sh` script to streamline deployment processes (installing dependencies, collecting static files, and running migrations).

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- virtualenv (recommended)

## Local Development Setup

1. **Clone the repository** (if applicable) and navigate to the project directory:
   ```bash
   cd my_site
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the base directory (where `manage.py` is located) and add your development settings. A typical local `.env` looks like:
   ```ini
   SECRET_KEY=your-local-secret-key
   IS_DEVELOPMENT=True
   ```
   *(In local development, SQLite is used by default and media is stored locally in the `/uploads/` directory.)*

5. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The site will be available at `http://127.0.0.1:8000/`.

## Deployment (Render & Backblaze)

This project is configured out-of-the-box for hosting on **Render**.

### 1. Build Script
The repository includes a `build.sh` script which Render uses to build the application:
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

### 2. Environment Variables for Production
When deploying to Render, set the following environment variables in your Render dashboard:

- `IS_DEVELOPMENT=False`
- `SECRET_KEY`: A strong, random secret key.
- `DATABASE_URL`: Your production database URL (provided by Render Postgres).
- `RENDER_EXTERNAL_HOSTNAME`: Provided by Render (used for `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`).

**For Backblaze B2 Media Storage:**
- `BACKBLAZE_S2_KEY_ID`: Your Backblaze Application Key ID.
- `BACKBLAZE_S2_SECRET_KEY`: Your Backblaze Application Key.
- `BACKBLAZE_S2_NAME`: Your Backblaze Bucket Name.
- `AWS_S3_REGION_NAME`: The region of your Backblaze bucket.

### 3. Render Web Service Configuration
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn my_site.wsgi:application` (make sure gunicorn is in your requirements)

## Project Structure

```
my_site/
├── blog/                   # Main blog application
├── my_site/                # Project settings and configurations
│   ├── settings.py         # Main configuration (local & production logic)
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI entry point for production
├── static/                 # Project-level static files (CSS, JS, Images)
├── templates/              # Global HTML templates
├── uploads/                # Local media upload directory
├── build.sh                # Deployment build script
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```
