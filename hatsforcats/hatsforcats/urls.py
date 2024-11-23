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
from django.contrib import admin
from django.urls import path
from ecommerceapp.views import InventoryProductListView, InventoryProductDetailView, InventoryCreateProductView, InventoryProductDeleteView, InventoryProductEditView, EditVariantView, CreateVariantView, DeleteVariantView

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
]

