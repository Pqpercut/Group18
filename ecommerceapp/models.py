from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings



# Create your models here.

class Product (models.Model):
# Model created by: Adam 
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self): 
        return f"{self.name}"

class ProductCategories (models.Model):
# Model created by: Adam 
    CATEGORYTYPES = {
        ('seasonal', 'Seasonal Hats'),
        ('occasional', 'Occasional Hats'),
        ('cozy', 'Cozy & Comfortable Hats'),
        ('summer', 'Summer Hats'),
        ('themed', 'Themed Hats')
    }
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'categories')
    categories = models.CharField(max_length=50, choices=CATEGORYTYPES, default='hats')

class ProductVariant (models.Model):
# Model created by: Adam 
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'productvariant')
    size = models.CharField(max_length=50) 
    colour = models.CharField(max_length=50) # Each product variant can only be a single colour and size. i.e. Blue S, Blue M, Blue L, Red S, Red M, Red L
    price = models.FloatField()
    stocklevel = models.PositiveIntegerField()
   
class ImagePath (models.Model):
# Model created by: Adam 
    productVariantID = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name = 'imagepath')    
    imagepath = models.ImageField(upload_to='uploads/product-images/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)


class Review (models.Model):
# Model created by: Adam 
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'review')    
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'review') 
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    title = models.CharField(max_length=50) 
    description = models.TextField()
    reviewDate = models.DateTimeField(auto_now_add=True)



class UserAddress(models.Model):
#Model made by Qasim Farooq
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'useraddress')
    houseNumber = models.IntegerField()
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length= 20)
    city = models.CharField(max_length=10)
    apartmentNumber= models.IntegerField(blank=True, null=True)

class Basket(models.Model):
#Model made by Qasim Farooq
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'basket')

#written by Sakina Khaki
class Order(models.Model):
    #choices for status
    STATUS = {
        ('pending', 'Order Pending'), 
        ('route', 'On Route'), 
        ('delivered', 'Delivered'), 
        ('refunded', 'Refunded')
    }

    PAYMENT = {
        ('credit', 'Credit card'),
        ('debit', 'Debit card'),
        ('paypal', 'Paypal')
    }

    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    orderDate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default="pending")
    totalAmount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])
    paymentMethod = models.CharField(max_length=50, choices=PAYMENT, default="credit")
    trackingInfo = models.CharField(max_length=200)

#written by Sakina Khaki
class OrderItem(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    variantID = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.PositiveIntegerField()
    priceAtPurchase = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])

#written by Sakina Khaki
class BasketItem(models.Model):
    basketID = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basketitem')
    variantID = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='basketitem')
    quantity = models.PositiveIntegerField()

##Written by Qasim Farooq
class ContactTable(models.Model):
    username = models.CharField(max_length=50)
    description = models.TextField()
    email = models.EmailField()



class Wishlists (models.Model):
# Model created by: Adam    
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'wishList')
    name = models.CharField(max_length=50, default="Wishlist")
    
class WishlistItem(models.Model):
    wishlistID = models.ForeignKey(Wishlists, on_delete=models.CASCADE, related_name='wishListID')
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'wishlist') 
    
    
    
