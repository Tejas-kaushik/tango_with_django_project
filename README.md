# tango_with_django_project
# Rango (Tango with Django)

This is my implementation of the *Tango with Django* Rango project.

## Features implemented
- Categories and Pages models (+ admin integration)
- Templates + template inheritance (base.html)
- Static files (CSS/images)
- Forms to add categories/pages
- Page view tracking via `goto` view
- Custom template tags (top categories)
- Authentication (register/login/logout) + restricted page
- Sessions/cookies (visit counter)

## Requirements
- Python: 3.x (I used 3.11)
- Django: 2.2.28

## Setup (Conda example)
```bash
conda create -n rango python=3.11
conda activate rango
pip install django==2.2.28
