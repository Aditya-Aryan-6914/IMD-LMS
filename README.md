# CapNova

CapNova is a Django-based digital capacity building and learning management portal designed to support organizational training, competency development, and knowledge sharing through a centralized web platform.

## Overview

This project is intended to provide a structured system for:
- managing learning content and training programs
- tracking learner progress and competencies
- supporting organizational knowledge sharing
- delivering a centralized digital training experience

## Tech Stack

- Python
- Django
- SQLite (default development database)

## Project Structure

- `CapNova/` — Django project folder
- `manage.py` — Django management entry point
- `db.sqlite3` — local SQLite database for development

## Getting Started

1. Clone the repository
2. Create a virtual environment
3. Install project dependencies
4. Apply database migrations
5. Run the development server

Example:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

## Notes

This repository is currently a basic Django project scaffold and can be extended with apps, models, templates, and user workflows for the CapNova platform.
