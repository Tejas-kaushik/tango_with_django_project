from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.forms import UserForm, UserProfileForm
from django.http import HttpResponse
from django.utils import timezone
import datetime


# --- CH10: Session-based visitor counter helper ---
def visitor_session_handler(request):
    visits = request.session.get('visits', 0)
    last_visit = request.session.get('last_visit')

    if last_visit:
        try:
            last_visit_time = datetime.datetime.fromisoformat(last_visit)
        except ValueError:
            # If something weird got stored, reset
            last_visit_time = timezone.now()

        # count a new visit only if >= 1 day has passed
        if (timezone.now() - last_visit_time).days >= 1:
            visits += 1
            request.session['visits'] = visits
            request.session['last_visit'] = timezone.now().isoformat()
    else:
        # first ever visit
        visits = 1
        request.session['visits'] = visits
        request.session['last_visit'] = timezone.now().isoformat()

    return visits
# --- END CH10 helper ---


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # CH10: update + get visits count
    visits = visitor_session_handler(request)

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
        'visits': visits,  # <-- NEW
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # CH10: show the same visits count on About
    visits = visitor_session_handler(request)
    return render(request, 'rango/about.html', {'visits': visits})


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


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('rango:index')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('rango:index')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
