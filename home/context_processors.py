from .models import ProductCategory

def categories_processor(request):
    """
    Returns top-level categories for global navigation.
    Subcategories can be accessed via parent_category.subcategories.all() in templates.
    """
    top_categories = ProductCategory.objects.filter(parent=None).prefetch_related('subcategories__subcategories')
    return {
        'nav_categories': top_categories
    }
