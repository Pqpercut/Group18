from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.urls import reverse_lazy,  reverse
from django.db.models import Sum
from .forms import VariantForm, UpdateStockForm, CreateVariantForm, EditVariantForm, RegistrationForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, FormView, CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.db.models import Min
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from .mixins import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class InventoryDashboard(TemplateView):
	template_name = "inventory-management/dashboard.html"

class InventoryProductListView (ListView):
	# Created by Adam Ahmed 23/11/2024
	''' View for IMS System that displays all the products currently available and allows new product creation '''
	model = Product
	template_name = "inventory-management/product_list.html"
	context_object_name = "products"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		low_stock_threshold = 5 
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
	fields = ['name', 'description']

	def get_success_url(self):
		return reverse_lazy('IMS - Product List')

class InventoryProductEditView(UpdateView):
	# Created by Adam Ahmed 23/11/2024
	''' View that allows already created products to be edited '''
	model = Product
	template_name = "inventory-management/product_edit.html"
	context_object_name = "product"
	fields = ['name', 'description']

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

		# Multiple file uploads
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
		return reverse_lazy('IMS - Product Detail', kwargs={'pk': self.object.productID.pk})



class CatalogueViewClass(ListView):
	
	context_object_name = "ProductList"
	template_name = "product_catalogue.html"
	
	
	filterValue = ""
	orderValue = ""
	SearchValue = ""	
	def get(self, request, *args, **kwargs): ###Get filter values for context data to use
		### Get Filter Value
		
		self.filterValue = request.GET.get('selected_filters',"") 
		self.filterValue = self.filterValue.split(",") if self.filterValue else [] ## Split all values into a list for it to be recognised
		
		###Get Order Value

		self.orderValue = request.GET.get("order","name") ### Default value will be name
		
		### Get Search value
		self.searchValue = request.GET.get("search","")
		
	
		##Return filter, may have to be an array since we have multiple filter values?
		return super().get(request, *args, **kwargs)
	

	def get_queryset(self):
		queryset = Product.objects.all()
		###Input filter values

		if (self.filterValue !=[]):
			queryset = queryset.filter(categories__categories__in = self.filterValue)

		##Input Order values 
		queryset = queryset.order_by(self.orderValue)
		##Search value
		if self.searchValue != '': ### Only filter for search value if a search value exists
			queryset = queryset.filter(name__icontains=self.searchValue)
		return queryset
	
	
	def get_context_data(self, **kwargs): ###use filter values 
		###List Size issue
		listSize = len(self.get_queryset())
		style = ""
		if(listSize == 2) or (listSize == 1):
			style="product-size" + str(listSize)
			print(style)
		else:
			style=""
		###Return context
		context = super().get_context_data(**kwargs)
		context['productClass'] = style
		return context
	


	

class CreateReviewClass(LoginRequiredMixin, CreateView):
	model = Review
	form_class = ReviewForm
	template_name = "CreateReviewPage.html"
	success_url = reverse_lazy('Catalogue')



	def form_valid(self, form):
		
		form.instance.rating = self.request.POST.get('rating-hidden')

		user = self.request.user
		form.instance.userID = user

		productID = self.request.POST.get('prod-id')
		product = get_object_or_404(Product,id=productID)
		form.instance.productID = product


		messages.success(self.request, "Your review has been added successfully!")
		return super().form_valid(form)
	

class WishlistView(ListView):
	
	
	context_object_name = "wishlist_Table"
	##template_name = "product_catalogue.html"

	
	


class CustomLoginView(LoginView):
	template_name = 'login/login.html'  
	authentication_form = CustomLoginForm
	redirect_authenticated_user = True 

	def get_success_url(self):
		if self.request.user.groups.filter(name='admin').exists():
			return 'inventory-managment/product'
		elif self.request.user.groups.filter(name='customer').exists():
			return 'home'
		return super().get_success_url()
	
class RegistrationView(FormView):
	template_name = 'login/register.html'  
	form_class = RegistrationForm
	success_url = reverse_lazy('login') 

	def form_valid(self, form):
		# Save the user
		user = form.save()

		group = Group.objects.get(name='Customer')
		user.groups.add(group)

		Basket.objects.create(userID=user)

		return super().form_valid(form)
	
class HomeView(TemplateView):
	# Created by Adam Ahmed 
	template_name = "home-page.html"
	
def ContactPageView(request, *args, **kwargs):
	submitted = False
	if request.method == 'POST':
		contactform = ContactEnquiryForm(request.POST)
		if contactform.is_valid():
			contact = contactform.save()
			subject = f"New Contact Request from {contact.username}"
			message = (
				f"You have received a new contact enquiry.\n\n"
				f"Name: {contact.username}\n"
				f"Email: {contact.email}\n\n"
				f"Description:\n{contact.description}"
			)
			from_email = 'noreply.hatsforcats@gmail.com'
			recipient_list = ['noreply.hatsforcats@gmail.com']

			send_mail(
				subject,
				message,
				from_email,
				recipient_list,
				fail_silently=False,
			)
			return HttpResponseRedirect('contact-page?submit=True')
	else:
		contactform = ContactEnquiryForm()
		if 'submit' in request.GET:
			submitted = True

	context = {"ContactForm": contactform, 'submitted': submitted}
	return render(request, 'general-Pages/Contact-Page.html', context)



##def ContactPageViewClass(FormView):
	###TBC (Incomplete)

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
class VariantDisplayView(View):
#written by Sakina Khaki
	
	#get product by id
	def getObj(self, pk):
		return Product.objects.get(id = pk)

	'''
		use productid to get product; get name, description
		get every variant of product 
		map sizes -> colour (vice versa)
	'''
	def pageData(self, product):
		#getting every product varient from db
		allitems = ProductVariant.objects.all()
		allitems = allitems.filter(productID = product)

		name = product.name
		desc = product.description

		#
		sizes = ["S", "M", "L", "XL"] #all sizes
		available_sizes = set(sizes)

		colours = {v.colour for v in allitems} #all colours
		available_colours = set(colours)

		#map sizes and colours
		sizes_map = {}
		for i in allitems:
			sizes_map.setdefault(i.colour, []).append(i.size)

		print(sizes_map)

		colours_map = {}
		for i in allitems:
			colours_map.setdefault(i.size, []).append(i.colour)

		#to pass to html
		return {
			'name': name, 'desc': desc, 
			'variants' : allitems,
			'colours': colours, 
			'sizes': sizes, 
			'sizes_map': sizes_map, 'colours_map' : colours_map,
			'quantity': 1 #default
		}


	'''
		post request to add to basket
		filter available size/colour (create sets)
		get quantity wanted (in the post request)
		validate item is available
			if unavailable, return page reload
	'''
	def post(self, request, pk):
		product = self.getObj(pk)
		allitems = ProductVariant.objects.filter(productID=product)

		#get from post request
		quantity = int(request.POST.get("quantity"))
		colour = request.POST.get("colour")
		size = request.POST.get("size")

		#puts all available sizes in set
		available_sizes = {i.size for i in allitems if i.colour == colour}


		#all available colours into set
		available_colours = {i.colour for i in allitems if i.size == size}


		#final validation check - checks if that size is available in that colour 
		if (colour not in available_colours) or (size not in available_sizes):
			print(size)
			print(colour)
			print("no colour and or size")
			return render(request, "productdetailpage.html", self.pageData(product))
		else:
			print("yay") 

		#sorts variantid out 
		
		variantid = ProductVariant.objects.get(productID=product, colour=colour, size=size).id
		variant = ProductVariant.objects.get(productID=product, id=variantid)

		#get basketid
		basket = Basket.objects.get(userID=request.user)
		
		#basketid for testing
		#basket = Basket.objects.get(userID=1)
		#basketid = basket.id


		'''
			add to basket 
			check if existing or new item
			return redirect to basket
		'''

		#check if user has ordered item before already
		basketitem = BasketItem.objects.filter(basketID=basket, variantID=variant).first()


		if basketitem: 
		#inc quantity of thing in basket
			#print("added", quantity, "to EXISTING")
			basketitem.quantity += quantity

		else: 
		#create new basketitem entry
			#print("added", quantity, "to NEW")
			BasketItem.objects.create(basketID=basket, variantID=variant, quantity=quantity)
			
			
		return redirect('basket')




	#display product variant page 
	def get(self, request, pk):
		prod = self.getObj(pk)
		itemNames = self.pageData(prod)
		return render(request, "productdetailpage.html", itemNames)


class BasketView(View):

	#get basket id
	def getBasket(self, user):
		return Basket.objects.get(userID=user).id

	#veiw basket; calc total price, num items 
	def get(self, request):
		basket = self.getBasket(request.user)
		allitems = BasketItem.objects.filter(basketID=basket)

		total = 0
		numitems = 0
		for i in allitems:
			variant = ProductVariant.objects.get(id=i.variantID.id)
			total += (variant.price * i.quantity)
			numitems += (1 * i.quantity)
		#print(total)

		itemNames = {
			'basket' : allitems,
			'total' : total,
			'numitems' : numitems
		}


		#viewing the basket
		return render(request, "basket.html", itemNames)

	#adding/removing items from basket
	def post(self, request):
		#get basketid
		basketid = Basket.objects.get(userID=request.user).id

		#for testing
		#basketid = Basket.objects.get(userID=1)

		variantid = request.POST.get("variantid")
		variant = ProductVariant.objects.get(id=variantid)

		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()


		'''
			check if item is in basket 
			add: quantity += 1
			rem_all or quantity = 1: delete
			else quantity -= 1
		'''

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


		return redirect("basket")
		


@permission_required('ecommerceapp.Customer')
#remove from basket 
def basketRem(request):
#written by Sakina Khaki
	if request.method == "POST":
		#print("beep")
		#get basketid
		basketid = Basket.objects.get(userID=request.user).id

		#for testing
		#basketid = Basket.objects.get(userID=1)

		variantid = request.POST.get("variantid")
		variant = ProductVariant.objects.get(id=variantid)

		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()


		'''
			check if item is in basket 
			add: quantity += 1
			rem_all or quantity = 1: delete
			else quantity -= 1
		'''

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
	basketid = Basket.objects.get(userID=request.user).id

	#for testing if right basket loaded
	#admin acc id = 1
	assert basketid == 1, "basket is wrong! id="+str(basketid)

	allitems = BasketItem.objects.filter(basketID=basketid)

	total = 0
	numitems = 0
	for i in allitems:
		variant = ProductVariant.objects.get(id=i.variantID.id)
		total += (variant.price * i.quantity)
		numitems += (1 * i.quantity)
	#print(total)

	itemNames = {
		'basket' : allitems,
		'total' : total,
		'numitems' : numitems
	}


	#viewing the basket
	return render(request, "basket.html", itemNames)


# @permission_required('ecommerceapp.Customer')
# #checkout
# def checkout(request):
#   return render(request, "admin/temp_basket/tempCheckout.html")

class CustomPasswordResetView(PasswordResetView):
	form_class = CustomPasswordResetForm
	
class CheckoutView(GroupRequiredMixin, FormView):
	template_name = "checkout.html"
	form_class = CheckoutForm
	group_required = 'Customer'

	def get_basket(self):
		'''Get the current user's basket.'''
		return get_object_or_404(Basket, userID=self.request.user)

	def get_initial(self):
		'''Prefill the form with the user's address if it exists.'''
		try:
			user_address = UserAddress.objects.get(userID=self.request.user)
			initial_data = {
				'houseNumber': user_address.houseNumber,
				'apartmentNumber': user_address.apartmentNumber,
				'street': user_address.street,
				'postcode': user_address.postcode,
				'city': user_address.city,
			}
			return initial_data
		except UserAddress.DoesNotExist:
			return super().get_initial()

	def get_context_data(self, **kwargs):
		'''Add basket items and total cost to context.'''
		context = super().get_context_data(**kwargs)
		basket = self.get_basket()
		basket_items = basket.basketitem.all()
		total_cost = sum(item.variantID.price * item.quantity for item in basket_items)
		context['basket_items'] = basket_items
		context['total_cost'] = total_cost
		return context

	def form_valid(self, form):
		'''Handle the checkout process.'''
		# Save or update the user's address
		user_address, created = UserAddress.objects.update_or_create(
			userID=self.request.user,
			defaults={
				'houseNumber': form.cleaned_data['houseNumber'],
				'apartmentNumber': form.cleaned_data.get('apartmentNumber', 0),
				'street': form.cleaned_data['street'],
				'postcode': form.cleaned_data['postcode'],
				'city': form.cleaned_data['city'],
			}
		)

		# Process basket and create order
		basket = self.get_basket()
		basket_items = basket.basketitem.all()

		# Createnew order
		order = Order.objects.create(
			userID=self.request.user,
			totalAmount=sum(item.variantID.price * item.quantity for item in basket_items),
			status='pending',
			paymentMethod='credit',
			trackingInfo="Processing",
		)

		# Convert basket items to order items
		for basket_item in basket_items:
			OrderItem.objects.create(
				orderID=order,
				variantID=basket_item.variantID,
				quantity=basket_item.quantity,
				priceAtPurchase=basket_item.variantID.price,
			)

		# Clear the basket
		basket_items.delete()

		return redirect(reverse('order-summary', kwargs={'order_id': order.id}))

class OrderSummaryView(GroupRequiredMixin, TemplateView):
	template_name = "purchaseconfirmation.html"
	group_required = 'Customer'

	def get_context_data(self, **kwargs):
		"""Add order details to context."""
		context = super().get_context_data(**kwargs)
		order = get_object_or_404(Order, id=self.kwargs['order_id'], userID=self.request.user)
		context['order'] = order
		context['order_items'] = order.orderitem.all()
		return context
	
