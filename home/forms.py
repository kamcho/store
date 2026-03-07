from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ContactMessage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'description', 'short_description',
            'model_code', 'series', 'price', 'sale_price', 'cost_price',
            'stock_quantity', 'min_stock_level', 'availability', 'warranty_period',
            'features', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product-url-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed product description'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Brief description for listings'}),
            'model_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. SM-S908E'}),
            'series': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Galaxy S, Galaxy Z'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'warranty_period': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '12'}),
            'features': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter one feature per line, e.g.\nPremium Dynamic AMOLED 2X\nSnapdragon 8 Gen 2\n5000mAh Battery'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.all()
        self.fields['category'].empty_label = "Select a category"
        
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
