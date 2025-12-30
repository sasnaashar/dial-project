"""
URL configuration for dialproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""dialproject URL Configuration - full website"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [

    # ====================================================
    # PUBLIC PAGES
    # ====================================================
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('listings/', views.listings, name='listings'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),

    # ====================================================
    # BUSINESS PAGE (Dial style)
    # ====================================================
    path('b/<slug:slug>/', views.business_page, name='business_page'),

    # ====================================================
    # CATEGORY LISTINGS
    # ====================================================
    path('category/<slug:slug>/', views.category_listings, name='category_listings'),

    # ====================================================
    # CUSTOM UPLOADED TEMPLATE (Dial style)
    # ====================================================
    path('t/<slug:template_slug>/', views.category_template_page, name='category_template'),

    # ====================================================
    # PUBLIC ADD LISTING
    # ====================================================
    path('add-listing/', views.add_listing, name='add_listing'),

    # ====================================================
    # AUTHENTICATION
    # ====================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    # ====================================================
    # DASHBOARD
    # ====================================================
    path('dashboard/', views.dashboard_home, name='dashboard_home'),

    # Listings
    path('dashboard/listings/', views.dashboard_listings, name='dashboard_listings'),
    path('dashboard/listings/add/', views.dashboard_add_listing, name='dashboard_add_listing'),
    path('dashboard/listings/edit/<int:id>/', views.dashboard_edit_listing, name='dashboard_edit_listing'),
    path('dashboard/listings/delete/<int:id>/', views.dashboard_delete_listing, name='dashboard_delete_listing'),
    path('dashboard/listings/feature/<int:id>/', views.dashboard_toggle_feature, name='dashboard_toggle_feature'),

    # Category admin
    path('dashboard/categories/', views.category_admin_list, name='category_admin_list'),
    path('dashboard/categories/add/', views.category_create, name='category_create'),
    path('dashboard/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]

# ====================================================
# MEDIA FILES
# ====================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)