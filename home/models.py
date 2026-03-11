from django.db import models
from django.urls import reverse

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('pre_order', 'Pre-Order'),
        ('discontinued', 'Discontinued'),
    ]

    category = models.ForeignKey(ProductCategory, on_delete=models.RESTRICT)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    # Product details
    warranty_period = models.PositiveIntegerField(help_text="Warranty in months", default=12)
    features = models.JSONField(default=list, blank=True, help_text="List of key features")
    
    # SEO and Marketing
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_features_list(self):
        """Return features as a list of strings for form display."""
        if isinstance(self.features, list):
            return self.features
        elif isinstance(self.features, str):
            # Handle case where features might be stored as string
            return [self.features]
        else:
            return []

    def get_starting_price(self):
        """Return the price of the cheapest active variant."""
        active_variants = self.variants.filter(is_active=True).order_by('price')
        if active_variants.exists():
            return active_variants.first().get_current_price()
        return None

    def get_price_range(self):
        """Return a tuple of (min_price, max_price) for all variants."""
        active_variants = self.variants.filter(is_active=True)
        if not active_variants.exists():
            return None, None
        prices = [v.get_current_price() for v in active_variants]
        return min(prices), max(prices)

    def is_in_stock(self):
        """Return True if any variant is in stock."""
        return any(v.stock_quantity > 0 and v.availability == 'in_stock' for v in self.variants.filter(is_active=True))

    def get_discount_percentage(self):
        """Return discount percentage of the first variant if it has one."""
        first = self.variants.filter(is_active=True).first()
        if first:
            return first.get_discount_percentage()
        return 0

    def get_main_image(self):
        """Return the main product image, or the first image, or None."""
        main = self.images.filter(is_main_image=True).first()
        if main:
            return main
        return self.images.first()

    def get_features_list(self):
        """Return features as a proper Python list, handling stringified JSON."""
        import json
        if isinstance(self.features, list):
            return self.features
        if isinstance(self.features, str):
            try:
                parsed = json.loads(self.features)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                pass
        return []
    
    def get_category_hierarchy_slugs(self):
        """Return a list of slugs for the product's category and all its ancestors."""
        slugs = []
        curr = self.category
        while curr:
            slugs.append(curr.slug)
            curr = curr.parent
        return slugs


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main_image = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, related_name='variant_specifications', null=True, blank=True)
    category = models.CharField(max_length=100, help_text="e.g., Display, Processor, Camera")
    name = models.CharField(max_length=100, help_text="e.g., Screen Size, CPU Type")
    value = models.CharField(max_length=200, help_text="e.g., 6.7 inches, Snapdragon 888")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'category', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.category}: {self.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text="e.g. 55-inch, 65-inch, 128GB, 256GB")
    model_code = models.CharField(max_length=50, unique=True, help_text="Specific model code for this variant")
    
    # Pricing (overrides base product if specified)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    availability = models.CharField(max_length=20, choices=Product.AVAILABILITY_CHOICES, default='in_stock')
    
    # Variant specific specs
    specifications = models.JSONField(default=dict, blank=True, help_text="e.g. {'screen_size': '55-inch', 'resolution': '4K'}")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price']

    def save(self, *args, **kwargs):
        if not self.model_code:
            # Generate SKU: PRODUCT-NAME-VARIANT-NAME-NUMBER
            from django.utils.text import slugify
            import random
            import string
            
            base_sku = slugify(self.product.name)
            if self.name:
                base_sku += f"-{slugify(self.name)}"
            
            base_sku = base_sku.upper()[:40]
            
            # Ensure uniqueness
            sku = base_sku
            counter = 1
            while ProductVariant.objects.filter(model_code=sku).exists():
                suffix = f"-{counter}"
                sku = f"{base_sku[:50-len(suffix)]}{suffix}"
                counter += 1
            
            self.model_code = sku
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    def get_current_price(self):
        """Return sale price if available, otherwise regular price."""
        return self.sale_price if self.sale_price else self.price
    
    def get_discount_percentage(self):
        """Calculate discount percentage."""
        if self.sale_price and self.price > 0:
            return round((self.price - self.sale_price) / self.price * 100, 1)
        return 0


class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='variant_images/')
    alt_text = models.CharField(max_length=200, blank=True, help_text="Describe the image for SEO")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which to display this image")
    is_main_image = models.BooleanField(default=False, help_text="Set as main image for this variant")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"
        
    def __str__(self):
        return f"Image for {self.variant.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


