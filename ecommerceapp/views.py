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
	fields = ['name', 'description', 'availability']

	def get_success_url(self):
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

def catalogueView(request, *args, **kwargs):
	###Written by Qasim Farooq 29/11/24

	##Get filter in URL
	FiltergetValue = request.GET.get('selected_filters',"")
	print("BEFORE:" + str(FiltergetValue)) 
	filterList = []
	filterValue = "" 
	if (FiltergetValue !=""):
		filterList = FiltergetValue.split(",")
		print("FILTER EXISTS : " + str(FiltergetValue))
		for x in filterList:
			##Add all filter values to list and seperate with comma
			filterValue = filterValue + x + ","
			print(x)

	print("AFTER:" , filterValue)
	##Assign the correct Order by Value
	orderValue = request.GET.get("order","default-value")
	if orderValue == 'price':
		orderValue = 'productvariant__price'
	else:
		orderValue = 'name'

	##Get a query of all products
	productList = Product.objects.all()

    #If there is a filter then filter the query to only those products
	if (FiltergetValue !=""):
		print("Filter complete")
		productList = productList.filter(categories__categories__in = filterList)

	##Order the query
	##Aggregate the values to be able to prevent multiple variants showing on the list
	productList = productList.annotate(min_val=Min(orderValue))
	productList = productList.annotate(img_path=Min('productvariant__imagepath__imagepath'))
	
	productList = productList.order_by('min_val')

	searchValue = request.GET.get("search","")

	if searchValue != '':
		productList = productList.filter(name__icontains=searchValue)
		print("searching")
	##Return the query

	fullProductList = Product.objects.all()

	listSize = len(productList)
	style = ""
	if(listSize == 2):
		style="product-size2"
	elif(listSize == 1):
		style="product-size1"
	else:
		style=""

	context = {"ProductList" : productList, "FullProductList" : fullProductList,"searchValue": searchValue, "productClass": style, "listsize": listSize}

    
	return render(request, "product_catalogue.html", context)

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
def variantDisplay(request, pk):
#written by Sakina Khaki
	#print("blorp")

	#productid = request.POST.get("productid")
	productid = pk #testing purpose

	product = Product.objects.get(id = productid)
	name = product.name
	desc = product.description

	allitems = ProductVariant.objects.all()
	allitems = allitems.filter(productID = productid)

	sizes = ["S", "M", "L", "XL"] #all sizes
	available_sizes = set(sizes)

	colours = {v.colour for v in allitems} #all colours
	available_colours = set(colours)

	#dictionary of all sizes and colours
	sizes_map = {}
	for i in allitems:
		sizes_map.setdefault(i.colour, []).append(i.size)

	print(sizes_map)
	#print(sizes_map)

	colours_map = {}
	for i in allitems:
		colours_map.setdefault(i.size, []).append(i.colour)


	if request.method == "POST":
		quantity = int(request.POST.get("quantity"))
		colour = request.POST.get("colour")
		size = request.POST.get("size")

		#puts all available sizes in set
		available_sizes.clear()
		for i in allitems: 
			if i.colour == colour:
				available_sizes.add(i.size)


		#all available colours into set
		available_colours.clear()
		for i in allitems:
			if i.size == size:
				available_colours.add(i.colour)


		#final validation check - checks if that size is available in that colour 
		if (colour not in available_colours) or (size not in available_sizes):
			print(size)
			print(colour)
			print("no colour and or size")
			return render(request, "productdetailpage.html", {
				'name': name, 'desc': desc, 
				'variants' : allitems,
				'colours': colours, 
				'sizes': sizes, 
				'sizes_map': sizes_map, 'colours_map' : colours_map,
				'quantity': quantity
			})
		else:
			print("yay")


		#sorts variantid out 
		
		variantid = ProductVariant.objects.get(productID=product, colour=colour, size=size).id
		variant = ProductVariant.objects.get(productID=product, id=variantid)

		#get basketid
		#basketid = Basket.objects.get(userID=request.user).id
		
		#basketid for testing
		basket = Basket.objects.get(userID=1)
		basketid = basket.id

		#check if user has ordered item before already
		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()


		if basketitem: 
		#inc quantity of thing in basket
			print("added", quantity, "to EXISTING")
			basketitem.quantity += quantity
		else: 
		#create new basketitem entry
			print("added", quantity, "to NEW")
			BasketItem.objects.create(basketID=basket, variantID=variant, quantity=quantity)

		return redirect('basket')
	else:
		quantity = 1


	itemNames = {
		'name': name, 'desc': desc, 
		'variants' : allitems,
		'colours': colours, 
		'sizes': sizes, 
		'sizes_map': sizes_map, 'colours_map' : colours_map,
		'quantity': quantity,
		'product': product,
	}


	#viewing
	return render(request, "productdetailpage.html", itemNames)




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


	#viewing the basket
	return render(request, "basket.html", itemNames)


# @permission_required('ecommerceapp.Customer')
# #checkout
# def checkout(request):
# 	return render(request, "admin/temp_basket/tempCheckout.html")

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
	
