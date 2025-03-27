from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategories)
admin.site.register(ProductVariant)
admin.site.register(ImagePath)
admin.site.register(Review)
admin.site.register(UserAddress)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BasketItem)
admin.site.register(ContactTable)
admin.site.register(Wishlists)
admin.site.register(WishlistItem)