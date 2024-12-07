from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.urls import reverse_lazy
from django.db.models import Sum
from .forms import VariantForm, UpdateStockForm, CreateVariantForm, EditVariantForm, RegistrationForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, FormView, CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from .forms import ContactEnquiryForm
from django.db.models import Min
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required


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

	searchValue = request.GET.get("search","")

	if searchValue != '':
		productList = productList.filter(name__contains=searchValue)
		print("searching")
	##Return the query
	context = {"ProductList" : productList}

	
	return render(request, "product-catalogue/product_catalogue.html", context)

class CustomLoginView(LoginView):
	template_name = 'login/login.html'  
	# redirect_authenticated_user = True 

	def get_success_url(self):
		if self.request.user.groups.filter(name='admin').exists():
			return 'inventory-managment/product'
		elif self.request.user.groups.filter(name='customer').exists():
			return 'home'
		return super().get_success_url()
	
class RegistrationView(FormView):
	template_name = 'login/register.html'  # Template for the registration page
	form_class = RegistrationForm
	success_url = reverse_lazy('login')  # Redirect after successful registration

	def form_valid(self, form):
		# Save the user
		user = form.save()

		# Add the user to the 'customer' group by default
		group = Group.objects.get(name='Customer')  # Ensure the group exists in the DB
		user.groups.add(group)


		return super().form_valid(form)
	
class HomeView(TemplateView):
	template_name = "home-page.html"


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


@user_passes_test("ecommerceapp.Admin") 
def ContactQueryView(request,*args,**kwargs):
	queries = ContactTable.objects.all()
	context = {"queryTable": queries}
	return render(request,'general-pages/ViewContactQuery.html', context)


#display products
def productDisplay(request):
#written by Sakina Khaki
	allitems = Product.objects.all()
	itemNames = {
		'products' : allitems
	}

	#viewing
	return render(request, "admin/temp_basket/tempProducts.html", itemNames)


#display product varients
#get product_id. if product_id = variant, display it else dont
def variantDisplay(request, quantity):
#written by Sakina Khaki
	#print("blorp")

	#productid = request.POST.get("productid")
	productid = 1 #testing purpose


	product = Product.objects.get(id = productid)
	name = product.name
	desc = product.description

	allitems = ProductVariant.objects.all()
	allitems = allitems.filter(productID = productid)

	sizes = ["S", "M", "L", "XL"] #all available sizes
	available_sizes = set()
	for v in allitems:
		for s in v.size:
			available_sizes.add(s)
	

	#when a colour is clicked
	if request.method == "POST":
		#print(request.POST.get("colour"))
		col = request.POST.get("colour")
		available_sizes.clear()
		for i in allitems: 
			if i.colour == col:
				available_sizes.add(i.size)

	#when size is clicked
	if request.method == "POST":
		print(request.POST.get("size"))

	itemNames = {
		'name' : name, 'desc' : desc,
		'variants' : allitems,
		'sizes' : sizes, 'available_sizes' : available_sizes,
		'quantity' : quantity
	}

	#viewing
	return render(request, "productdetailpage.html", itemNames)


@permission_required('ecommerceapp.Customer') 
#add to basket
def basketAdd(request):
#written by Sakina Khaki
	#gets everyhting from post data
	if request.method == "POST" and request.POST.get("form_name") == "add_basket":
		#print(request.POST.get("variantid"))
		variantid = request.POST.get("variantid")  
		quantity = int(request.POST.get("quantity"))
		amendQuantity = False

		#get basketid
		#basketid = Basket.objects.get(userID=request.user).id
		
		#for testing
		basket = Basket.objects.get(userID=1)
		basketid = basket.id

		#get varientid
		variant = ProductVariant.objects.get(id=variantid)

		#check if user has ordered item before already
		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()

		#checks which btn
		btn = request.POST.get("add_button")

		if btn == "add_one":
			amendQuantity = True
			quantity += 1
			print(quantity)

		elif btn == "rem_one" and quantity > 1:
			amendQuantity = True
			quantity -= 1
			print(quantity)

		elif btn == "add_to_basket":
			print("cheking basket...")
			
			if basketitem: 
				print("added", quantity, "to EXISTING")
				basketitem.quantity += quantity
			else: 
			#create new basketitem entry
				print("added", quantity, "to NEW")
				BasketItem.objects.create(basketID=basket, variantID=variant, quantity=quantity)

	else:
		quantity = 1

	return(variantDisplay(request, quantity))
		#return render(request, "admin/temp_basket/tempProducts.html")



@permission_required('ecommerceapp.Customer')
#remove from basket 
def basketRem(request):
#written by Sakina Khaki
	if request.method == "POST":
		#print("beep")
		#get basketid
		#basketid = Basket.objects.get(userID=request.user).id

		#for testing
		basketid = Basket.objects.get(userID=1)

		variantid = request.POST.get("variantid")
		variant = ProductVariant.objects.get(id=variantid)

		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()

		#which btn? 
		btn = request.POST.get("remove_btn")
		if basketitem:
			if btn == "add_one":
				print("quantitiy changed")
				basketitem.quantity += 1
				basketitem.save()

			elif btn == "rem_all" or basketitem.quantity == 1:
				print("removed")
				basketitem.delete()
			
			else:
				print("quantitiy changed")
				basketitem.quantity -= 1
				basketitem.save()


	return(viewBasket(request))


@permission_required('ecommerceapp.Customer')
#veiw basket
def viewBasket(request):
#written by Sakina Khaki
	#print("beep")
	#get basketid
	#basketid = Basket.objects.get(userID=request.user).id

	#for testing
	basketid = Basket.objects.get(userID=1)

	allitems = BasketItem.objects.filter(basketID=basketid)

	total = 0
	for i in allitems:
		variant = ProductVariant.objects.get(id=i.variantID.id)
		total += (variant.price * i.quantity)
	#print(total)

	itemNames = {
		'basket' : allitems,
		'total' : total
	}


	#viewing the absket
	return render(request, "admin/temp_basket/tempBasket.html", itemNames)


@permission_required('ecommerceapp.Customer')
#checkout
def checkout(request):
	return render(request, "admin/temp_basket/tempCheckout.html")

