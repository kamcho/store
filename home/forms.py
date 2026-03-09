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
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 'short_description',
            'warranty_period', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product-url-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed product description'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Brief description for listings'}),
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

    def clean_features(self):
        data = self.cleaned_data.get('features')
        if isinstance(data, str):
            # Split by lines and remove empty lines
            features_list = [line.strip() for line in data.splitlines() if line.strip()]
            return features_list
        return data

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
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Display, Processor, Camera'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Screen Size, CPU Type'}),
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6.7 inches, Snapdragon 888'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

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
    specifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Color: Red\nStorage: 128GB'
        })
    )

    class Meta:
        model = ProductVariant
        fields = ['name', 'model_code', 'price', 'sale_price', 'cost_price', 'stock_quantity', 'min_stock_level', 'availability', 'specifications', 'is_active']
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
        if self.instance and self.instance.pk and self.instance.specifications:
            if isinstance(self.instance.specifications, dict):
                specs_text = "\n".join([f"{k}: {v}" for k, v in self.instance.specifications.items()])
                self.initial['specifications'] = specs_text

    def clean_specifications(self):
        data = self.cleaned_data.get('specifications')
        if not data:
            return {}
        
        specs_dict = {}
        for line in data.splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                specs_dict[key.strip()] = value.strip()
            else:
                specs_dict[line] = ""
        return specs_dict

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
