from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ==========================================================
# CATEGORY TEMPLATE (Admin uploads an HTML template file)
# ==========================================================
class CategoryTemplate(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # Admin uploads the HTML file (just like DialAddress)
    html_file = models.FileField(upload_to="category_templates/")

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if empty
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_template", args=[self.slug])


# ==========================================================
# CATEGORY MODEL
# Each category can have ONE assigned template
# ==========================================================
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    # Assign a custom template to this category
    template = models.ForeignKey(
        CategoryTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories"
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        # Auto slug from name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_listings", args=[self.slug])


# ==========================================================
# LISTING (Business page)
# Clean modern business profile page
# ==========================================================
class Listing(models.Model):
    title = models.CharField(max_length=200)

    # Unique business URL:  /b/<slug>/
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    image = models.ImageField(upload_to='listings/', blank=True, null=True)

    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Display on homepage
    featured = models.BooleanField(default=False)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate unique slug
        if not self.slug:
            base = slugify(self.title)
            slug_temp = base
            counter = 1

            # Ensure uniqueness
            while Listing.objects.filter(slug=slug_temp).exists():
                slug_temp = f"{base}-{counter}"
                counter += 1

            self.slug = slug_temp

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # Business page URL: /b/slug/
    def get_absolute_url(self):
        return reverse("business_page", args=[self.slug])


# ==========================================================
# CONTACT MESSAGE
# ==========================================================
class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created:%Y-%m-%d %H:%M}"