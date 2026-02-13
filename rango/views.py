from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('rango:index')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category

            if page.url and not page.url.startswith(('http://', 'https://')):
                page.url = 'http://' + page.url

            page.views = 0
            page.save()

            return redirect('rango:show_category', category_name_slug=category.slug)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def goto(request):
    page_id = request.GET.get('page_id')

    if page_id:
        try:
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)
        except Page.DoesNotExist:
            pass

    return redirect(reverse('rango:index'))
