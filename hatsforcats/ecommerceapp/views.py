from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import *

class InventoryProductListView (ListView):
    model = Product
    template_name = "inventory-management/product_list.html"  
    context_object_name = "products"  

# class InventoryProductDetailView (UpdateView):

# class InventoryProductDeleteView (DeleteView):
