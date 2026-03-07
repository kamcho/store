from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, ProductSpecification

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.safestring import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Preview'

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 2

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sale_price', 'stock_quantity', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured', 'availability')
    search_fields = ('name', 'description', 'series', 'model_code')
    inlines = [ProductImageInline, ProductSpecificationInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description', 'price', 'sale_price', 'stock_quantity', 'availability', 'is_active', 'is_featured')
        }),
        ('Samsung Specifics', {
            'fields': ('model_code', 'series', 'warranty_period', 'features')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_main_image')
    list_filter = ('product', 'is_main_image')

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'name', 'value')
    list_filter = ('product', 'category')
    search_fields = ('product__name', 'name', 'value')
