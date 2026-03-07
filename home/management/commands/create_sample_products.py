from django.core.management.base import BaseCommand
from home.models import ProductCategory, Product, ProductSpecification
import json

class Command(BaseCommand):
    help = 'Create sample Samsung products'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Smartphones', 'slug': 'smartphones', 'description': 'Latest Samsung Galaxy smartphones'},
            {'name': 'Tablets', 'slug': 'tablets', 'description': 'Samsung Galaxy tablets and e-readers'},
            {'name': 'TVs', 'slug': 'tvs', 'description': 'Samsung Neo QLED and OLED TVs'},
            {'name': 'Smart Watches', 'slug': 'smart-watches', 'description': 'Samsung Galaxy Watch series'},
            {'name': 'Earbuds', 'slug': 'earbuds', 'description': 'Samsung Galaxy Buds wireless earbuds'},
        ]

        created_categories = {}
        for cat_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            created_categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Products data
        products_data = [
            # Smartphones
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'slug': 'samsung-galaxy-s24-ultra',
                'category': 'smartphones',
                'model_code': 'SM-S928B',
                'series': 'Galaxy S',
                'description': 'The ultimate Samsung smartphone with S Pen, advanced camera system, and titanium design.',
                'short_description': 'Flagship smartphone with 200MP camera and S Pen',
                'price': 1199.99,
                'sale_price': 1099.99,
                'stock_quantity': 25,
                'features': ['200MP Main Camera', 'S Pen Included', 'Titanium Frame', '5000mAh Battery', '6.8" Dynamic AMOLED'],
                'is_featured': True,
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '6.8 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '3200 x 1440'},
                    {'category': 'Camera', 'name': 'Main Camera', 'value': '200MP + 50MP + 12MP + 10MP'},
                    {'category': 'Camera', 'name': 'Front Camera', 'value': '12MP'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Snapdragon 8 Gen 3'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '12GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '256GB/512GB/1TB'},
                ]
            },
            {
                'name': 'Samsung Galaxy S24',
                'slug': 'samsung-galaxy-s24',
                'category': 'smartphones',
                'model_code': 'SM-S921B',
                'series': 'Galaxy S',
                'description': 'Compact flagship with powerful performance and advanced AI features.',
                'short_description': 'Compact flagship with advanced AI capabilities',
                'price': 799.99,
                'stock_quantity': 40,
                'features': ['50MP Camera', 'AI Features', 'Galaxy AI', '4000mAh Battery', '6.2" Dynamic AMOLED'],
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '6.2 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '2340 x 1080'},
                    {'category': 'Camera', 'name': 'Main Camera', 'value': '50MP + 10MP + 12MP'},
                    {'category': 'Camera', 'name': 'Front Camera', 'value': '12MP'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Exynos 2400'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '8GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '128GB/256GB'},
                ]
            },
            
            # Tablets
            {
                'name': 'Samsung Galaxy Tab S9 Ultra',
                'slug': 'samsung-galaxy-tab-s9-ultra',
                'category': 'tablets',
                'model_code': 'SM-X910',
                'series': 'Galaxy Tab',
                'description': 'The ultimate tablet with massive 14.6" display and S Pen included.',
                'short_description': 'Premium tablet with S Pen and stunning display',
                'price': 1099.99,
                'sale_price': 999.99,
                'stock_quantity': 15,
                'features': ['14.6" Display', 'S Pen Included', 'Snapdragon 8 Gen 2', '11200mAh Battery', 'Quad Speakers'],
                'is_featured': True,
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '14.6 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '2960 x 1848'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Snapdragon 8 Gen 2 for Galaxy'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '12GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '256GB/512GB/1TB'},
                    {'category': 'Battery', 'name': 'Battery Capacity', 'value': '11200mAh'},
                ]
            },
            {
                'name': 'Samsung Galaxy Tab S9',
                'slug': 'samsung-galaxy-tab-s9',
                'category': 'tablets',
                'model_code': 'SM-X710',
                'series': 'Galaxy Tab',
                'description': 'Premium tablet with dynamic AMOLED display and S Pen.',
                'short_description': 'High-performance tablet with S Pen',
                'price': 699.99,
                'stock_quantity': 20,
                'features': ['11" Display', 'S Pen Included', 'Snapdragon 8 Gen 2', '8400mAh Battery'],
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '11 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '2560 x 1600'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Snapdragon 8 Gen 2 for Galaxy'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '8GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '128GB/256GB'},
                    {'category': 'Battery', 'name': 'Battery Capacity', 'value': '8400mAh'},
                ]
            },

            # TVs
            {
                'name': 'Samsung Neo QLED 8K QN900C',
                'slug': 'samsung-neo-qled-8k-qn900c',
                'category': 'tvs',
                'model_code': 'QN85QN900C',
                'series': 'Neo QLED',
                'description': 'Revolutionary 8K resolution with Quantum Matrix Pro technology.',
                'short_description': 'Premium 8K QLED TV with advanced AI upscaling',
                'price': 3499.99,
                'sale_price': 2999.99,
                'stock_quantity': 8,
                'features': ['8K Resolution', 'Quantum Matrix Pro', 'Neural Quantum Processor 8K', 'Object Tracking Sound', 'Gaming Hub'],
                'is_featured': True,
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '75 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '7680 x 4320 (8K)'},
                    {'category': 'Display', 'name': 'Panel Type', 'value': 'Mini LED QLED'},
                    {'category': 'Smart TV', 'name': 'Operating System', 'value': 'Tizen OS'},
                    {'category': 'Audio', 'name': 'Sound Output', 'value': '70W 4.2.2 Channel'},
                    {'category': 'Connectivity', 'name': 'HDMI Ports', 'value': '4x HDMI 2.1'},
                ]
            },
            {
                'name': 'Samsung OLED 4K S95C',
                'slug': 'samsung-oled-4k-s95c',
                'category': 'tvs',
                'model_code': 'QN55S95C',
                'series': 'OLED',
                'description': 'Stunning OLED display with vibrant colors and perfect blacks.',
                'short_description': 'Premium 4K OLED TV with incredible contrast',
                'price': 1899.99,
                'stock_quantity': 12,
                'features': ['4K OLED Display', 'Neural Quantum Processor 4K', 'Object Tracking Sound Lite', 'Smart TV'],
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '55 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '3840 x 2160 (4K)'},
                    {'category': 'Display', 'name': 'Panel Type', 'value': 'OLED'},
                    {'category': 'Smart TV', 'name': 'Operating System', 'value': 'Tizen OS'},
                    {'category': 'Audio', 'name': 'Sound Output', 'value': '40W 2.2.2 Channel'},
                    {'category': 'Connectivity', 'name': 'HDMI Ports', 'value': '4x HDMI 2.1'},
                ]
            },

            # Smart Watches
            {
                'name': 'Samsung Galaxy Watch 6 Classic',
                'slug': 'samsung-galaxy-watch-6-classic',
                'category': 'smart-watches',
                'model_code': 'SM-R965',
                'series': 'Galaxy Watch',
                'description': 'Premium smartwatch with rotating bezel and advanced health monitoring.',
                'short_description': 'Classic smartwatch with rotating bezel',
                'price': 399.99,
                'stock_quantity': 30,
                'features': ['Rotating Bezel', 'Advanced Sleep Tracking', 'Body Composition', 'IP68 + 5ATM', 'Wear OS'],
                'is_featured': True,
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '1.3 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '450 x 450'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Exynos W930'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '2GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '16GB'},
                    {'category': 'Battery', 'name': 'Battery Life', 'value': 'Up to 40 hours'},
                ]
            },
            {
                'name': 'Samsung Galaxy Watch 6',
                'slug': 'samsung-galaxy-watch-6',
                'category': 'smart-watches',
                'model_code': 'SM-R930',
                'series': 'Galaxy Watch',
                'description': 'Sleek smartwatch with comprehensive health and fitness tracking.',
                'short_description': 'Modern smartwatch with advanced health features',
                'price': 299.99,
                'stock_quantity': 35,
                'features': ['Advanced Sleep Tracking', 'Body Composition', 'IP68 + 5ATM', 'Wear OS', 'Lightweight Design'],
                'specifications': [
                    {'category': 'Display', 'name': 'Screen Size', 'value': '1.3 inches'},
                    {'category': 'Display', 'name': 'Resolution', 'value': '450 x 450'},
                    {'category': 'Performance', 'name': 'Processor', 'value': 'Exynos W930'},
                    {'category': 'Memory', 'name': 'RAM', 'value': '2GB'},
                    {'category': 'Memory', 'name': 'Storage', 'value': '16GB'},
                    {'category': 'Battery', 'name': 'Battery Life', 'value': 'Up to 40 hours'},
                ]
            },

            # Earbuds
            {
                'name': 'Samsung Galaxy Buds 2 Pro',
                'slug': 'samsung-galaxy-buds-2-pro',
                'category': 'earbuds',
                'model_code': 'SM-R510',
                'series': 'Galaxy Buds',
                'description': 'Premium wireless earbuds with intelligent ANC and 360 Audio.',
                'short_description': 'High-end earbuds with active noise cancellation',
                'price': 229.99,
                'stock_quantity': 50,
                'features': ['Intelligent ANC', '360 Audio', 'Hi-Fi Sound', 'IPX7 Water Resistance', 'Wireless Charging'],
                'is_featured': True,
                'specifications': [
                    {'category': 'Audio', 'name': 'Driver Size', 'value': '10mm'},
                    {'category': 'Audio', 'name': 'Frequency Response', 'value': '20Hz - 20kHz'},
                    {'category': 'Battery', 'name': 'Earbud Battery', 'value': 'Up to 8 hours'},
                    {'category': 'Battery', 'name': 'Total Battery', 'value': 'Up to 29 hours'},
                    {'category': 'Connectivity', 'name': 'Bluetooth Version', 'value': '5.3'},
                    {'category': 'Features', 'name': 'Water Resistance', 'value': 'IPX7'},
                ]
            },
            {
                'name': 'Samsung Galaxy Buds 2',
                'slug': 'samsung-galaxy-buds-2',
                'category': 'earbuds',
                'model_code': 'SM-R177',
                'series': 'Galaxy Buds',
                'description': 'Comfortable wireless earbuds with great sound quality.',
                'short_description': 'Affordable earbuds with premium features',
                'price': 149.99,
                'stock_quantity': 60,
                'features': ['Active Noise Cancellation', 'Ambient Sound', 'Hi-Fi Sound', 'IPX2 Water Resistance', 'Compact Design'],
                'specifications': [
                    {'category': 'Audio', 'name': 'Driver Size', 'value': '12mm'},
                    {'category': 'Audio', 'name': 'Frequency Response', 'value': '20Hz - 20kHz'},
                    {'category': 'Battery', 'name': 'Earbud Battery', 'value': 'Up to 7.5 hours'},
                    {'category': 'Battery', 'name': 'Total Battery', 'value': 'Up to 29 hours'},
                    {'category': 'Connectivity', 'name': 'Bluetooth Version', 'value': '5.2'},
                    {'category': 'Features', 'name': 'Water Resistance', 'value': 'IPX2'},
                ]
            },
        ]

        # Create products
        for product_data in products_data:
            category = created_categories[product_data['category']]
            specifications = product_data.pop('specifications', [])
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'features': json.dumps(product_data['features'])
                }
            )
            
            if created:
                # Create specifications
                for spec_data in specifications:
                    ProductSpecification.objects.create(
                        product=product,
                        **spec_data
                    )
                
                self.stdout.write(f'Created product: {product.name}')
            else:
                self.stdout.write(f'Product already exists: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample products!'))
