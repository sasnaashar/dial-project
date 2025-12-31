import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .models import Listing, Category, CategoryTemplate
from .forms import ListingForm, ContactForm, RegisterForm, SearchForm, CategoryForm


# ============================================================
# LOGIN
# ============================================================
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")

    return render(request, "main/login.html", {"form": form})


# ============================================================
# LOGOUT
# ============================================================
def logout_user(request):
    logout(request)
    return redirect("login")


# ============================================================
# HOME
# ============================================================
def home(request):
    categories = Category.objects.all()
    featured = Listing.objects.filter(featured=True).order_by("-id")[:6]

    if not featured.exists():
        featured = Listing.objects.all().order_by("-id")[:6]

    return render(request, "main/home.html", {
        "categories": categories,
        "featured": featured,
    })


# ============================================================
# LISTINGS
# ============================================================
def listings(request):
    results = Listing.objects.all().order_by("-id")
    q = request.GET.get("q", "")

    if q:
        results = results.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, "main/listings.html", {"results": results})


# ============================================================
# BUSINESS PAGE (DialAddress Style)
# ============================================================
def business_page(request, slug):
    item = get_object_or_404(Listing, slug=slug)
    return render(request, "main/business_page.html", {"item": item})


# ============================================================
# CATEGORY LISTINGS
# ============================================================
def category_listings(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if category.template:
        return redirect("category_template", template_slug=category.template.slug)

    listings = Listing.objects.filter(category=category).order_by("-id")

    return render(request, "main/category_listings.html", {
        "category": category,
        "listings": listings,
    })


# ============================================================
# CATEGORY TEMPLATE PAGE
# ============================================================
def category_template_page(request, template_slug):
    template_obj = get_object_or_404(CategoryTemplate, slug=template_slug)

    file_path = os.path.join(settings.MEDIA_ROOT, template_obj.html_file.name)
    html_code = ""

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html_code = f.read()

    return render(request, "main/category_template.html", {
        "template": template_obj,
        "html_code": html_code,
    })


# ============================================================
# CONTACT
# ============================================================
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Message sent!")
        return redirect("contact")

    return render(request, "main/contact.html", {"form": form})


# ============================================================
# SEARCH
# ============================================================
def search(request):
    form = SearchForm(request.GET or None)
    results = Listing.objects.none()

    if form.is_valid():
        results = Listing.objects.all()

        q = form.cleaned_data.get("q")
        if q:
            results = results.filter(title__icontains=q)

    return render(request, "main/search.html", {
        "form": form,
        "results": results,
    })


# ============================================================
# REGISTER
# ============================================================
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "main/register.html", {"form": form})


# ============================================================
# ADD LISTING (LOGIN ONLY)
# ============================================================
@login_required
def add_listing(request):
    form = ListingForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        listing = form.save()
        return redirect("business_page", slug=listing.slug)

    return render(request, "main/add_listing.html", {"form": form})


# ============================================================
# DASHBOARD (LOGIN ONLY — NO STAFF)
# ============================================================
@login_required
def dashboard_home(request):
    return render(request, "main/dashboard_home.html", {
        "total_listings": Listing.objects.count(),
        "total_categories": Category.objects.count(),
        "featured": Listing.objects.filter(featured=True).count(),
    })


@login_required
def dashboard_listings(request):
    return render(request, "main/dashboard_listings.html", {
        "listings": Listing.objects.all().order_by("-id")
    })


@login_required
def dashboard_add_listing(request):
    form = ListingForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("dashboard_listings")

    return render(request, "main/dashboard_listing_form.html", {
        "form": form,
        "title": "Add Listing",
    })


@login_required
def dashboard_edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    form = ListingForm(request.POST or None, request.FILES or None, instance=listing)

    if form.is_valid():
        form.save()
        return redirect("dashboard_listings")

    return render(request, "main/dashboard_listing_form.html", {
        "form": form,
        "title": "Edit Listing",
    })


@login_required
def dashboard_delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    listing.delete()
    return redirect("dashboard_listings")


@login_required
def dashboard_toggle_feature(request, id):
    listing = get_object_or_404(Listing, id=id)
    listing.featured = not listing.featured
    listing.save()
    return redirect("dashboard_listings")


# ============================================================
# CATEGORY ADMIN (LOGIN ONLY)
# ============================================================
@login_required
def category_admin_list(request):
    return render(request, "main/category_admin_list.html", {
        "categories": Category.objects.all().order_by("name")
    })


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("category_admin_list")

    return render(request, "main/category_form.html", {
        "form": form,
        "title": "Add Category",
    })


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect("category_admin_list")

    return render(request, "main/category_form.html", {
        "form": form,
        "title": "Edit Category",
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("category_admin_list")

# ============================================================
# ABOUT PAGE (REQUIRED – DO NOT DELETE)
# ============================================================
def about(request):
    """
    Simple About page.
    This MUST exist because urls.py references it.
    """
    return render(request, "main/about.html")