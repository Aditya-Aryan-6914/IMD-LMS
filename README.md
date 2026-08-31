# CapNova

**CapNova** is a Django-based digital capacity building and learning management system (LMS) designed to support organizational training, competency development, and knowledge sharing through a centralized web platform. It provides trainers and learners with an integrated environment to manage training programs, track progress, and facilitate digital learning experiences.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database](#database)
- [API Routes](#api-routes)
- [Authentication](#authentication)
- [Static Files & Templates](#static-files--templates)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

CapNova is built to address the need for organizations to centralize their training and learning initiatives. Whether you're managing corporate training programs, employee onboarding, competency development, or continuous professional development (CPD), CapNova provides a scalable and maintainable foundation.

### Core Objectives

- **Centralized Learning Portal**: Create a single platform for all training and learning content
- **User Management**: Support multiple user roles (admins, trainers, trainees, learners)
- **Progress Tracking**: Monitor learner engagement and competency development
- **Content Management**: Organize and deliver training materials efficiently
- **Knowledge Sharing**: Foster organizational knowledge transfer and collaboration
- **Scalability**: Built on Django with SQLite (development) and extensible database support (PostgreSQL, MySQL for production)

---

## Features

### Current Features (v0.1.0)

- ✅ **User Authentication**: Django-powered authentication system with secure login/logout
- ✅ **Admin Dashboard**: Django admin panel for system management
- ✅ **Static File Management**: Serve CSS, JavaScript, and media assets
- ✅ **Template-Based Rendering**: Django templating engine for dynamic content
- ✅ **Responsive Design**: Base template with CSS framework for modern UI
- ✅ **SQLite Database**: Lightweight database for development and testing

### Planned Features (Roadmap)

- 🔄 User role-based access control (RBAC)
- 🔄 Training program creation and management
- 🔄 Learner progress tracking and analytics
- 🔄 Certificate generation
- 🔄 Attendance management
- 🔄 Competency assessment tools
- 🔄 Real-time notifications
- 🔄 API endpoints for mobile integration
- 🔄 Advanced reporting and analytics dashboards

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend Framework** | Django | 6.1+ |
| **Language** | Python | 3.8+ |
| **Database** | SQLite (dev) / PostgreSQL or MySQL (prod) | Latest |
| **Frontend** | HTML5, CSS3, JavaScript | ES6+ |
| **Server** | Django Development Server / Gunicorn (prod) | - |
| **Template Engine** | Django Templates | Bundled with Django |

### Optional Dependencies

- ASGI support via `asgiref` (3.12.1+)
- REST Framework (for future API development)
- Celery (for asynchronous tasks)
- Redis (for caching and task queues)

---

## Project Structure

```
CapNova/
├── CapNova/                          # Django project root
│   ├── CapNova/                      # Main Django app configuration
│   │   ├── __init__.py              # Python package marker
│   │   ├── settings.py              # Django configuration (SECRET_KEY, DATABASES, APPS, etc.)
│   │   ├── urls.py                  # URL routing configuration
│   │   ├── views.py                 # View handlers (currently home view)
│   │   ├── wsgi.py                  # WSGI application entry point (production)
│   │   ├── asgi.py                  # ASGI application entry point (async support)
│   │   └── __pycache__/             # Python bytecode cache
│   ├── db.sqlite3                   # SQLite database file (development only)
│   ├── manage.py                    # Django management CLI tool
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git ignore rules
│   ├── static/                      # Static files (served to browser)
│   │   ├── css/
│   │   │   └── base.css            # Global stylesheet
│   │   └── assets/
│   │       └── base/               # Images, fonts, and other assets
│   ├── templates/                   # HTML templates (Django Jinja2)
│   │   ├── base.html               # Base template (inherited by other templates)
│   │   └── auth/
│   │       ├── index.html          # Home/landing page
│   │       └── traineeLogin.html   # Trainee login page
│   └── [future apps]/              # Additional Django apps (to be created)
├── .venv/                           # Virtual environment (local development)
├── .git/                            # Git repository
└── README.md                        # This file
```

### Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| `CapNova/CapNova/` | Project-level Django configuration |
| `static/` | CSS, JavaScript, images, fonts - served directly to browsers |
| `templates/` | HTML templates using Django Jinja2 syntax |
| `db.sqlite3` | Local SQLite database (development only, don't commit to production) |
| `.venv/` | Python virtual environment (local only, excluded from git) |

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
  ```bash
  python --version  # Verify installation
  ```
- **pip**: Python package manager (comes with Python)
  ```bash
  pip --version  # Verify installation
  ```
- **Git**: Version control system
  ```bash
  git --version  # Verify installation
  ```

### Optional but Recommended

- **Virtual Environment Tool**: `virtualenv` or `venv` (included with Python 3.3+)
- **Database Client**: SQLite Browser for exploring database contents
- **Code Editor**: VS Code, PyCharm, Sublime Text, or similar

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/CapNova.git
cd CapNova
```

### Step 2: Create a Virtual Environment

It's best practice to use a virtual environment to isolate project dependencies.

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### Step 3: Upgrade pip, setuptools, and wheel

```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Project Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Navigate to Project Directory

```bash
cd CapNova
```

### Step 6: Apply Database Migrations

Django uses migrations to manage database schema changes.

```bash
python manage.py migrate
```

### Step 7: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- **Username**: Choose a username
- **Email**: Enter your email
- **Password**: Create a strong password
- **Confirm Password**: Re-enter your password

### Step 8: Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

### Step 9: Access the Application

- **Home Page**: `http://127.0.0.1:8000/`
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/` (login with superuser credentials)
- **Authentication URLs**: `http://127.0.0.1:8000/auth/` (Django auth routes)

---

## Configuration

### Django Settings

All Django configuration is located in `CapNova/CapNova/settings.py`.

#### Critical Settings

| Setting | Current Value | Notes |
|---------|--------------|-------|
| `DEBUG` | `True` | ⚠️ Must be `False` in production |
| `SECRET_KEY` | [Auto-generated] | ⚠️ Change in production |
| `ALLOWED_HOSTS` | `[]` | Add your domain(s) before deploying |
| `DATABASES` | SQLite (dev) | Change to PostgreSQL/MySQL for production |
| `INSTALLED_APPS` | Django defaults | Add custom apps here |
| `STATIC_URL` | `/static/` | URL prefix for static files |

### Environment Variables (Production)

For production, create a `.env` file in the project root:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/capnova
```

Load these using `python-dotenv`:

```python
# In settings.py
import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
```

---

## Usage

### Running the Development Server

```bash
# From the CapNova/ directory
python manage.py runserver
```

### Making Migrations (After Model Changes)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser

```bash
python manage.py createsuperuser
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

### Clearing Cache

```bash
python manage.py clear_cache
```

### Interactive Django Shell

```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
users = User.objects.all()
```

---

## Database

### SQLite (Development)

- **File Location**: `CapNova/db.sqlite3`
- **Use Case**: Local development and testing
- **Advantages**: No setup required, single file storage
- **Limitations**: Single user, not suitable for production

### PostgreSQL (Recommended for Production)

**Installation:**
```bash
pip install psycopg2-binary
```

**Update settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'capnova_db',
        'USER': 'capnova_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL (Alternative for Production)

**Installation:**
```bash
pip install mysqlclient
```

**Update settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'capnova_db',
        'USER': 'capnova_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Database Backup & Restore

**Backup SQLite:**
```bash
cp CapNova/db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

**Dump PostgreSQL:**
```bash
pg_dump -U capnova_user capnova_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

---

## API Routes

### Current Endpoints

| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `/` | GET | `views.home` | Home/Landing page (renders `auth/index.html`) |
| `/admin/` | GET, POST | Django Admin | Admin dashboard and user management |
| `/auth/` | GET, POST | Django Auth URLs | Login, logout, password reset |

### Authentication Routes

| Endpoint | Purpose |
|----------|---------|
| `/auth/login/` | User login |
| `/auth/logout/` | User logout |
| `/auth/password_change/` | Change password |
| `/auth/password_reset/` | Reset forgotten password |

### Future API Endpoints (Planned)

```
POST /api/v1/users/                      # Create user
GET  /api/v1/users/<id>/                 # Get user details
GET  /api/v1/courses/                    # List courses
POST /api/v1/courses/                    # Create course
GET  /api/v1/courses/<id>/progress/      # User progress
POST /api/v1/assignments/submit/         # Submit assignment
```

---

## Authentication

### Current Authentication System

CapNova uses Django's built-in authentication system with the following features:

- **Password Hashing**: PBKDF2 algorithm (secure, industry-standard)
- **Session Management**: Database-backed sessions
- **CSRF Protection**: Cross-Site Request Forgery tokens on all forms
- **User Roles**: Django Groups and Permissions

### User Management

**Create a new user programmatically:**

```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password123'
)
```

**Assign permissions to users:**

```python
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create or assign permission
permission = Permission.objects.get(codename='add_course')
user.user_permissions.add(permission)
```

### Future Authentication Features

- Social login (Google, GitHub, Microsoft)
- Two-factor authentication (2FA)
- OAuth2 integration
- SAML support for enterprise SSO

---

## Static Files & Templates

### Static Files

**Location**: `CapNova/static/`

**Structure:**
```
static/
├── css/
│   └── base.css              # Global stylesheet
├── assets/
│   └── base/                 # Images, icons, fonts
└── js/                       # JavaScript files (to be added)
```

**Serving Static Files in Development:**

Django automatically serves static files when `DEBUG=True`. Access them at:
```
http://localhost:8000/static/css/base.css
http://localhost:8000/static/assets/base/image.png
```

**Serving Static Files in Production:**

1. Run: `python manage.py collectstatic`
2. Configure your web server (Nginx, Apache) to serve from `STATIC_ROOT`

### Templates

**Location**: `CapNova/templates/`

**Structure:**
```
templates/
├── base.html                 # Base template (parent)
└── auth/
    ├── index.html           # Home page
    └── traineeLogin.html    # Trainee login page
```

**Base Template Inheritance:**

```django
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <h1>Welcome to CapNova</h1>
{% endblock %}
```

---

## Development

### Project Workflow

1. **Create a new branch**:
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Make your changes** to templates, views, or models

3. **Test locally**:
   ```bash
   python manage.py runserver
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "Add feature description"
   ```

5. **Push to GitHub**:
   ```bash
   git push origin feature/feature-name
   ```

6. **Create a Pull Request** on GitHub

### Creating Django Apps

To extend CapNova with new functionality, create Django apps:

```bash
python manage.py startapp courses
python manage.py startapp learners
python manage.py startapp assignments
```

Then add them to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'courses',
    'learners',
    'assignments',
]
```

### Database Migrations Workflow

```bash
# After modifying models
python manage.py makemigrations

# Review generated migration file (optional)
cat CapNova/migrations/0001_initial.py

# Apply migrations
python manage.py migrate

# View migration history
python manage.py showmigrations
```

### Debugging

**Enable debug toolbar (development):**

```bash
pip install django-debug-toolbar
```

Update `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

**Python debugger:**

```python
# In your view or function
import pdb; pdb.set_trace()
# Or in Python 3.7+:
breakpoint()
```

---

## Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Switch to PostgreSQL/MySQL database
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Run security check: `python manage.py check --deploy`
- [ ] Set up environment variables with `.env` file
- [ ] Configure HTTPS/SSL certificate
- [ ] Set up database backups

### Deploying to Heroku

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create capnova-app

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploying to AWS, Azure, or DigitalOcean

Refer to each platform's Django deployment guide:
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [DigitalOcean App Platform](https://docs.digitalocean.com/products/app-platform/)

### Using Gunicorn (WSGI Server)

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn CapNova.wsgi:application --bind 0.0.0.0:8000
```

### Using Nginx as Reverse Proxy

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/CapNova/staticfiles/;
    }
}
```

---

## Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'django'` | Django not installed | Run `pip install -r requirements.txt` |
| `django.db.utils.OperationalError: no such table` | Migrations not applied | Run `python manage.py migrate` |
| `Secret key exposed in settings` | Hardcoded secret key | Use environment variables or `.env` file |
| `Static files not loading` | DEBUG=False without collectstatic | Run `python manage.py collectstatic` |
| `Port 8000 already in use` | Another process using port | Use `python manage.py runserver 8001` |
| `CSRF verification failed` | CSRF token missing in form | Include `{% csrf_token %}` in forms |

### Debug Commands

```bash
# Check Django project integrity
python manage.py check

# List all installed apps
python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"

# View database tables
python manage.py dbshell
# Then: .tables (SQLite) or \dt (PostgreSQL)

# Clear cache
python manage.py clear_cache

# Reset app database (caution: deletes all data)
python manage.py migrate <app_name> zero
```

---

## Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork** the repository on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** with clear, descriptive commits
4. **Write tests** for new features
5. **Submit a Pull Request** with a description of changes

### Code Style

- Follow [PEP 8](https://pep8.org/) for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic

### Commit Message Format

```
git commit -m "Type: Brief description (max 50 chars)

Detailed explanation of changes (if needed).
Fixes #issue_number (if applicable)
"
```

**Types**: feat, fix, docs, style, refactor, test, chore

---

## License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.

You are free to use, modify, and distribute this project, provided you include the original license notice.

---

## Support & Contact

- **Issues**: Report bugs and feature requests on [GitHub Issues](https://github.com/yourusername/CapNova/issues)
- **Discussions**: Join our community discussions on [GitHub Discussions](https://github.com/yourusername/CapNova/discussions)
- **Email**: contact@capnova.com

---

## Changelog

### Version 0.1.0 (Current)
- Initial Django project setup with authentication
- Base template and CSS styling
- SQLite database configuration
- Admin panel integration
- Home page and trainee login page

### Planned Releases

**v0.2.0**: User role management and permissions
**v0.3.0**: Course and training program management
**v0.4.0**: Progress tracking and analytics
**v1.0.0**: Full production-ready LMS

---

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Inspired by leading LMS platforms
- Thanks to all contributors and community members

---

**Last Updated**: 2026-08-31  
**Maintained by**: [Your Name/Organization]
