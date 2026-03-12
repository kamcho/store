from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ProductVariant, ContactMessage

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

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'cart_id', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('phone', 'name', 'email', 'message', 'cart_id')
    readonly_fields = ('created_at', 'display_cart_items')
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('phone', 'name', 'email', 'cart_id')
        }),
        ('Message Content', {
            'fields': ('message',)
        }),
        ('Cart Snapshot', {
            'fields': ('display_cart_items',),
            'description': 'These items were in the user\'s cart when this message was sent.'
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )

    def display_cart_items(self, obj):
        from django.utils.safestring import mark_safe
        if not obj.cart_items:
            return "No items"
        
        html = '<table style="width:100%; border-collapse: collapse;">'
        html += '<tr style="background:#f8f8f8;"><th style="padding:8px; border:1px solid #ddd;">Product</th><th style="padding:8px; border:1px solid #ddd;">Variant</th><th style="padding:8px; border:1px solid #ddd;">Qty</th><th style="padding:8px; border:1px solid #ddd;">Price</th></tr>'
        for item in obj.cart_items:
            html += f'<tr>'
            html += f'<td style="padding:8px; border:1px solid #ddd;">{item.get("product")}</td>'
            html += f'<td style="padding:8px; border:1px solid #ddd;">{item.get("variant")}</td>'
            html += f'<td style="padding:8px; border:1px solid #ddd;">{item.get("quantity")}</td>'
            html += f'<td style="padding:8px; border:1px solid #ddd;">KSH {item.get("price"):,.0f}</td>'
            html += f'</tr>'
        html += '</table>'
        return mark_safe(html)
    
    display_cart_items.short_description = 'Cart Items Snapshot'
