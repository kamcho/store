from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ProductVariant, ProductVariantImage, ContactMessage

class ProductForm(forms.ModelForm):
    features = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 6, 
            'placeholder': 'Enter one feature per line:\n\nPremium Dynamic AMOLED 2X Display\nSnapdragon 8 Gen 2 Processor\n5000mAh Battery\n5G Connectivity\nWireless Charging\nIP68 Water Resistance'
        }),
        required=False,
        help_text="Enter one feature per line"
    )

    specifications_raw = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 8, 
            'placeholder': 'Format: Category | Name | Value (one per line)\n\nDisplay | Screen Size | 6.8 inches\nPerformance | Processor | Snapdragon 8 Gen 3\nMemory | RAM | 12GB'
        }),
        required=False,
        help_text="Enter one specification per line in the format: Category | Name | Value"
    )
    
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 'features',
            'warranty_period', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product-url-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed product description'}),
            'warranty_period': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '12'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Build hierarchical category choices
        choices = [('', 'Select a category')]
        
        def add_category(category, level=0):
            prefix = "— " * level if level > 0 else ""
            choices.append((category.pk, f"{prefix}{category.name}"))
            for child in category.subcategories.all().order_by('name'):
                add_category(child, level + 1)
        
        top_categories = ProductCategory.objects.filter(parent=None).order_by('name')
        for cat in top_categories:
            add_category(cat)
            
        self.fields['category'].choices = choices
        
        # Convert list of features to multi-line string for the widget
        if self.instance and self.instance.pk:
            features = self.instance.get_features_list()
            if features:
                self.initial['features'] = "\n".join(features)
            
            # Load specifications into raw field
            specs = self.instance.specifications.all().order_by('display_order', 'category', 'name')
            if specs.exists():
                specs_lines = []
                for spec in specs:
                    specs_lines.append(f"{spec.category} | {spec.name} | {spec.value}")
                self.initial['specifications_raw'] = "\n".join(specs_lines)

    def clean_features(self):
        data = self.cleaned_data.get('features')
        if isinstance(data, str):
            # Split by lines and remove empty lines
            features_list = [line.strip() for line in data.splitlines() if line.strip()]
            return features_list
        return data

    def save(self, commit=True):
        product = super().save(commit=commit)
        
        # When saving the form, we also process the raw specifications field
        if commit:
            self._save_specifications(product)
            
        return product

    def _save_specifications(self, product):
        raw_specs = self.cleaned_data.get('specifications_raw', '')
        if not isinstance(raw_specs, str):
            return

        # Parse the raw specifications
        new_specs_data = []
        for line in raw_specs.splitlines():
            line = line.strip()
            if not line:
                continue
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                category, name, value = parts[0], parts[1], parts[2]
            elif len(parts) == 2:
                category, name, value = "General", parts[0], parts[1]
            else:
                category, name, value = "General", parts[0], ""
            
            new_specs_data.append({
                'category': category,
                'name': name,
                'value': value
            })

        # To keep it simple, we clear existing and recreate
        # In a high-traffic app we might want to be more surgical
        from .models import ProductSpecification
        product.specifications.all().delete()
        
        for i, spec_data in enumerate(new_specs_data):
            ProductSpecification.objects.create(
                product=product,
                display_order=i,
                **spec_data
            )

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main_image', 'display_order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe the image for SEO'}),
            'is_main_image': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ['category', 'name', 'value', 'display_order']
        widgets = {
            # Hidden: not needed in the UI, we default it to "General" if not provided.
            'category': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Screen Size, CPU Type'}),
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6.7 inches, Snapdragon 888'}),
            # Hidden: auto-managed
            'display_order': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make category optional in the form; we will normalize it in clean().
        self.fields["category"].required = False

        # Provide sensible defaults for new specs
        if not self.instance or not getattr(self.instance, "pk", None):
            self.initial.setdefault("category", "General")
            self.initial.setdefault("display_order", 0)

    def clean_category(self):
        value = (self.cleaned_data.get("category") or "").strip()
        return value or "General"

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True
)

ProductSpecificationFormSet = inlineformset_factory(
    Product, ProductSpecification,
    form=ProductSpecificationForm,
    extra=1,
    can_delete=True
)

from .models import ProductVariant

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['name', 'model_code', 'price', 'sale_price', 'cost_price', 'stock_quantity', 'min_stock_level', 'availability', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 55-inch'}),
            'model_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique SKU code'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['model_code'].required = True
        self.fields['price'].required = True
        self.fields['stock_quantity'].required = True

    def clean_model_code(self):
        model_code = self.cleaned_data.get('model_code')
        if not model_code:
            raise forms.ValidationError("Model code (SKU) is required.")
        
        # Check uniqueness across all variants except current one
        sku_exists = ProductVariant.objects.filter(model_code=model_code)
        if self.instance.pk:
            sku_exists = sku_exists.exclude(pk=self.instance.pk)
        
        if sku_exists.exists():
            raise forms.ValidationError(f"The SKU '{model_code}' is already in use by another variant.")
        return model_code

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_stock_quantity(self):
        stock = self.cleaned_data.get('stock_quantity')
        if stock is not None and stock < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock


class ProductVariantImageForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Remove filename length restriction - allow long filenames
            # Django's default limit is 100 characters, we'll override this
            if len(image.name) > 255:  # Set a more reasonable limit
                raise forms.ValidationError(f'Filename "{image.name}" is too long. Maximum 255 characters allowed.')
        return image
    
    class Meta:
        model = ProductVariantImage
        fields = ['image', 'alt_text', 'is_main_image', 'display_order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe the image for SEO'}),
            'is_main_image': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant,
    form=ProductVariantForm,
    extra=1,
    can_delete=True
)

ProductVariantImageFormSet = inlineformset_factory(
    ProductVariant, ProductVariantImage,
    form=ProductVariantImageForm,
    extra=1,
    can_delete=True
)


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'How can we help you?'}),
        }
