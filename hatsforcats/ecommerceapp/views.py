from django.shortcuts import render

# Create your views here.

from .models import Basket, BasketItem, Product


#display products
def productDisplay(request):
	allitems = Product.objects.all()
	itemNames = {
		'products' : allitems
	}

	#viewing
	return render(request, "admin/temp_basket/tempProducts.html", itemNames)

#add to basket
def basketAdd(request, variantid, quantity=1, amendQuantity=False):
	#get basketid
	basketid = Basket.objects.get(userID=request.user).id
	
	#check if user has ordered item before already
	basketitem = BasketItem.objects.filter(BasketID=basketid, variantID=variantid).first()

	if basketitem: 
		#inc quantity
		if amendQuantity:
			basketitem.quantity = quantity
		else:
			basketitem.quantity += 1
		basketitem.save()
	else: 
		#create new basketitem entry
		BasketItem.objects.create(BasketID=basketid, variantID=variantid, quantity=quantity)


#remove from basket 
def basketRem(request, variantid):
	#get basketid
	basketid = Basket.objects.get(userID=request.user).id

	basketitem = BasketItem.objects.filter(BasketID=basketid, variantID=variantid).first()

	if basketitem:
		basketitem.delete()


#veiw basket
def viewBasket(request):
	#get basketid
	basketid = Basket.objects.get(userID=request.user).id

	allitems = BasketItem.objects.filter(BasketID=basketid)
	itemNames = {
		'basket' : allitems
	}

	#viewing the absket
	return render(request, "admin/temp_basket/tempProducts.html", itemNames)

