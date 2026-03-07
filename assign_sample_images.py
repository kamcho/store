import os
import requests
import tempfile
from django.core.files import File
from home.models import Product, ProductImage

def run():
    print("Starting image assignment...")
    
    # Map keywords to working Unsplash source URLs
    image_map = {
        'Galaxy S': 'https://images.unsplash.com/photo-1621330396173-e41b1cafd17f?auto=format&fit=crop&q=80&w=800',
        'Watch': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&q=80&w=800',
        'Buds': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&q=80&w=800',
        'Laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&q=80&w=800',
        'Tablet': 'https://images.unsplash.com/photo-1544244015-0cd4b3ff074b?auto=format&fit=crop&q=80&w=800',
        'Default': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&q=80&w=800'
    }

    products = Product.objects.all()
    
    for product in products:
        if product.images.exists():
            continue

        image_url = image_map['Default']
        lower_name = product.name.lower()
        
        if any(x in lower_name for x in ['s24', 'galaxy s', 'phone']):
            image_url = image_map['Galaxy S']
        elif 'watch' in lower_name:
            image_url = image_map['Watch']
        elif any(x in lower_name for x in ['buds', 'audio', 'headphones']):
            image_url = image_map['Buds']
        elif any(x in lower_name for x in ['laptop', 'book']):
            image_url = image_map['Laptop']
        elif any(x in lower_name for x in ['tab', 'tablet']):
            image_url = image_map['Tablet']

        print(f"Downloading for {product.name}...")
        
        try:
            r = requests.get(image_url, timeout=15)
            if r.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tf:
                    tf.write(r.content)
                    tf.flush()
                    temp_path = tf.name
                
                with open(temp_path, 'rb') as f:
                    new_img = ProductImage(
                        product=product,
                        alt_text=product.name,
                        is_main_image=True
                    )
                    new_img.image.save(f"{product.slug}.jpg", File(f), save=True)
                
                os.unlink(temp_path)
                print(f"Success: {product.name}")
            else:
                print(f"Failed {product.name}: {r.status_code}")
        except Exception as e:
            print(f"Error {product.name}: {e}")

if __name__ == "__main__":
    run()
