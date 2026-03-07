from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Product, ProductCategory, ProductImage, ProductSpecification, ContactMessage
from .forms import ProductForm, ProductImageFormSet, ProductSpecificationFormSet, ContactMessageForm
from .forms_login import CustomLoginForm

def home(request):
    # Hero product: first featured product, or newest active product
    hero_product = Product.objects.filter(
        is_active=True, is_featured=True
    ).select_related('category').prefetch_related('images').first()
    if not hero_product:
        hero_product = Product.objects.filter(
            is_active=True
        ).select_related('category').prefetch_related('images').first()

    # Featured products for the hero cards (up to 4, excluding hero product)
    featured_qs = Product.objects.filter(is_active=True).exclude(
        pk=hero_product.pk if hero_product else 0
    ).select_related('category').prefetch_related('images').order_by('-is_featured', '-created_at')[:12]

    # All products for the "Our Innovations" section
    all_products = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images').order_by('-created_at')[:12]

    # Categories for quick-links
    categories = ProductCategory.objects.all()

    # Categories with their products (for per-category sections)
    categories_with_products = ProductCategory.objects.prefetch_related(
        Prefetch(
            'product_set',
            queryset=Product.objects.filter(is_active=True).select_related('category').prefetch_related('images').order_by('-created_at')[:8],
            to_attr='active_products'
        )
    )

    # Flash sale products (products with a sale price)
    flash_sale_products = Product.objects.filter(
        is_active=True, sale_price__isnull=False
    ).select_related('category').prefetch_related('images').order_by('sale_price')[:8]

    # Recent arrivals (newest products)
    recent_arrivals = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images').order_by('-created_at')[:8]

    context = {
        'hero_product': hero_product,
        'featured_products': featured_qs,
        'products': all_products,
        'categories': categories,
        'categories_with_products': categories_with_products,
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
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Get search query
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            name__icontains=search_query
        )
    
    # Get sort option
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
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
        
        if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
            product = form.save()
            image_formset.instance = product
            image_formset.save()
            spec_formset.instance = product
            spec_formset.save()
            
            messages.success(request, f'Product "{product.name}" has been created successfully!')
            return redirect('product_list')
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
        'button_text': 'Create Product',
    }
    return render(request, 'home/product_form.html', context)

@login_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        spec_formset = ProductSpecificationFormSet(request.POST, instance=product)
        
        if form.is_valid() and image_formset.is_valid() and spec_formset.is_valid():
            product = form.save()
            image_formset.save()
            spec_formset.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully!')
            return redirect('product_list')
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
        'button_text': 'Update Product',
    }
    return render(request, 'home/product_form.html', context)

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
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
        
    request.session['cart'] = cart
    messages.success(request, "Product added to cart!")
    
    # Redirect back to where user came from, or cart detail
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue
            
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'Shopping Cart',
    }
    return render(request, 'home/cart_detail.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, "Product removed from cart.")
    
    return redirect('cart_detail')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if quantity > 0:
            cart[product_id_str] = quantity
        else:
            if product_id_str in cart:
                del cart[product_id_str]
        
        request.session['cart'] = cart
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
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Fetch product data from database
        products = Product.objects.filter(is_active=True).select_related('category')[:20]
        
        # Build product context
        product_context = "## Available Products:\n\n"
        for product in products:
            product_context += f"**{product.name}** ({product.category.name if product.category else 'Uncategorized'})\n"
            product_context += f"- Price: KSH {product.price:,.2f}\n"
            if product.description:
                product_context += f"- Description: {product.description[:200]}\n"
            if product.model_code:
                product_context += f"- Model: {product.model_code}\n"
            product_context += "\n"
        
        # Try to use OpenAI API if available
        try:
            from django.conf import settings
            from openai import OpenAI
            
            # Check if API key is configured
           
            
            # Initialize OpenAI client
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Create enhanced system prompt with product context
            system_prompt = f"""You are a helpful AI assistant for World Tech Partners, 
an authorized Samsung dealer in Kenya.

IMPORTANT GUIDELINES:
- Only answer questions about Samsung products, electronics, and our services
- Politely decline to answer questions about other topics (politics, religion, other brands, etc.) but respond to greetings
- Use the product information provided below to answer specific product questions
- Be friendly, professional, and knowledgeable
- Keep responses concise (2-3 sentences max)
- If asked about a product not in our inventory, mention we can source it

YOUR SERVICES:
- Product sales (phones, TVs, watches, buds, appliances)
- Warranty and support
- Delivery across Kenya
- Genuine Samsung products only

{product_context}

When users ask off-topic questions, politely say:
"I'm here to help with Samsung products and our services at World Tech Partners. Is there a Samsung device you'd like to know more about?"
"""
            
            # Call OpenAI API (new format for openai>=1.0.0)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=250,
                temperature=0.7
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
        # Check if asking about specific product
        for product in products:
            if product.name.lower() in message_lower or (product.model_code and product.model_code.lower() in message_lower):
                return f"We have the {product.name} available for KSH {product.price:,.2f}. {product.description[:100] if product.description else 'Contact us for more details!'}"
    
    # General category responses
    if any(word in message_lower for word in ['price', 'cost', 'how much']):
        return "Our Samsung products range from KSH 15,000 to KSH 150,000. We offer flexible payment options. What specific product are you interested in?"
    elif any(word in message_lower for word in ['galaxy', 'phone', 's24', 's23', 'fold']):
        phone_products = [p for p in products if p.category and 'phone' in p.category.name.lower()] if products else []
        if phone_products:
            sample = phone_products[0]
            return f"We have the latest Galaxy series! For example, the {sample.name} at KSH {sample.price:,.2f}. Which model interests you?"
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
