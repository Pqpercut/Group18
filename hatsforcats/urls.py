"""
URL configuration for hatsforcats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from ecommerceapp.views import HomeView, InventoryProductListView, InventoryProductDetailView, InventoryCreateProductView, InventoryProductDeleteView, InventoryProductEditView, EditVariantView, CreateVariantView, DeleteVariantView, CustomLoginView, RegistrationView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from ecommerceapp.views import InventoryProductListView, InventoryProductDetailView, InventoryCreateProductView, InventoryProductDeleteView, InventoryProductEditView, EditVariantView, CreateVariantView, DeleteVariantView
from ecommerceapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    # Created by Adam 23/11/2024 / Placeholder template, to be replaced with template from front end
    ##### PRODUCTS
    path("inventory-management/", InventoryDashboard.as_view(), name="IMS - Dashboard"),
    path("inventory-management/products/", InventoryProductListView.as_view(), name="IMS - Product List"),
    path("inventory-management/products/<int:pk>/", InventoryProductDetailView.as_view(), name="IMS - Product Detail"),
    path("inventory-management/products/create/", InventoryCreateProductView.as_view(),name="IMS - Create Product"),
    path("inventory-management/products/<int:pk>/edit/", InventoryProductEditView.as_view(), name="IMS - Product Edit"),
    path("inventory-management/products/<int:pk>/delete/", InventoryProductDeleteView.as_view(), name="IMS - Product Delete"),

    path("inventory-management/variants/<int:pk>/edit/", EditVariantView.as_view(), name="IMS - Product Variant Edit"),\
    path("inventory-management/products/<int:product_pk>/create-variant/", CreateVariantView.as_view(), name="IMS - Product Variant Create"),
    path("inventory-management/variants/<int:pk>/delete/", DeleteVariantView.as_view(), name="IMS - Product Variant Delete"),
    
    ##### ORDERS
    path("inventory-management/orders/", OrderListView.as_view(), name="IMS - Order List"),
    path("inventory-management/orders/<int:pk>/", OrderDetailView.as_view(), name="IMS - Order Detail"),
    
    ##### CUSTOMERS
    path("inventory-management/customers/", UserListView.as_view(), name="IMS - Customers"),

    path("inventory-management/discount/", DiscountListView.as_view(), name="IMS - Discounts"),
    path("inventory-management/discount/create", DiscountCreateView.as_view(), name="IMS - Discount Create"),
    path("inventory-management/discount/<int:pk>/edit/", DiscountUpdateView.as_view(), name="IMS - Discount Edit"),




    
    # Created by Adam 01/12/2024 
    path('', HomeView.as_view(), name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),


    path('basket', BasketView.as_view(), name='basket'), 
    path('checkout-page', CheckoutView.as_view(), name='checkout'), 


    path('password-reset/', PasswordResetView.as_view(template_name='login/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),

    path('order-summary/<int:order_id>/', OrderSummaryView.as_view(), name='order-summary'),
    path('unauthorized/', TemplateView.as_view(template_name="unauthorized.html"), name='unauthorized'),

    #Created by Qasim 
    ##path("catalogue",catalogueView, name = "Catalogue"),
    path("catalogue",CatalogueViewClass.as_view(), name = "Catalogue"),
    path("contact-page", ContactPageView, name="Contact-Page"),
    path("Contact-Queries", ContactQueryView, name="Contact Queries"),
    path("CreateReview/<int:pk>/", CreateReviewClass.as_view(), name= "Reviews"),
    path("Wishlist/", WishlistView.as_view(),name="Wishlist"),
    path("Wishlist/<int:pk>/", WishlistView.as_view(),name="Wishlist"),


    path("tempBasket.html", basketRem, name="basketRem"),
    path("", productDisplay, name="productDisplay"),
    path("product/<int:pk>", VariantDisplayView.as_view(), name="variantDisplay"),
    path("bluesky_post", bluesky_post, name='bluesky_post')

    #ADAM
     path('user/<int:pk>', UserProfileView.as_view(), name='user home'),
     path('user/orders', UserProfileOrdersView.as_view(), name='user orders'),
     path('user/orders/<int:pk>', UserProfileOrderDetailView.as_view(), name='user orders detail'),
     path('user/address', UserProfileAddressView.as_view(), name='user addresses'),
     path('user/address/<int:pk>/update', UserProfileAddressUpdateView.as_view(), name='user addresses update'),
     path('user/address/create', UserProfileAddressCreateView.as_view(), name='user addresses create'),
     path('user/address/<int:pk>/delete', UserAddressDeleteView.as_view(), name='user addresses delete'),


    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),


]

# This is only to serve media files in the development environement. When we host this on the Universities Apache Server we will store the files in a seperate location on the Server
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
