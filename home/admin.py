from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ProductVariant

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

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True

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
    list_display = ('name', 'category', 'get_starting_price_display', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    inlines = [ProductVariantInline, ProductImageInline, ProductSpecificationInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def get_starting_price_display(self, obj):
        price = obj.get_starting_price()
        return f"KSH {price:,.2f}" if price else "N/A"
    get_starting_price_display.short_description = 'Starting Price'

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description', 'is_active', 'is_featured')
        }),
        ('Samsung Specifics', {
            'fields': ('warranty_period', 'features')
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
    list_display = ('product', 'variant', 'category', 'name', 'value')
    list_filter = ('product', 'variant', 'category')
    search_fields = ('product__name', 'variant__name', 'name', 'value')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'model_code', 'price', 'stock_quantity', 'is_active')
    list_filter = ('product', 'is_active', 'availability')
    search_fields = ('name', 'model_code', 'product__name')
