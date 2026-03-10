from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, Min
from django.contrib import messages
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
import json
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ProductVariant, ProductVariantImage, ContactMessage
from .forms import ProductForm, ProductImageFormSet, ProductSpecificationFormSet, ProductVariantForm, ProductVariantFormSet, ProductVariantImageFormSet, ContactMessageForm
from .forms_login import CustomLoginForm

@cache_page(60 * 150)  # Cache for 15 minutes
def home(request):
    # Hero product: first featured product, or newest active product
    hero_product = Product.objects.filter(
        is_active=True, is_featured=True
    ).select_related('category').prefetch_related('images', 'variants').first()
    if not hero_product:
        hero_product = Product.objects.filter(
            is_active=True
        ).select_related('category').prefetch_related('images', 'variants').first()

    # Featured products for the hero cards (up to 10 random products)
    featured_products = Product.objects.filter(is_active=True).exclude(
        pk=hero_product.pk if hero_product else 0
    ).select_related('category').prefetch_related('images', 'variants').order_by('?')[:6]

    # Custom sections as requested by the user
    # Pair of (Section Display Name, Category Slug)
    section_configs = [
        ("Smartphones", "smartphones"),
        ("TV & Audio", "tv-audio"),
        ("Home & Living", "home-appliances"),
    ]

    homepage_sections = []
    
    def get_category_descendants(category):
        descendant_ids = [category.id]
        for sub in category.subcategories.all():
            descendant_ids.extend(get_category_descendants(sub))
        return descendant_ids

    for display_name, slug in section_configs:
        try:
            category = ProductCategory.objects.get(slug=slug)
            all_cat_ids = get_category_descendants(category)
            
            section_products = Product.objects.filter(
                is_active=True, 
                category_id__in=all_cat_ids
            ).select_related('category').prefetch_related('images', 'variants').order_by('-created_at')[:8]
            
            if section_products.exists():
                homepage_sections.append({
                    'name': display_name,
                    'slug': slug,
                    'products': section_products
                })
        except ProductCategory.DoesNotExist:
            continue

    # Flash sale products (products with an active variant that has a sale price)
    flash_sale_products = Product.objects.filter(
        is_active=True,
        variants__is_active=True,
        variants__sale_price__isnull=False
    ).distinct().select_related('category').prefetch_related('images', 'variants')[:8]

    # Recent arrivals (newest products)
    recent_arrivals = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images', 'variants').order_by('-created_at')[:4]

    context = {
        'hero_product': hero_product,
        'featured_products': featured_products,
        'homepage_sections': homepage_sections,
        'flash_sale_products': flash_sale_products,
        'recent_arrivals': recent_arrivals,
        'store_name': 'World Tech Partners',
        'store_tagline': 'Your Premium Technology Partner',
    }
    return render(request, 'home/index.html', context)

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    # Get category filter
    category_slug = request.GET.get('category')
    if category_slug and category_slug != 'None':
        category = get_object_or_404(ProductCategory, slug=category_slug)
        
        def get_descendants(cat):
            descendants = [cat.id]
            for child in cat.subcategories.all():
                descendants.extend(get_descendants(child))
            return descendants
            
        all_cat_ids = get_descendants(category)
        products = products.filter(category_id__in=all_cat_ids)
    
    # Get search query
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            name__icontains=search_query
        )
    
    # Annotate with starting price for sorting and display
    products = products.annotate(starting_price=Min('variants__price'))
    
    # Get sort option
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('starting_price')
    elif sort_by == 'price_high':
        products = products.order_by('-starting_price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter sidebar
    categories = ProductCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query or '',
        'sort_by': sort_by,
    }
    
    return render(request, 'home/product_list.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES)
        spec_formset = ProductSpecificationFormSet(request.POST)
        
        # Debug: Print form errors
        print("=== FORM VALIDATION DEBUG ===")
        print(f"Main form valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Main form errors: {form.errors}")
        
        print(f"Image formset valid: {image_formset.is_valid()}")
        if not image_formset.is_valid():
            print(f"Image formset errors: {image_formset.errors}")
            for i, img_form in enumerate(image_formset):
                if img_form.errors:
                    print(f"Image form {i} errors: {img_form.errors}")
        
        print(f"Spec formset valid: {spec_formset.is_valid()}")
        if not spec_formset.is_valid():
            print(f"Spec formset errors: {spec_formset.errors}")
            for i, spec_form in enumerate(spec_formset):
                if spec_form.errors:
                    print(f"Spec form {i} errors: {spec_form.errors}")
        print("=== END DEBUG ===")
        
        if form.is_valid():
            product = form.save()
            
            # Only save formsets if they have valid data
            if image_formset.is_valid():
                image_formset.instance = product
                image_formset.save()
            
            if spec_formset.is_valid():
                spec_formset.instance = product
                spec_formset.save()
            
            messages.success(request, f'Product "{product.name}" has been created successfully! Add variations to proceed.')
            return redirect('product_variant_manage', slug=product.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet()
        spec_formset = ProductSpecificationFormSet()
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'spec_formset': spec_formset,
        'title': 'Create New Product',
        'button_text': 'Create Product & Add Variants',
    }
    return render(request, 'home/product_form.html', context)

@login_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        spec_formset = ProductSpecificationFormSet(request.POST, instance=product)
        
        # Debug: Check form validity
        print(f"Product form valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Product form errors: {form.errors}")
        
        print(f"Image formset valid: {image_formset.is_valid()}")
        if not image_formset.is_valid():
            print(f"Image formset errors: {image_formset.errors}")
            for i, img_form in enumerate(image_formset):
                if not img_form.is_valid():
                    print(f"Image form {i} errors: {img_form.errors}")
        
        print(f"Spec formset valid: {spec_formset.is_valid()}")
        if not spec_formset.is_valid():
            print(f"Spec formset errors: {spec_formset.errors}")
        
        if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
            # Debug: Check is_active field before and after save
            print(f"Product is_active before save: {product.is_active}")
            print(f"Form data is_active: {form.cleaned_data.get('is_active')}")
            
            product = form.save()
            
            print(f"Product is_active after save: {product.is_active}")
            
            image_formset.save()
            spec_formset.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('product_variant_manage', slug=product.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)
        spec_formset = ProductSpecificationFormSet(instance=product)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'spec_formset': spec_formset,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'button_text': 'Update Product & Next',
    }
    return render(request, 'home/product_edit.html', context)

@login_required
def product_variant_manage(request, slug):
    print(f"=== product_variant_manage view called ===")
    print(f"Method: {request.method}")
    print(f"Slug: {slug}")
    
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        print(f"=== POST request received ===")
        print(f"POST keys: {list(request.POST.keys())}")
        
        # Debug: Check specifications-related fields
        for key in request.POST.keys():
            if 'specifications' in key:
                print(f"Specifications field: {key} = {repr(request.POST.get(key))}")
        
        variant_formset = ProductVariantFormSet(request.POST, instance=product)
        
        # Check if variant formset is valid
        if variant_formset.is_valid():
            print(f"Variant formset is valid")
            variants = variant_formset.save(commit=False)
            
            # Debug: Check each variant's specifications
            for i, variant in enumerate(variants):
                print(f"Variant {i}: {variant.name}")
                print(f"  Specifications: {repr(variant.specifications)}")
                
            # Handle image uploads for each variant
            for i, variant in enumerate(variants):
                if variant.pk:  # Only handle existing variants
                    # Get images for this variant from POST data
                    image_formset = ProductVariantImageFormSet(request.POST, request.FILES, instance=variant, prefix=f'variant_images-{i}')
                    
                    if image_formset.is_valid():
                        image_formset.save()
                    else:
                        # Add image errors to messages
                        for error in image_formset.errors:
                            messages.error(request, f'Image error for variant {variant.name}: {error}')
            
            # Save all variants
            variant_formset.save()
            messages.success(request, f'Variants for "{product.name}" have been updated successfully!')
            return redirect('product_variant_manage', product.slug)
        else:
            print(f"Variant formset errors: {variant_formset.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        variant_formset = ProductVariantFormSet(instance=product)
        
    context = {
        'variant_formset': variant_formset,
        'product': product,
        'title': f'Manage Variants: {product.name}',
        'button_text': 'Save Variants',
    }
    return render(request, 'home/variant_form.html', context)

@login_required
def variant_image_manage(request, slug, variant_id):
    """
    Dedicated page for managing images for a specific variant
    """
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    if request.method == 'POST':
        # Handle image actions (set main, delete)
        if 'set_main_image' in request.POST:
            image_id = request.POST.get('set_main_image')
            image = get_object_or_404(ProductVariantImage, id=image_id)
            if image.variant.id == variant.id:
                # Unset all other images as main
                ProductVariantImage.objects.filter(variant=variant).update(is_main_image=False)
                
                # Set this image as main
                image.is_main_image = True
                image.save()
                
                messages.success(request, f'Image "{image.alt_text}" set as main image!')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
            else:
                messages.error(request, 'Invalid image or variant mismatch.')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
                
        elif 'delete_image' in request.POST:
            image_id = request.POST.get('delete_image')
            image = get_object_or_404(ProductVariantImage, id=image_id)
            if image.variant.id == variant.id:
                # Delete image file and database record
                if image.image and os.path.exists(image.image.path):
                    os.remove(image.image.path)
                
                image.delete()
                messages.success(request, f'Image "{image.alt_text}" deleted successfully!')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
            else:
                messages.error(request, 'Invalid image or variant mismatch.')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
    
    context = {
        'variant': variant,
        'images': variant.images.all(),
        'title': f'Manage Images: {variant.name}',
    }
    return render(request, 'home/variant_image_manage.html', context)

@login_required
def add_variant_image_upload(request, slug, variant_id):
    """
    Add an image to a variant using a separate operation
    """
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            alt_text = request.POST.get('alt_text', '')
            display_order = request.POST.get('display_order', 0)
            is_main_image = 'is_main_image' in request.POST
            
            try:
                new_image = ProductVariantImage.objects.create(
                    variant=variant,
                    image=image_file,
                    alt_text=alt_text,
                    display_order=display_order,
                    is_main_image=is_main_image
                )
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'Image "{alt_text}" added successfully!',
                        'image_id': new_image.id,
                        'image_url': new_image.image.url if new_image.image else '',
                        'alt_text': new_image.alt_text,
                        'display_order': new_image.display_order,
                        'is_main_image': new_image.is_main_image
                    })
                messages.success(request, f'Image added successfully!')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'Error adding image: {str(e)}'
                    })
                messages.error(request, f'Error adding image: {str(e)}')
                return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
        else:
            messages.error(request, 'No image file provided.')
            return redirect('variant_image_manage', slug=slug, variant_id=variant_id)
    
    return redirect('variant_image_manage', slug=slug, variant_id=variant_id)

@login_required
def delete_variant(request, slug, variant_id):
    """
    Delete a single variant via AJAX request
    """
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, slug=slug)
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
            
            variant_name = variant.name
            variant.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request - return JSON response
                return JsonResponse({
                    'success': True,
                    'message': f'Variant "{variant_name}" has been deleted successfully.',
                    'variant_id': variant_id
                })
            else:
                # Regular request - redirect back with message
                messages.success(request, f'Variant "{variant_name}" has been deleted successfully.')
                return redirect('product_variant_manage', slug=slug)
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Error deleting variant: {str(e)}'
                })
            else:
                messages.error(request, f'Error deleting variant: {str(e)}')
                return redirect('product_variant_manage', slug=slug)
    
    # If not POST, redirect back
    return redirect('product_variant_manage', slug=slug)

@login_required
def set_main_image(request, image_id):
    """
    Set an image as the main image for its variant
    """
    if request.method == 'POST':
        image = get_object_or_404(ProductVariantImage, id=image_id)
        variant = image.variant
        
        # Unset all other images as main
        ProductVariantImage.objects.filter(variant=variant).update(is_main_image=False)
        
        # Set this image as main
        image.is_main_image = True
        image.save()
        
        messages.success(request, f'Image "{image.alt_text}" set as main image!')
        return redirect('product_variant_edit', slug=variant.product.slug, variant_id=variant.id)
    
    return redirect('product_variant_edit', slug=variant.product.slug, variant_id=variant.id)

@login_required
def delete_variant_image(request, image_id):
    """
    Delete a variant image
    """
    if request.method == 'POST':
        image = get_object_or_404(ProductVariantImage, id=image_id)
        variant = image.variant
        
        # Delete the image file
        if image.image:
            if os.path.exists(image.image.path):
                os.remove(image.image.path)
        
        # Delete the database record
        image.delete()
        
def product_variant_edit(request, slug, variant_id):
    print(f"=== product_variant_edit view called ===")
    print(f"Method: {request.method}")
    print(f"Slug: {slug}")
    print(f"Variant ID: {variant_id}")
    
    product = get_object_or_404(Product, slug=slug)
    variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
    
    if request.method == 'POST':
        print(f"=== POST request received ===")
        print(f"POST keys: {list(request.POST.keys())}")
        
        form = ProductVariantForm(request.POST, instance=variant)
        image_formset = ProductVariantImageFormSet(request.POST, request.FILES, instance=variant)
        
        # Debug: Check form validity
        print(f"Form valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        
        # Debug: Check specifications data
        print(f"POST data specifications: {request.POST.get('specifications', 'NOT_FOUND')}")
        if form.cleaned_data.get('specifications'):
            print(f"Specifications type: {type(form.cleaned_data.get('specifications'))}")
            print(f"Specifications value: {repr(form.cleaned_data.get('specifications'))}")
        
        print(f"Image formset valid: {image_formset.is_valid()}")
        if not image_formset.is_valid():
            print(f"Image formset errors: {image_formset.errors}")
            for i, img_form in enumerate(image_formset):
                print(f"Form {i} - Has instance pk: {bool(img_form.instance.pk)}")
                print(f"Form {i} - Has cleaned_data: {bool(img_form.cleaned_data)}")
                if img_form.cleaned_data:
                    print(f"Form {i} - Cleaned data keys: {list(img_form.cleaned_data.keys())}")
                    print(f"Form {i} - Has image in cleaned_data: {'image' in img_form.cleaned_data}")
                if not img_form.is_valid():
                    print(f"Image form {i} errors: {img_form.errors}")
        
        if form.is_valid() and image_formset.is_valid():
            form.save()
            image_formset.save()
            messages.success(request, f'Variant "{variant.name}" has been updated successfully!')
            return redirect('product_variant_manage', slug=product.slug)
        elif form.is_valid():
            # Save the main form even if image formset has validation issues
            form.save()
            messages.success(request, f'Variant "{variant.name}" has been updated successfully! (Note: Image upload had validation issues)')
            return redirect('product_variant_manage', slug=product.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductVariantForm(instance=variant)
        image_formset = ProductVariantImageFormSet(instance=variant)
        
    context = {
        'form': form,
        'image_formset': image_formset,
        'product': product,
        'variant': variant,
        'title': f'Edit Variant: {variant.name}',
        'button_text': 'Update Variant',
    }
    return render(request, 'home/variant_edit.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Optional offer price from query string (e.g. from flash sale links)
    offer_price = request.GET.get('offer_price')
    
    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category').prefetch_related('images')[:4]
    
    images = product.images.all()
    specifications = product.specifications.all()
    
    context = {
        'product': product,
        'offer_price': offer_price,
        'related_products': related_products,
        'images': images,
        'specifications': specifications,
        'title': product.name,
    }
    return render(request, 'home/product_detail.html', context)

@login_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('product_list')
    
    context = {
        'product': product,
    }
    return render(request, 'home/product_confirm_delete.html', context)

def add_to_cart(request, product_id):
    """
    Add a specific product variant to the cart.

    The URL still receives the parent product_id, but the concrete variant
    to add is determined from POST data (`variant_id`). We store cart items
    keyed by variant_id in the session so that different variants of the
    same product can coexist in the cart.
    """
    product = get_object_or_404(Product, id=product_id)

    # Only allow POST for adding to cart so we can safely read variant_id
    if request.method != "POST":
        messages.error(request, "Invalid request method for adding to cart.")
        return redirect(request.META.get("HTTP_REFERER", "cart_detail"))

    variant_id = request.POST.get("variant_id")

    if variant_id:
        # Ensure the variant actually belongs to this product
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
    else:
        # Fallback to the first active variant if none provided
        variant = product.variants.filter(is_active=True).first() or product.variants.first()

    if not variant:
        messages.error(request, "This product has no available variants to add to cart.")
        return redirect(request.META.get("HTTP_REFERER", "cart_detail"))

    cart = request.session.get("cart", {})
    variant_key = str(variant.id)

    if variant_key in cart:
        cart[variant_key] += 1
    else:
        cart[variant_key] = 1

    request.session["cart"] = cart
    messages.success(request, f'"{product.name} - {variant.name}" added to cart.')

    return redirect(request.META.get("HTTP_REFERER", "cart_detail"))

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for variant_id, quantity in cart.items():
        try:
            variant = ProductVariant.objects.select_related("product").get(id=variant_id)
            product = variant.product

            # Prefer sale_price when available, otherwise use regular price
            unit_price = variant.sale_price if getattr(variant, "sale_price", None) else variant.price
            subtotal = unit_price * quantity
            total_price += subtotal

            cart_items.append({
                "product": product,
                "variant": variant,
                "unit_price": unit_price,
                "quantity": quantity,
                "subtotal": subtotal,
            })
        except ProductVariant.DoesNotExist:
            continue
            
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'Shopping Cart',
    }
    return render(request, 'home/cart_detail.html', context)

def remove_from_cart(request, variant_id):
    """
    Remove a specific variant from the cart (identified by variant_id).
    """
    cart = request.session.get("cart", {})
    variant_key = str(variant_id)

    if variant_key in cart:
        del cart[variant_key]
        request.session["cart"] = cart
        messages.success(request, "Item removed from cart.")

    return redirect("cart_detail")


def update_cart(request, variant_id):
    """
    Update quantity for a specific variant in the cart.
    """
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get("cart", {})
        variant_key = str(variant_id)

        if quantity > 0:
            cart[variant_key] = quantity
        else:
            if variant_key in cart:
                del cart[variant_key]

        request.session["cart"] = cart
        messages.success(request, "Cart updated.")
    
    return redirect('cart_detail')

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', reverse('home'))
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'home/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@require_http_methods(["POST"])
def ai_chat(request):
    """
    AI Chat endpoint for Samsung product assistance using OpenAI API
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        product_id = data.get('product_id')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Fetch current product if context provided
        current_product = None
        if product_id:
            current_product = Product.objects.filter(id=product_id, is_active=True).first()

        # Fetch all active products for broad context
        products = Product.objects.filter(is_active=True).select_related('category')
        
        # Build product context
        product_context = "## Available Products at World Tech Partners:\n\n"
        if current_product:
            product_context += f"CURRENTLY VIEWED PRODUCT: **{current_product.name}**\n"
            starting_price = current_product.get_starting_price()
            if starting_price:
                product_context += f"- Price: starting at KSH {starting_price:,.2f}\n"
            product_context += f"- Details: {current_product.description}\n\n"
            product_context += "OTHER PRODUCTS:\n"

        for product in products:
            if current_product and product.id == current_product.id:
                continue
            starting_price = product.get_starting_price()
            price_str = f"starting at KSH {starting_price:,.2f}" if starting_price else "Price on request"
            product_context += f"- {product.name} ({product.category.name if product.category else 'Samsung'}): {price_str}\n"
        
        # Try to use OpenAI API if available
        try:
            from django.conf import settings
            from openai import OpenAI
            
            # Initialize OpenAI client
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Create professional system prompt
            current_focus = f"The user is currently looking at: {current_product.name}. " if current_product else ""
            
            system_prompt = f"""You are a professional AI sales and technical specialist for World Tech Partners, an authorized Samsung dealer in Kenya.

CONSTRAINTS:
1. ONLY answer questions about Samsung products (phones, TVs, appliances, etc.), Samsung repair services, and World Tech Partners' services.
2. If the user asks about ANY other brand or topic, politely decline and steer back to Samsung.
3. BE PROFESSIONAL, concise, and to the point.
4. You are encouraged to use your external technical knowledge about Samsung devices to provide detailed advice.
5. {current_focus}If the user asks about 'this product', focus on the currently viewed product.

SERVICES PROVIDED:
- Sales of genuine Samsung electronics.
- Professional Samsung repair and maintenance services.
- Warranty support.
- Nationwide delivery in Kenya.

PRODUCT CONTEXT FROM OUR STORE:
{product_context}
"""
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o",  # Using gpt-4o for better performance
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=350,
                temperature=0.5
            )
            
            ai_response = response.choices[0].message.content
            print(ai_response)
        except (ImportError, AttributeError):
            # Fallback to keyword-based responses if OpenAI not configured
            ai_response = get_fallback_response(user_message, products)
        except Exception as e:
            # Log error and use fallback
            print(f"OpenAI API Error: {e}")
            ai_response = get_fallback_response(user_message, products)
        
        return JsonResponse({'response': ai_response})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_fallback_response(message, products=None):
    """Fallback responses when OpenAI is not available"""
    message_lower = message.lower()
    
    # Check for off-topic queries
    off_topic_keywords = ['politics', 'religion', 'weather', 'sports', 'news', 'apple', 'iphone', 'huawei', 'oppo']
    if any(keyword in message_lower for keyword in off_topic_keywords):
        return "I'm here to help with Samsung products and our services at World Tech Partners. Is there a Samsung device you'd like to know more about?"
    
    # Product-specific responses using database
    if products:
        for product in products:
            starting_price = product.get_starting_price()
            if product.name.lower() in message_lower:
                price_info = f"available for KSH {starting_price:,.2f}" if starting_price else "available"
                return f"We have the {product.name} {price_info}. {product.description[:100] if product.description else 'Contact us for more details!'}"
    
    # General category responses
    if any(word in message_lower for word in ['price', 'cost', 'how much']):
        return "Our Samsung products range from KSH 15,000 to KSH 150,000. We offer flexible payment options. What specific product are you interested in?"
    elif any(word in message_lower for word in ['galaxy', 'phone', 's24', 's23', 'fold']):
        phone_products = [p for p in products if p.category and 'phone' in p.category.name.lower()] if products else []
        if phone_products:
            sample = phone_products[0]
            starting_price = sample.get_starting_price()
            price_info = f"at KSH {starting_price:,.2f}" if starting_price else ""
            return f"We have the latest Galaxy series! For example, the {sample.name} {price_info}. Which model interests you?"
        return "We have the latest Galaxy series including S24 Ultra, S23, and Z Fold models. Which model interests you?"
    elif any(word in message_lower for word in ['tv', 'television', 'qled']):
        return "Our Samsung TV range includes QLED, OLED, and Crystal UHD models from 43\" to 85\". What size are you looking for?"
    elif any(word in message_lower for word in ['watch', 'smartwatch']):
        return "We offer Samsung Galaxy Watch 6 and Watch 5 series. They pair perfectly with your Galaxy phone!"
    elif any(word in message_lower for word in ['buds', 'earbuds', 'headphones']):
        return "We have Galaxy Buds Pro 2 and Buds FE with premium sound quality. Which features are most important to you?"
    elif any(word in message_lower for word in ['warranty', 'guarantee']):
        return "All our Samsung products come with official warranty. As an authorized dealer, we provide full warranty support!"
    elif any(word in message_lower for word in ['delivery', 'shipping']):
        return "We offer delivery across Kenya. Where would you like your purchase delivered?"
    else:
        return "I'm here to help with Samsung products! Ask me about phones, TVs, watches, buds, pricing, or delivery. What interests you?"
    return render(request, 'home/product_detail.html', context)


def contact_submit(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    return redirect('home')


@login_required
def notifications_list(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    notifications = ContactMessage.objects.all().order_by('-created_at')
    
    # Simple pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home/notifications.html', {'page_obj': page_obj})


@login_required
def notification_mark_read(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Access denied.'}, status=403)
    
    notification = get_object_or_404(ContactMessage, pk=pk)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications_list')
def handler404(request, exception):
    """Custom 404 error handler: redirect to home with message"""
    messages.error(request, "The page you are looking for does not exist.")
    return redirect('home')

def handler500(request):
    """Custom 500 error handler: avoid redirect loops"""
    from django.http import HttpResponse
    return HttpResponse("""
        <h1>500 - Server Error</h1>
        <p>Something went wrong on our end. Please <a href="/">click here</a> to go back to the homepage.</p>
    """, status=500)

def handler403(request, exception=None):
    """Custom 403 error handler: redirect to home with message"""
    messages.error(request, "You do not have permission to access that page.")
    return redirect('home')

def handler400(request, exception=None):
    """Custom 400 error handler: redirect to home with message"""
    messages.error(request, "There was a problem with your request.")
    return redirect('home')
