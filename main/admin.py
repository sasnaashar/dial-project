from django.contrib import admin
from .models import Listing, Category, ContactMessage

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','phone','featured','created_at')
    list_filter = ('featured','category')
    search_fields = ('title','description','city','state','phone','email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug','icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','created')
    readonly_fields = ('created',)
    