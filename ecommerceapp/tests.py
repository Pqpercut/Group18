from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerceapp.models import Basket, Product, BasketItem, ProductVariant, ImagePath
from django.core.files.uploadedfile import SimpleUploadedFile


class variantDisplayTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Product", description="test product 1")

        self.product1 = ProductVariant.objects.create(productID=self.product, size="M", colour="red", price=12, stocklevel=22)
        self.product2 = ProductVariant.objects.create(productID=self.product, size="XL", colour="pink", price=12, stocklevel=15)
 
    #correct product acquired from productid
    def test_productid(self):
        prod = Product.objects.get(id=self.product1.id)
        self.assertEqual(prod.name, "Product", "wrong product!")

    #all variants of product are correct
    def test_variants_of_products(self):
        variants = ProductVariant.objects.filter(productID=self.product.id)
        self.assertEqual(variants.count(), 2, "wrong num variants!")

    #colours map accurate to whats in stock 
    def test_colour_map(self):
        #expected 
        expected = {
            "red" : ["M"],
            "pink" : ["XL"]
        }

        #get variants
        variants = ProductVariant.objects.filter(productID=self.product.id)

        #actual mapping 
        actual = {}
        for i in variants:
            actual.setdefault(i.colour, []).append(i.size)

        self.assertEqual(expected, actual, "colour mapping is wrong!")

    #size map accuracy
    def test_size_map(self):
        #expected 
        expected = {
            "M" : ["red"],
            "XL" : ["pink"]
        }

        #get variants
        variants = ProductVariant.objects.filter(productID=self.product.id)

        #actual mapping 
        actual = {}
        for i in variants:
            actual.setdefault(i.size, []).append(i.colour)

        self.assertEqual(expected, actual, "size mapping is wrong!")


    #picking colour updates sizes
    def test_colour_updates_size(self):
        col = "red" 
        sizes = []

        variants = ProductVariant.objects.filter(productID=self.product.id, colour=col)

        for i in variants: 
            sizes.append(i.size)

        self.assertEqual(sizes, ["M"], "returned "+str(sizes))


    #picking size updates colour
    def test_size_updates_colour(self):
        size = "XL" 
        cols = []

        variants = ProductVariant.objects.filter(productID=self.product.id, size=size)

        for i in variants: 
            cols.append(i.colour)

        self.assertEqual(cols, ["pink"], "returned "+str(cols)) 


    #nonexistent item is not recognised
    def test_nonexistent_item(self):
        size = "S"
        colour = "green"

        variant = ProductVariant.objects.filter(productID=self.product.id, colour=colour, size=size).first()
    
        self.assertIsNone(variant, "item does not exist")

    #test if correct img to name 
    



class BasketTestCase(TestCase):
    def setUp(self):
        #create test user
        self.user = User.objects.create_user(username="testuser", password="password")

        #create test products
        #self.product1 = Product.objects.create(name="Product 1", price=10.00, stock=10)
        #self.product2 = Product.objects.create(name="Product 2", price=20.00, stock=5)

        self.product1 = Product.objects.create(name="Product 1")
        self.product2 = Product.objects.create(name="Product 2")

        #create basket
        self.basket = Basket.objects.create(userID=self.user).id 

    def test_add_product(self):
        #add product to the basket
        self.basket.add_product(self.product1, 2)
        item = BasketItem.objects.get(basket=self.basket, product=self.product1)
        self.assertEqual(item.quantity, 2)

    def test_add_product_exceeding_stock(self):
        #make quantity more than stock
        with self.assertRaises(ValueError):
            self.basket.add_product(self.product1, 20)  #stock < 20

    def test_add_product_negative_quantity(self):
        #adding w negative quantity 
        with self.assertRaises(ValueError):
            self.basket.add_product(self.product1, -1)

    def test_remove_product(self):
        #remove product from basket
        self.basket.add_product(self.product1, 3)
        self.basket.remove_product(self.product1)
        self.assertFalse(BasketItem.objects.filter(basket=self.basket, product=self.product1).exists())

    def test_remove_nonexistent_product(self):
        #removing non existent product from absket 
        with self.assertRaises(BasketItem.DoesNotExist):
            self.basket.remove_product(self.product2)  

    #nonexistent item not added to basket, notifies user

    def test_update_quantity(self):
        #update quantity of existing product 
        self.basket.add_product(self.product1, 2)
        self.basket.update_quantity(self.product1, 5)
        item = BasketItem.objects.get(basket=self.basket, product=self.product1)
        self.assertEqual(item.quantity, 5)

    def test_update_quantity_to_zero(self):
        #update quantity to 0: will remove from basket 
        self.basket.add_product(self.product1, 2)
        self.basket.update_quantity(self.product1, 0)
        self.assertFalse(BasketItem.objects.filter(basket=self.basket, product=self.product1).exists())

    def test_update_quantity_negative(self):
        #update quantity to negative val 
        self.basket.add_product(self.product1, 2)
        with self.assertRaises(ValueError):
            self.basket.update_quantity(self.product1, -3)

    def test_clear_basket(self):
        #clear basket 
        self.basket.add_product(self.product1, 2)
        self.basket.add_product(self.product2, 3)
        self.basket.clear()
        self.assertEqual(BasketItem.objects.filter(basket=self.basket).count(), 0)

    def test_get_total_price(self):
        #total price 
        self.basket.add_product(self.product1, 2)  
        self.basket.add_product(self.product2, 1)  
        self.assertEqual(self.basket.get_total_price(), 40.00)

    def test_get_total_price_empty_basket(self):
        #make sure total = 0 when empty basket 
        self.assertEqual(self.basket.get_total_price(), 0.00)

class ProductPageTest(TestCase):

    def setUp(self):
        # Create a Product instance
        self.product1 = Product.objects.create(name="aog Top hat", description="A nice hat")
        self.product2 = Product.objects.create(name="dog Beanie", description="Stylish blue beanie")

        # Create ProductVariants for each product
        self.variant1 = ProductVariant.objects.create(
            productID=self.product1, 
            size="M", 
            colour="Blue", 
            price=20.99, 
            stocklevel=100
        )
        self.variant2 = ProductVariant.objects.create(
            productID=self.product2, 
            size="L", 
            colour="Black", 
            price=40.99, 
            stocklevel=50
        )

        
        
        # Create an ImagePath for the product variants
        self.image1 = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.imagepath1 = ImagePath.objects.create(productVariantID=self.variant1, imagepath=self.image1)
        self.image2 = SimpleUploadedFile("test_image2.jpg", b"file_content", content_type="image/jpeg")
        self.imagepath2 = ImagePath.objects.create(productVariantID=self.variant2, imagepath=self.image2)

        # Define the URL to test the product page (replace with the correct URL)
        self.url = reverse('Catalogue')  # Replace with the actual view name for product list
    
    def test_view_all_products(self):
        # Test that the product page loads correctly and displays products
        
        response = self.client.get(reverse('Catalogue'))
        self.assertEqual(response.status_code, 200)
        
        # Check that both products are in the response content
        self.assertContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertContains(response, f'<p class="product-name">{self.product2.name}</p>')
        

   

    def test_filter(self):
        # Test that the product page loads correctly and displays products
        
        
        response = self.client.get("/catalogue?selected_filters=seasonal" )
        self.assertEqual(response.status_code, 200)
        # Check that both products are in the response content
        self.assertNotContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertNotContains(response, f'<p class="product-name">{self.product2.name}</p>')        
    
    



    def test_product_images_display(self):
        # Test that the images associated with the variants are correctly displayed
        response = self.client.get(self.url)
        
        # Check if images are included for the variants
        self.assertContains(response, self.imagepath1.imagepath.url)  # URL of the image
        self.assertContains(response, self.imagepath2.imagepath.url)  # URL of the image
    




    
    def test_product_variant_price_display(self):
        # Ensure that the price for the product variant is displayed correctly
        response = self.client.get(self.url)
        
        # Check the price of both product variants
        self.assertContains(response, f"£{self.variant1.price}")
        self.assertContains(response, f"£{self.variant2.price}")

    def test_orderName(self):

        response = self.client.get("/catalogue?order=name" )
        self.assertEqual(response.status_code, 200)
        # Check that both products are in the response content
        content = response.content.decode('utf-8') 


        pos1 = content.find(f'<p class="product-name">{self.product1.name}</p>')
        pos2 = content.find(f'<p class="product-name">{self.product2.name}</p>')


        
        self.assertTrue(pos1 < pos2, "Products are not in the correct order.")

    def test_orderPrice(self):

        response = self.client.get("/catalogue?order=productvariant__price" )
        self.assertEqual(response.status_code, 200)
        # Check that both products are in the response content
        content = response.content.decode('utf-8') 


        pos1 = content.find(f"£{self.variant1.price}")
        pos2 = content.find(f"£{self.variant2.price}")


        
        self.assertTrue(pos1 < pos2, "Products are not in the correct order.")



