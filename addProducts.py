import os
import django
import random
from ecommerceapp.models import Product,ProductCategories,ProductVariant  # Adjust to your app name

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Sample data
product_names = ["Product#1","Product#2"]

product_descriptions = ["Product#1 description", "Product#2 description"]
categories = ["Seasonal Hats", "Occasional Hats", "Cozy & Comfortable Hats", "Summer Hats", "Themed Hats"]
sizes = ["S","M","L","XL"]
colours = ["Red", "Blue", "Green", "Grey", "Black","White"]
prices = [10.99, 15.99, 20.00, 25.99, 7.99, 4.99]


variantsPerProduct = 3
# Function to create products
def create_products():
    for product_no in range(0,len(product_names)):
        product = Product.objects.create(
            name= product_names[product_no],
            product_description = random.choice(product_descriptions)
        )

        for variant_no in range(0,variantsPerProduct):
            ProductVariant.objects.create(
                product= product,
                size = sizes[variant_no],
                color = colours[variant_no],
                price = prices[variant_no],
                stocklevel =  random.randrange(1,31)
            )


            
        

# Run script
if __name__ == "__main__":
    create_products()  # Create 50 products