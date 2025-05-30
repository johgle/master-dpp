from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'design', 'description', 'qr_code')

# Alternativt:
# admin.site.register(Product)
