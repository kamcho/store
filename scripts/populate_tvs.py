import setup_django

from home.models import Product, ProductCategory, ProductVariant
from django.utils.text import slugify

def populate_tvs():
    tvs_data = [
        {
            "category": "neo-qled",
            "name": "Samsung Neo QLED 4K QN90C",
            "slug": "samsung-neo-qled-qn90c",
            "description": "Premium Neo QLED 4K TV with Quantum Mini LEDs for ultra-bright contrast and immersive viewing.",
            "short_description": "Premium Neo QLED 4K TV with Quantum Mini LED.",
            "model_code": "QN90C-BASE",
            "series": "Neo QLED",
            "price": 1899.99,
            "sale_price": 1699.99,
            "cost_price": 1400.00,
            "stock_quantity": 10,
            "min_stock_level": 3,
            "availability": "in_stock",
            "warranty_period": 24,
            "features": [
                "Quantum Mini LED technology",
                "Neural Quantum Processor 4K",
                "Dolby Atmos sound",
                "120Hz refresh rate",
                "Smart Hub with Tizen"
            ],
            "is_featured": True,
            "is_active": True,
            "variants": [
                {"name": "55-inch", "model_code": "QN55QN90C", "price": 1499.99, "sale_price": 1299.99, "stock": 5},
                {"name": "65-inch", "model_code": "QN65QN90C", "price": 1899.99, "sale_price": 1699.99, "stock": 5},
                {"name": "75-inch", "model_code": "QN75QN90C", "price": 2599.99, "sale_price": 2399.99, "stock": 2}
            ]
        },
        {
            "category": "neo-qled",
            "name": "Samsung Neo QLED 8K QN900C",
            "slug": "samsung-neo-qled-qn900c",
            "description": "Flagship 8K Neo QLED television with ultra-premium design and AI-powered upscaling.",
            "short_description": "Flagship 8K Neo QLED TV.",
            "model_code": "QN900C-BASE",
            "series": "Neo QLED",
            "price": 4499.99,
            "sale_price": 4199.99,
            "cost_price": 3600.00,
            "stock_quantity": 5,
            "min_stock_level": 2,
            "availability": "in_stock",
            "warranty_period": 24,
            "features": [
                "8K resolution",
                "Quantum Mini LED",
                "Neural Quantum Processor 8K",
                "Infinity Screen design",
                "Object Tracking Sound Pro"
            ],
            "is_featured": True,
            "is_active": True,
            "variants": [
                {"name": "65-inch", "model_code": "QN65QN900C", "price": 3499.99, "sale_price": 3199.99, "stock": 2},
                {"name": "75-inch", "model_code": "QN75QN900C", "price": 4499.99, "sale_price": 4199.99, "stock": 3},
                {"name": "85-inch", "model_code": "QN85QN900C", "price": 5999.99, "sale_price": 5499.99, "stock": 1}
            ]
        },
        {
            "category": "qled",
            "name": "Samsung QLED Q60C",
            "slug": "samsung-qled-q60c",
            "description": "Entry-level QLED TV with Quantum Dot color technology and slim design.",
            "short_description": "Affordable QLED TV with Quantum Dot.",
            "model_code": "Q60C-BASE",
            "series": "QLED",
            "price": 799.99,
            "sale_price": 699.99,
            "cost_price": 550.00,
            "stock_quantity": 20,
            "min_stock_level": 5,
            "availability": "in_stock",
            "warranty_period": 12,
            "features": [
                "Quantum Dot color",
                "Dual LED backlight",
                "4K resolution",
                "Tizen Smart TV",
                "Slim AirSlim design"
            ],
            "is_featured": False,
            "is_active": True,
            "variants": [
                {"name": "43-inch", "model_code": "QN43Q60C", "price": 549.99, "sale_price": 499.99, "stock": 10},
                {"name": "50-inch", "model_code": "QN50Q60C", "price": 649.99, "sale_price": 599.99, "stock": 5},
                {"name": "55-inch", "model_code": "QN55Q60C", "price": 799.99, "sale_price": 699.99, "stock": 5}
            ]
        },
        {
            "category": "qled",
            "name": "Samsung QLED Q70C",
            "slug": "samsung-qled-q70c",
            "description": "Mid-range QLED TV designed for gaming and fast motion with 120Hz refresh rate.",
            "short_description": "QLED gaming TV with 120Hz refresh.",
            "model_code": "Q70C-BASE",
            "series": "QLED",
            "price": 1199.99,
            "sale_price": 999.99,
            "cost_price": 800.00,
            "stock_quantity": 15,
            "min_stock_level": 5,
            "availability": "in_stock",
            "warranty_period": 12,
            "features": [
                "Quantum Processor 4K",
                "120Hz refresh rate",
                "Motion Xcelerator Turbo",
                "Quantum HDR",
                "Game Mode Pro"
            ],
            "is_featured": True,
            "is_active": True,
            "variants": [
                {"name": "55-inch", "model_code": "QN55Q70C", "price": 999.99, "sale_price": 899.99, "stock": 8},
                {"name": "65-inch", "model_code": "QN65Q70C", "price": 1199.99, "sale_price": 999.99, "stock": 7}
            ]
        },
        {
            "category": "qled",
            "name": "Samsung QLED Q80C",
            "slug": "samsung-qled-q80c",
            "description": "High-performance QLED TV with full array local dimming and powerful AI processor.",
            "short_description": "Premium QLED with local dimming.",
            "model_code": "Q80C-BASE",
            "series": "QLED",
            "price": 1499.99,
            "sale_price": 1299.99,
            "cost_price": 1050.00,
            "stock_quantity": 12,
            "min_stock_level": 4,
            "availability": "in_stock",
            "warranty_period": 12,
            "features": [
                "Full Array Local Dimming",
                "Quantum HDR+",
                "Object Tracking Sound Lite",
                "120Hz refresh rate",
                "AI upscaling"
            ],
            "is_featured": True,
            "is_active": True,
            "variants": [
                {"name": "50-inch", "model_code": "QN50Q80C", "price": 1099.99, "sale_price": 999.99, "stock": 4},
                {"name": "65-inch", "model_code": "QN65Q80C", "price": 1499.99, "sale_price": 1299.99, "stock": 8}
            ]
        },
        {
            "category": "crystal-uhd",
            "name": "Samsung Crystal UHD CU7000",
            "slug": "samsung-crystal-uhd-cu7000",
            "description": "Affordable 4K Crystal UHD TV with vibrant colors and smart features.",
            "short_description": "Budget 4K Crystal UHD TV.",
            "model_code": "CU7000-BASE",
            "series": "Crystal UHD",
            "price": 499.99,
            "sale_price": 449.99,
            "cost_price": 350.00,
            "stock_quantity": 25,
            "min_stock_level": 5,
            "availability": "in_stock",
            "warranty_period": 12,
            "features": [
                "Crystal Processor 4K",
                "PurColor technology",
                "Smart Hub",
                "4K resolution",
                "Ultra Slim design"
            ],
            "is_featured": False,
            "is_active": True,
             "variants": [
                {"name": "43-inch", "model_code": "UN43CU7000", "price": 379.99, "sale_price": 349.99, "stock": 10},
                {"name": "55-inch", "model_code": "UN55CU7000", "price": 499.99, "sale_price": 449.99, "stock": 15}
            ]
        },
        {
            "category": "lifestyle-tv",
            "name": "Samsung The Frame",
            "slug": "samsung-the-frame",
            "description": "Lifestyle TV that doubles as an art display when turned off.",
            "short_description": "Art-inspired lifestyle television.",
            "model_code": "THE-FRAME-BASE",
            "series": "Lifestyle TV",
            "price": 1499.99,
            "sale_price": 1399.99,
            "cost_price": 1100.00,
            "stock_quantity": 10,
            "min_stock_level": 3,
            "availability": "in_stock",
            "warranty_period": 24,
            "features": [
                "Art Mode",
                "Customizable bezels",
                "Matte display",
                "Quantum Dot color",
                "SmartThings support"
            ],
            "is_featured": True,
            "is_active": True,
            "variants": [
                {"name": "43-inch", "model_code": "QN43LS03C", "price": 999.99, "sale_price": 899.99, "stock": 3},
                {"name": "55-inch", "model_code": "QN55LS03C", "price": 1499.99, "sale_price": 1399.99, "stock": 5},
                {"name": "65-inch", "model_code": "QN65LS03C", "price": 1999.99, "sale_price": 1899.99, "stock": 2}
            ]
        }
    ]

    for data in tvs_data:
        category_slug = data.pop('category')
        variants_data = data.pop('variants', [])
        
        try:
            category = ProductCategory.objects.get(slug=category_slug)
        except ProductCategory.DoesNotExist:
            print(f"Category {category_slug} does not exist. Skipping {data['name']}.")
            continue

        product, created = Product.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'category': category,
                'name': data['name'],
                'description': data['description'],
                'short_description': data['short_description'],
                'series': data['series'],
                'model_code': data['model_code'],
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
        
        status = "Created" if created else "Updated"
        print(f"{status} base product: {product.name}")

        for v_data in variants_data:
            variant, v_created = ProductVariant.objects.update_or_create(
                model_code=v_data['model_code'],
                defaults={
                    'product': product,
                    'name': v_data['name'],
                    'price': v_data['price'],
                    'sale_price': v_data['sale_price'],
                    'stock_quantity': v_data['stock'],
                    'specifications': {'screen_size': v_data['name']}
                }
            )
            v_status = "Created" if v_created else "Updated"
            print(f"  {v_status} variant: {variant.name}")

if __name__ == '__main__':
    populate_tvs()
    print("TV population complete!")
