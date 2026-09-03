# CapNova — IMD Training & Capacity Building Portal

CapNova is a Django LMS built for the India Meteorological Department (IMD)
to run internal and public training: courses, MCQ assessments, completion
certificates, and homepage announcements, with three user roles (Trainee,
Trainer, Admin).

## What's here

- **Accounts** — email-based login (no usernames), self-registration as
  Trainee, Trainer, or Public User, admin approval for Trainers and
  employee Trainees, role-based dashboards, password reset by email.
- **Courses** — subjects and courses, admin assigns a trainer to each
  course, trainees browse and enrol, trainers upload library resources
  (recordings/slides/documents), trainee feedback, a competency map
  (subject → qualified trainers).
- **Assessments** — trainers build MCQ questionnaires with a deadline,
  trainees attempt them, auto-scored, trainers see participation/results.
- **Certificates** — trainer marks an enrollment complete; a certificate
  is generated (downloadable PDF) and publicly verifiable by number.
- **Announcements** — flat list on the public homepage.

"Public User" isn't a separate role — it's a Trainee record flagged
`is_public_user=True` for people outside IMD, auto-approved instead of
needing admin sign-off.

## Tech stack

Django 6.1 · SQLite (dev) · Pillow (profile photos) · ReportLab
(certificate PDFs)

## Getting started

```bash
cd CapNova
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # asks for email + full name, no username
python manage.py runserver
```

Visit `/` for the homepage, `/register/` to sign up, `/admin/` for the
Django admin.

### Email (password reset)

Reset emails print to the console by default — nothing to configure for
local dev. To send real email, set `EMAIL_HOST_USER` and
`EMAIL_HOST_PASSWORD` as environment variables (see `.env.example` for
the full list and `CapNova/settings.py` for how it's wired up).

### Optional: editor type-checking

`requirements-dev.txt` adds `django-stubs` for better Pylance/Pyright
support in your editor. Not needed to run the app.

```bash
pip install -r requirements-dev.txt
```

## Project layout

```
CapNova/
  accounts/       # User model, profiles, auth, dashboards, admin approval
  courses/        # Subjects, courses, enrollment, library, certificates
  assessments/    # Questionnaires, questions, attempts, scoring
  announcements/  # Homepage announcements
  templates/      # One folder per app, plus shared partials/base.html
  static/css/     # dashboard.css, register.css
```

## Known gaps

- No production static/media serving set up (Django serves them directly
  only when `DEBUG=True`).
- `ALLOWED_HOSTS` is empty — fine for local dev, set it before deploying.
- No automated test suite yet (`tests.py` in each app is still an empty
  stub).
- In-app notifications are just the homepage list — no per-user
  read/unread state yet.
