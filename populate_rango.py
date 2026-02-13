import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

def add_page(category, title, url, views=0):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_category(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'https://docs.python.org/3/tutorial/', 'views': 64},
        {'title': 'Learn Python', 'url': 'https://www.learnpython.org/', 'views': 32},
    ]

    django_pages = [
        {'title': 'Django Documentation', 'url': 'https://docs.djangoproject.com/', 'views': 64},
        {'title': 'Django Tutorial', 'url': 'https://docs.djangoproject.com/en/stable/intro/tutorial01/', 'views': 32},
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
    }

    for cat_name, cat_data in cats.items():
        c = add_category(cat_name, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    for c in Category.objects.all():
        print(f"- {c} ({c.views} views, {c.likes} likes)")
        for p in Page.objects.filter(category=c):
            print(f"  - {p.title} -> {p.url}")

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
