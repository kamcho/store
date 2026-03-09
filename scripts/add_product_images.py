#!/usr/bin/env python3
"""
Script to add sample images to Samsung Gear 360 Camera
"""

import os, sys, django
sys.path.append('/home/kali/Downloads/Samsung')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from django.core.files.base import ContentFile
from django.db import transaction
from home.models import Product, ProductImage

def add_sample_images():
    product = Product.objects.get(slug='sm-r210')
    
    # Check existing images
    existing_images = ProductImage.objects.filter(product=product)
    print(f"Current images for {product.name}: {existing_images.count()}")
    
    # Sample image data (using placeholder images)
    sample_images = [
        {
            'alt_text': 'Samsung Gear 360 Camera - Front View',
            'is_main_image': True,
            'display_order': 1,
            'filename': 'gear360-front.jpg'
        },
        {
            'alt_text': 'Samsung Gear 360 Camera - Side View',
            'is_main_image': False,
            'display_order': 2,
            'filename': 'gear360-side.jpg'
        },
        {
            'alt_text': 'Samsung Gear 360 Camera - Top View',
            'is_main_image': False,
            'display_order': 3,
            'filename': 'gear360-top.jpg'
        }
    ]
    
    with transaction.atomic():
        for img_data in sample_images:
            # Check if image already exists
            existing = ProductImage.objects.filter(
                product=product, 
                alt_text=img_data['alt_text']
            ).first()
            
            if existing:
                print(f"⚠️  Image '{img_data['alt_text']}' already exists, skipping...")
                continue
            
            # Create a simple placeholder image content
            # In a real scenario, you'd upload actual image files
            placeholder_content = b"placeholder_image_content"
            
            # Create new image
            image = ProductImage.objects.create(
                product=product,
                alt_text=img_data['alt_text'],
                is_main_image=img_data['is_main_image'],
                display_order=img_data['display_order']
            )
            
            # Save the image file
            image.image.save(img_data['filename'], ContentFile(placeholder_content))
            
            print(f"✅ Created image: {image.alt_text}")
    
    # Verify
    total_images = ProductImage.objects.filter(product=product).count()
    print(f"🎉 Total images for {product.name}: {total_images}")

if __name__ == "__main__":
    add_sample_images()
