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
    short_description = models.CharField(max_length=500)
    
    # Samsung Specifics
    model_code = models.CharField(max_length=50, unique=True, help_text="e.g. SM-S908E")
    series = models.CharField(max_length=50, blank=True, help_text="e.g. Galaxy S, Galaxy Z, Neo QLED")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    
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

    def get_current_price(self):
        return self.sale_price if self.sale_price else self.price

    def is_in_stock(self):
        return self.stock_quantity > 0 and self.availability == 'in_stock'

    def get_discount_percentage(self):
        if self.sale_price and self.price:
            return round((self.price - self.sale_price) / self.price * 100, 1)
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
    category = models.CharField(max_length=100, help_text="e.g., Display, Processor, Camera")
    name = models.CharField(max_length=100, help_text="e.g., Screen Size, CPU Type")
    value = models.CharField(max_length=200, help_text="e.g., 6.7 inches, Snapdragon 888")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'category', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.category}: {self.name}"


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


