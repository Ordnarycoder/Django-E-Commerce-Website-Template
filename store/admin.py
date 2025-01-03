from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductAdmin(admin.ModelAdmin):
    # Fields to be displayed in the product list
    list_display = ('name', 'brand', 'image_link', 'category', 'price', 'rate', 'seller', 'consideration_num', 'color')
    
    # Fields to filter by in the admin panel
    list_filter = ('category', 'brand', 'seller', 'color')
    
    # Fields to be used for searching
    search_fields = ('name', 'brand', 'category__name', 'color')
    
    # Fields layout in the product form
    fieldsets = (
        (None, {
            'fields': ('name', 'brand', 'category', 'price', 'color')
        }),
        ('Additional Information', {
            'classes': ('collapse',),
            'fields': ('product_link', 'rate', 'consideration_num', 'seller'),
        }),
    )

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)