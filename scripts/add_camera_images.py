#!/usr/bin/env python3
"""
Script to add placeholder images to camera products
"""

import os, sys, django
sys.path.append('/home/kali/Downloads/Samsung')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from django.db import transaction
from home.models import Product, ProductImage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io

def create_placeholder_image(width, height, text, color):
    """Create a simple placeholder image"""
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        # Try to use a larger font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill="white", font=font)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    
    return img_bytes

def add_camera_images():
    camera_products = Product.objects.filter(category__name__in=['Digital Cameras', 'Camera Lenses', 'Camera Accessories', 'Action Cameras'])
    
    with transaction.atomic():
        for product in camera_products:
            if product.images.exists():
                print(f"⚠️  {product.name} already has images, skipping...")
                continue
                
            print(f"Adding images to {product.name}...")
            
            # Add main product image
            main_image_bytes = create_placeholder_image(800, 600, product.name, (59, 130, 246))  # Blue background
            main_image = ProductImage(
                product=product,
                alt_text=f"{product.name} - Main Image",
                is_main_image=True,
                display_order=0
            )
            main_image.image.save(f"{product.slug}_main.jpg", ContentFile(main_image_bytes.read()), save=True)
            
            # Add detail image for cameras
            if 'Camera' in product.name and 'Lens' not in product.name and 'Accessory' not in product.name:
                detail_image_bytes = create_placeholder_image(800, 600, f"{product.name} - Detail", (34, 197, 94))  # Green background
                detail_image = ProductImage(
                    product=product,
                    alt_text=f"{product.name} - Detail View",
                    is_main_image=False,
                    display_order=1
                )
                detail_image.image.save(f"{product.slug}_detail.jpg", ContentFile(detail_image_bytes.read()), save=True)
            
            print(f"✅ Added images to {product.name}")

    print(f"🎉 Added placeholder images to camera products!")

if __name__ == "__main__":
    add_camera_images()
