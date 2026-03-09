import setup_django

from home.models import Product, ProductCategory
from django.utils.text import slugify

def populate_watches():
    watches_data = [
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch",
        "slug": "samsung-galaxy-watch-2018",
        "description": "The original Samsung Galaxy Watch combines classic watch design with smart fitness tracking and long battery life.",
        "short_description": "Samsung's first Galaxy Watch with fitness tracking and AMOLED display.",
        "model_code": "SM-R800",
        "series": "Galaxy Watch Series",
        "price": 299.99,
        "sale_price": None,
        "cost_price": 220.00,
        "stock_quantity": 25,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Super AMOLED display",
          "Heart rate monitoring",
          "GPS tracking",
          "Water resistant 5ATM",
          "Tizen OS"
        ],
        "is_featured": False,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch Active",
        "slug": "samsung-galaxy-watch-active",
        "description": "A lightweight smartwatch focused on health and fitness with automatic workout tracking.",
        "short_description": "Slim fitness-focused smartwatch with AMOLED display.",
        "model_code": "SM-R500",
        "series": "Galaxy Watch Series",
        "price": 199.99,
        "sale_price": None,
        "cost_price": 150.00,
        "stock_quantity": 20,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Auto workout tracking",
          "Heart rate monitoring",
          "Stress tracking",
          "Super AMOLED display",
          "Lightweight design"
        ],
        "is_featured": False,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch Active2",
        "slug": "samsung-galaxy-watch-active2",
        "description": "Improved fitness smartwatch with touch bezel navigation and enhanced health tracking.",
        "short_description": "Fitness smartwatch with touch bezel and ECG support.",
        "model_code": "SM-R820",
        "series": "Galaxy Watch Series",
        "price": 249.99,
        "sale_price": 219.99,
        "cost_price": 180.00,
        "stock_quantity": 18,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Touch bezel navigation",
          "ECG support",
          "Sleep tracking",
          "Fitness tracking",
          "Super AMOLED display"
        ],
        "is_featured": False,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 3",
        "slug": "samsung-galaxy-watch-3",
        "description": "Premium smartwatch with rotating bezel, advanced health monitoring and classic design.",
        "short_description": "Premium Galaxy smartwatch with rotating bezel.",
        "model_code": "SM-R840",
        "series": "Galaxy Watch Series",
        "price": 399.99,
        "sale_price": 349.99,
        "cost_price": 300.00,
        "stock_quantity": 15,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Physical rotating bezel",
          "Blood oxygen monitoring",
          "ECG",
          "Fall detection",
          "AMOLED display"
        ],
        "is_featured": False,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 4",
        "slug": "samsung-galaxy-watch-4",
        "description": "First Samsung smartwatch powered by Wear OS with advanced body composition analysis.",
        "short_description": "Wear OS smartwatch with body composition tracking.",
        "model_code": "SM-R870",
        "series": "Galaxy Watch Series",
        "price": 249.99,
        "sale_price": 219.99,
        "cost_price": 190.00,
        "stock_quantity": 30,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Wear OS powered by Samsung",
          "Body composition analysis",
          "Sleep tracking",
          "Advanced fitness tracking",
          "AMOLED display"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 4 Classic",
        "slug": "samsung-galaxy-watch-4-classic",
        "description": "Classic design smartwatch with rotating bezel and advanced Wear OS features.",
        "short_description": "Wear OS smartwatch with classic rotating bezel.",
        "model_code": "SM-R890",
        "series": "Galaxy Watch Series",
        "price": 349.99,
        "sale_price": 319.99,
        "cost_price": 270.00,
        "stock_quantity": 20,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Physical rotating bezel",
          "Wear OS",
          "Body composition analysis",
          "Heart rate monitoring",
          "Premium stainless steel build"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 5",
        "slug": "samsung-galaxy-watch-5",
        "description": "Durable smartwatch with sapphire crystal display and advanced health tracking.",
        "short_description": "Durable fitness smartwatch with sapphire crystal.",
        "model_code": "SM-R900",
        "series": "Galaxy Watch Series",
        "price": 279.99,
        "sale_price": 249.99,
        "cost_price": 210.00,
        "stock_quantity": 28,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Sapphire crystal display",
          "Sleep coaching",
          "Advanced fitness tracking",
          "Improved battery life",
          "Wear OS"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 5 Pro",
        "slug": "samsung-galaxy-watch-5-pro",
        "description": "Rugged smartwatch designed for outdoor adventures with extended battery life.",
        "short_description": "Premium rugged smartwatch with long battery life.",
        "model_code": "SM-R920",
        "series": "Galaxy Watch Series",
        "price": 449.99,
        "sale_price": 399.99,
        "cost_price": 350.00,
        "stock_quantity": 15,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Titanium body",
          "Route tracking GPS",
          "Extended battery life",
          "Sapphire crystal display",
          "Advanced health sensors"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 6",
        "slug": "samsung-galaxy-watch-6",
        "description": "Modern smartwatch with larger display, improved performance and advanced health features.",
        "short_description": "Galaxy smartwatch with larger display and advanced health tracking.",
        "model_code": "SM-R930",
        "series": "Galaxy Watch Series",
        "price": 299.99,
        "sale_price": 269.99,
        "cost_price": 230.00,
        "stock_quantity": 30,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Larger AMOLED display",
          "Improved performance",
          "Advanced sleep tracking",
          "Wear OS",
          "Fitness tracking"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 6 Classic",
        "slug": "samsung-galaxy-watch-6-classic",
        "description": "Classic rotating bezel smartwatch with large display and premium design.",
        "short_description": "Classic rotating bezel smartwatch with Wear OS.",
        "model_code": "SM-R960",
        "series": "Galaxy Watch Series",
        "price": 399.99,
        "sale_price": 369.99,
        "cost_price": 320.00,
        "stock_quantity": 22,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Rotating bezel",
          "Large AMOLED display",
          "Advanced health monitoring",
          "Wear OS",
          "Premium stainless steel design"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch 7",
        "slug": "samsung-galaxy-watch-7",
        "description": "Next-generation Galaxy smartwatch with AI-powered health insights and improved performance.",
        "short_description": "AI-powered health smartwatch with improved battery life.",
        "model_code": "SM-L300",
        "series": "Galaxy Watch Series",
        "price": 329.99,
        "sale_price": None,
        "cost_price": 270.00,
        "stock_quantity": 18,
        "min_stock_level": 5,
        "availability": "in_stock",
        "warranty_period": 12,
        "features": [
          "Galaxy AI health insights",
          "Advanced fitness tracking",
          "Improved battery life",
          "AMOLED display",
          "Wear OS"
        ],
        "is_featured": True,
        "is_active": True
      },
      {
        "category": "galaxy-watch-series",
        "name": "Samsung Galaxy Watch Ultra",
        "slug": "samsung-galaxy-watch-ultra",
        "description": "Samsung's most rugged and advanced smartwatch designed for extreme outdoor activities.",
        "short_description": "Ultra-rugged premium smartwatch for extreme sports.",
        "model_code": "SM-L705",
        "series": "Galaxy Watch Series",
        "price": 649.99,
        "sale_price": None,
        "cost_price": 550.00,
        "stock_quantity": 10,
        "min_stock_level": 3,
        "availability": "in_stock",
        "warranty_period": 24,
        "features": [
          "Titanium case",
          "Extreme durability",
          "Advanced GPS",
          "Long battery life",
          "AI fitness tracking"
        ],
        "is_featured": True,
        "is_active": True
      }
    ]

    for data in watches_data:
        category_slug = data.pop('category')
        try:
            category = ProductCategory.objects.get(slug=category_slug)
        except ProductCategory.DoesNotExist:
            print(f"Category {category_slug} does not exist. Skipping {data['name']}.")
            continue

        product, created = Product.objects.update_or_create(
            model_code=data['model_code'],
            defaults={
                'category': category,
                'name': data['name'],
                'slug': data['slug'],
                'description': data['description'],
                'short_description': data['short_description'],
                'series': data['series'],
                'price': data['price'],
                'sale_price': data['sale_price'],
                'cost_price': data['cost_price'],
                'stock_quantity': data['stock_quantity'],
                'min_stock_level': data['min_stock_level'],
                'availability': data['availability'],
                'warranty_period': data['warranty_period'],
                'features': data['features'],
                'is_featured': data['is_featured'],
                'is_active': data['is_active'],
            }
        )
        if created:
            print(f"Created watch: {product.name}")
        else:
            print(f"Updated watch: {product.name}")

if __name__ == '__main__':
    populate_watches()
    print("Watch population complete!")
