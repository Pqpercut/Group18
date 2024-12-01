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
from ecommerceapp.views import HomeView, InventoryProductListView, InventoryProductDetailView, InventoryCreateProductView, InventoryProductDeleteView, InventoryProductEditView, EditVariantView, CreateVariantView, DeleteVariantView, CustomLoginView, RegistrationView
from ecommerceapp.views import catalogueView
urlpatterns = [
    path('admin/', admin.site.urls),

    # Created by Adam 23/11/2024 / Placeholder template, to be replaced with template from front end
    path("inventory-management/products/", InventoryProductListView.as_view(), name="IMS - Product List"),
    path("inventory-management/products/<int:pk>/", InventoryProductDetailView.as_view(), name="IMS - Product Detail"),
    path("inventory-management/products/create/", InventoryCreateProductView.as_view(),name="IMS - Create Product"),
    path("inventory-management/products/<int:pk>/edit/", InventoryProductEditView.as_view(), name="IMS - Product Edit"),
    path("inventory-management/products/<int:pk>/delete/", InventoryProductDeleteView.as_view(), name="IMS - Product Delete"),

    path("inventory-management/variants/<int:pk>/edit/", EditVariantView.as_view(), name="IMS - Product Variant Edit"),\
    path("inventory-management/products/<int:product_pk>/create-variant/", CreateVariantView.as_view(), name="IMS - Product Variant Create"),
    path("inventory-management/variants/<int:pk>/delete/", DeleteVariantView.as_view(), name="IMS - Product Variant Delete"),
    
    # Created by Adam 01/12/2024 
    path('', HomeView.as_view(), name='home' ), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),


    #Created by Qasim 
    path("catalogue",catalogueView, name = "Catalogue")
]

# This is only to serve media files in the development environement. When we host this on the Universities Apache Server we will store the files in a seperate location on the Server
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
