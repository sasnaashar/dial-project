from django import forms
from .models import Listing, ContactMessage, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# -------------------------
# LISTING FORM
# -------------------------
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'image', 'phone', 'email', 'website',
            'category', 'address', 'city', 'state', 'featured'
        ]


# -------------------------
# CONTACT FORM
# -------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']


# -------------------------
# USER REGISTER FORM
# -------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# -------------------------
# SEARCH FORM
# -------------------------
class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Keyword',
        widget=forms.TextInput(attrs={'placeholder': 'Keywords...'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All categories'
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'State'})
    )


# -------------------------
# CATEGORY FORM (THE ONE YOU WERE MISSING)
# -------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'icon']