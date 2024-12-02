from django.shortcuts import render

# Create your views here.

from .models import Basket, BasketItem, ProductVariant
from django.contrib.auth.decorators import permission_required


#display products
def productDisplay(request):
	allitems = ProductVariant.objects.all()
	itemNames = {
		'products' : allitems
	}

	#viewing
	return render(request, "admin/temp_basket/tempProducts.html", itemNames)


@permission_required('ecommerceapp.Customer') 
#add to basket
def basketAdd(request):
	#gets everyhting from post data
	if request.method == "POST":
		#print("borp")
		variantid = request.POST.get("variantid")  
		quantity = int(request.POST.get("quantity", 1))  
		amendQuantity = request.POST.get("amendQuantity", "false").lower() == "true"

		#get basketid
		#basketid = Basket.objects.get(userID=request.user).id
		
		#for testing
		basketid = Basket.objects.get(userID=1)

		#get varientid
		variant = ProductVariant.objects.get(id=variantid)

		#check if user has ordered item before already
		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()

		if basketitem: 
			#inc quantity
			if amendQuantity:
				basketitem.quantity = quantity
			else:
				basketitem.quantity += 1
			basketitem.save()
		else: 
			#create new basketitem entry
			BasketItem.objects.create(basketID=basketid, variantID=variant, quantity=quantity)

	return(productDisplay(request))
		#return render(request, "admin/temp_basket/tempProducts.html")



@permission_required('ecommerceapp.Customer')
#remove from basket 
def basketRem(request):
	if request.method == "POST":
		#print("beep")
		#get basketid
		#basketid = Basket.objects.get(userID=request.user).id

		#for testing
		basketid = Basket.objects.get(userID=1)

		variantid = request.POST.get("variantid")
		variant = ProductVariant.objects.get(id=variantid)

		basketitem = BasketItem.objects.filter(basketID=basketid, variantID=variant).first()

		if basketitem:
			print("removed")
			basketitem.delete()
		else:
			print("not removed")

	return(viewBasket(request))


@permission_required('ecommerceapp.Customer')
#veiw basket
def viewBasket(request):
	#print("beep")
	#get basketid
	#basketid = Basket.objects.get(userID=request.user).id

	#for testing
	basketid = Basket.objects.get(userID=1)

	allitems = BasketItem.objects.filter(basketID=basketid)
	itemNames = {
		'basket' : allitems
	}

	#viewing the absket
	return render(request, "admin/temp_basket/tempBasket.html", itemNames)

