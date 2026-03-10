"""
URL configuration for Samsung project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse
from home.views import (
    home, product_list, product_create, product_edit, 
    product_delete, product_detail, product_variant_manage, product_variant_edit, delete_variant, set_main_image, delete_variant_image, add_to_cart, 
    cart_detail, remove_from_cart, update_cart, add_variant_image_upload,
    user_login, user_logout, ai_chat,variant_image_manage,
    contact_submit, notifications_list, notification_mark_read
)
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', lambda x: HttpResponse(status=204)),
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('products/<slug:slug>/edit/', product_edit, name='product_edit'),
    path('products/<slug:slug>/variants/', product_variant_manage, name='product_variant_manage'),
    path('products/<slug:slug>/variants/<int:variant_id>/edit/', product_variant_edit, name='product_variant_edit'),
    path('products/<slug:slug>/variants/<int:variant_id>/delete/', delete_variant, name='delete_variant'),
    path('products/<slug:slug>/variants/<int:variant_id>/add_image/', add_variant_image_upload, name='add_variant_image_upload'),
    path('products/<slug:slug>/variants/<int:variant_id>/images/', variant_image_manage, name='variant_image_manage'),
    path('products/<slug:slug>/variants/<int:variant_id>/delete-image/<int:image_id>/', delete_variant_image, name='delete_variant_image'),
    path('products/<slug:slug>/delete/', product_delete, name='product_delete'),
    
    # Notifications URLs
    path('contact/submit/', contact_submit, name='contact_submit'),
    path('notifications/', notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', notification_mark_read, name='notification_mark_read'),

    # Cart URLs
    path('cart/', cart_detail, name='cart_detail'),
    # add_to_cart keeps product_id in the URL; variant_id is provided via POST data
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # remove/update operate on concrete variant ids stored in the cart
    path('cart/remove/<int:variant_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:variant_id>/', update_cart, name='update_cart'),
    
    # API URLs
    path('api/chat/', ai_chat, name='ai_chat'),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
handler403 = 'home.views.handler403'
handler400 = 'home.views.handler400'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else settings.BASE_DIR / 'static')
else:
    # Fallback to serve media files in production via Django
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
