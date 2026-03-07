from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ProductReview, ServiceRequest

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
    list_display = ('name', 'slug', 'parent', 'display_order')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('parent', 'display_order')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sale_price', 'stock', 'is_active', 'is_new')
    list_filter = ('category', 'is_active', 'is_new', 'is_featured')
    search_fields = ('name', 'description', 'sku')
    inlines = [ProductImageInline, ProductSpecificationInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'sku', 'category', 'description', 'price', 'sale_price', 'stock', 'is_active', 'is_new', 'is_featured')
        }),
        ('Images', {
            'fields': ('image',)
        }),
        ('Specifications', {
            'fields': ('specifications',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    list_filter = ('product', 'is_primary')

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    list_filter = ('product',)
    search_fields = ('product__name', 'name', 'value')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'is_approved')
    list_filter = ('product', 'rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    actions = ['approve_reviews', 'unapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"

    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_reviews.short_description = "Unapprove selected reviews"

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'request_type', 'status', 'created_at')
    list_filter = ('request_type', 'status', 'created_at')
    search_fields = ('product__name', 'customer_name', 'customer_email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Request Details', {
            'fields': ('product', 'request_type', 'description', 'status')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
