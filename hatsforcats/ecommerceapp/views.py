from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.urls import reverse_lazy
from django.db.models import Sum
from .forms import VariantForm, UpdateStockForm, CreateVariantForm, EditVariantForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, FormView, CreateView
from django.shortcuts import get_object_or_404, redirect
from .forms import ContactEnquiryForm
from django.db.models import Min
from django.http import HttpResponse
from django.http import HttpResponseRedirect

class InventoryProductListView (ListView):
    # Created by Adam Ahmed 23/11/2024
    ''' View for IMS System that displays all the products currently available and allows new product creation '''
    model = Product
    template_name = "inventory-management/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        low_stock_threshold = 5  # Define a low stock threshold
        products_with_variants = []

        for product in Product.objects.all():
            variants = product.productvariant.all()
            total_stock = variants.aggregate(total=Sum('stocklevel'))['total'] or 0
            is_low_stock = total_stock < low_stock_threshold
            products_with_variants.append({
                'product': product,
                'variant_count': variants.count(),
                'is_low_stock': is_low_stock,
                'total_stock': total_stock,
            })
        context['products_with_variants'] = products_with_variants
        return context

class InventoryProductDetailView(DetailView):
    # Created by Adam Ahmed 23/11/2024
    ''' View for IMS System that shows the product details and all variants & allows stock updates '''
    model = Product
    template_name = "inventory-management/product_detail.html"
    context_object_name = "product"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UpdateStockForm(request.POST)

        if form.is_valid():
            variant = form.cleaned_data['variant']
            stock_level = form.cleaned_data['stocklevel']
            variant.stocklevel = stock_level
            variant.save()
        return redirect('IMS - Product Detail', pk=self.object.pk)
    
class InventoryCreateProductView(CreateView):
    # Created by Adam Ahmed 23/11/2024
    ''' View that allows for new product creation '''
    model = Product
    template_name = "inventory-management/product_create.html"
    fields = ['name', 'description', 'availability']

    def get_success_url(self):
        # Redirect back to the product list after successful creation
        return reverse_lazy('IMS - Product List')

class InventoryProductEditView(UpdateView):
    # Created by Adam Ahmed 23/11/2024
    ''' View that allows already created products to be edited '''
    model = Product
    template_name = "inventory-management/product_edit.html"
    context_object_name = "product"
    fields = ['name', 'description', 'availability']

    def get_success_url(self):
        return reverse_lazy('IMS - Product Detail', kwargs={'pk': self.object.pk})
     
class InventoryProductDeleteView(DeleteView):
    # Created by Adam Ahmed 23/11/2024
    ''' Seperate Confirmation View that requires another button click to delete a product '''
    model = Product
    template_name = "inventory-management/product_confirm_delete.html"
    success_url = reverse_lazy('IMS - Product List')

class CreateVariantView(CreateView):
    # Created by Adam Ahmed 23/11/2024
    # Updated by Adam Ahmed 30/11/2024
    '''Allows creation of product variant details and the ability to upload images'''
    model = ProductVariant
    template_name = "inventory-management/product_create_variant.html"
    form_class = CreateVariantForm

    def form_valid(self, form):
        # Save the product variant
        product = Product.objects.get(pk=self.kwargs['product_pk'])
        form.instance.productID = product
        response = super().form_valid(form)

        # Handle multiple file uploads
        images = form.cleaned_data.get('images', [])
        for image in images:
            ImagePath.objects.create(productVariantID=form.instance, imagepath=image)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_pk'] = self.kwargs['product_pk']
        return context

    def get_success_url(self):
        return reverse_lazy('IMS - Product Detail', kwargs={'pk': self.kwargs['product_pk']})


class EditVariantView(UpdateView):
    # Created by Adam Ahmed 23/11/2024
    # Updated by Adam Ahmed 30/11/2024
    '''Allows edit of product variant details and the ability to upload more images'''
    model = ProductVariant
    template_name = "inventory-management/product_variant_edit.html"
    form_class = EditVariantForm

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle multiple file uploads
        images = form.cleaned_data.get('images', [])
        for image in images:
            ImagePath.objects.create(productVariantID=self.object, imagepath=image)

        return response

    def get_success_url(self):
        return reverse_lazy('IMS - Product Detail', kwargs={'pk': self.object.productID.pk})
    
class DeleteVariantView(DeleteView):
    # Created by Adam Ahmed 23/11/2024
    ''' View that allows Product Variants to be deleted with confirmation '''
    model = ProductVariant
    template_name = "inventory-management/product_variant_delete.html"

    def get_success_url(self):
        # Redirect to the product detail page after deletion
        return reverse_lazy('IMS - Product Detail', kwargs={'pk': self.object.productID.pk})

def catalogueView(request, *args, **kwargs):
    ###Written by Qasim Farooq 29/11/24

   ##Get filter in URL
    filterList = request.GET.getlist('filter')
    ##Set string of filter values
    filterValue = ""
    for x in filterList:
        ##Add all filter values to list and seperate with comma
        filterValue = filterValue + x + ","


    ##Assign the correct Order by Value
    orderValue = request.GET.get("order","default-value")
    if orderValue == 'price':
        orderValue = 'productvariant__price'
    else:
        orderValue = 'name'

    ##Get a query of all products
    productList = Product.objects.all()

    #If there is a filter then filter the query to only those products
    if len(filterList) != 0:
            
        productList = productList.filter(categories__categories__in = filterList)

    ##Order the query
    ##Aggregate the values to be able to prevent multiple variants showing on the list
    productList = productList.annotate(min_val=Min(orderValue))
    productList = productList.annotate(img_path=Min('productvariant__imagepath__imagepath'))
    
    productList = productList.order_by('min_val')
    ##Return the query
    context = {"ProductList" : productList}

    
    return render(request, "product-catalogue/product_catalogue.html", context)



def ContactPageView(request, *args, **kwargs):
    submitted = False
    if request.method == 'POST':
        contactform = ContactEnquiryForm(request.POST)
        if contactform.is_valid():
            contactform.save()
            return HttpResponseRedirect('contact-page?submit=True')
    else:
        contactform = ContactEnquiryForm()
        if 'submit' in request.GET:
            submitted = True
    context = {"ContactForm": contactform, 'submitted' : submitted}
    return render(request,'general-pages/Contact-Page.html',context )