from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerceapp.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from PIL import Image
import io
## INSTALLL PIP BEFORE RUNNING THESE
def create_test_image(name="test_image.jpg", format="JPEG"):
    image = Image.new("RGB", (100, 100), color="blue")
    img_io = io.BytesIO()
    image.save(img_io, format)
    img_io.seek(0)
    return SimpleUploadedFile(name, img_io.read(), content_type=f"image/{format.lower()}")


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
        self.client.login(username='testuser', password='password')

        #create test products
        self.product1 = Product.objects.create(name="Product 1", description="product 1")
        self.product2 = Product.objects.create(name="Product 2", description="product 2")

        self.variant1 = ProductVariant.objects.create(
            productID=self.product1,
            size='M',
            colour='Red',
            price=15.00,
            stocklevel=10
        )
        self.variant2 = ProductVariant.objects.create(
            productID=self.product1,
            size='L',
            colour='Blue',
            price=17.00,
            stocklevel=5
        )

        #create basket
        self.basket = Basket.objects.create(userID=self.user) 



    def test_add_product(self):
        #add product to the basket
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)

        self.assertIsNotNone(basketitem)  #check item exist in basket
        self.assertEqual(basketitem.quantity, 1)  #make sure quantity = 1


    def test_add_product_exceeding_stock(self):
        #make quantity more than stock
        with self.assertRaises(ValueError):
            basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=50)  #stock < 50


    def test_add_product_negative_quantity(self):
        #adding w negative quantity 
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=-2)
        with self.assertRaises(IntegrityError):
            #basketitem.full_clean()  
            basketitem.save()

    #remove product from basket
    def test_remove_product(self):
        #add product to basket
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)
        self.assertIsNotNone(basketitem)  #check item exist in basket

        #remove it 
        basketitem.delete()

        self.assertFalse(BasketItem.objects.filter(basketID=self.basket, variantID=self.variant1).exists())


    def test_remove_nonexistent_product(self):
        #removing non existent product from absket 
        try:
            self.basket.delete(self.product2)  
        except BasketItem.DoesNotExist:
            self.fail("BasketItem.DoesNotExist raised when removing a nonexistent item")

        self.assertEqual(basketitems.count(), 0)  #noothing should be in basket
 

    
    def test_update_quantity(self):
        #update quantity of existing product 
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)
        
        basketitem.quantity += 4
        basketitem.save()
        
        item = BasketItem.objects.get(basketID=self.basket)
        self.assertEqual(item.quantity, 5)

    
    def test_update_quantity_to_zero(self):
        #update quantity to 0: will remove from basket 
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)
        
        basketitem.quantity -= 0
        basketitem.save()
        
        item = BasketItem.objects.get(basketID=self.basket)
        print(item.quantity)
        self.assertEqual(BasketItem.objects.filter(basketID=self.basket).count(), 0) 


    
    def test_update_quantity_negative(self):
        #update quantity to negative val 
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)
        with self.assertRaises(ValidationError):
            basketitem.quantity -= 0
            basketitem.full_clean()
            basketitem.save()

    
    def test_get_total_price(self):
        #total price 
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant1, quantity=1)  
        basketitem = BasketItem.objects.create(basketID=self.basket, variantID=self.variant2, quantity=1)  
        self.assertEqual(self.basket.get_total_price(), 40.00)


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

        
        
        ### Create an ImagePath for the product variants
        self.image1 = create_test_image("test_image.jpg")
        self.imagepath1 = ImagePath.objects.create(productVariantID=self.variant1, imagepath=self.image1)

        self.image2 = create_test_image("test_image2.jpg")
        self.imagepath2 = ImagePath.objects.create(productVariantID=self.variant2, imagepath=self.image2)

         ##Define the URL to test the product page (replace with the correct URL)
        self.url = reverse('Catalogue')  # Replace with the actual view name for product list
    
    def test_view_all_products(self):
        
        response = self.client.get(reverse('Catalogue'))
        self.assertEqual(response.status_code, 200)
        
        #Check that both products are in the response content
        self.assertContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertContains(response, f'<p class="product-name">{self.product2.name}</p>')
        

   

    def test_filter(self):
        
        
        
        response = self.client.get("/catalogue?selected_filters=seasonal" )
        self.assertEqual(response.status_code, 200)
        ###Check that both products are in the response content'
        self.assertNotContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertNotContains(response, f'<p class="product-name">{self.product2.name}</p>')        
    
    



    def test_product_images_display(self):
      
        response = self.client.get(self.url)
        
        ### Check if images are included for the variants
        self.assertContains(response, self.imagepath1.imagepath.url)  # URL of the image
        self.assertContains(response, self.imagepath2.imagepath.url)  # URL of the image
    




    
    def test_product_variant_price_display(self):
        
        response = self.client.get(self.url)
        
        ## Check the price of both product variants
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
        ## Check that both products are in the response content
        content = response.content.decode('utf-8') 


        pos1 = content.find(f"£{self.variant1.price}")
        pos2 = content.find(f"£{self.variant2.price}")


        
        self.assertTrue(pos1 < pos2, "Products are not in the correct order.")


class CataloguePageTest(TestCase):
    def setUp(self):
        
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

        
        
        ###Create an ImagePath for the product variants
        self.image1 = create_test_image("test_image.jpg")
        self.imagepath1 = ImagePath.objects.create(productVariantID=self.variant1, imagepath=self.image1)

        self.image2 = create_test_image("test_image2.jpg")
        self.imagepath2 = ImagePath.objects.create(productVariantID=self.variant2, imagepath=self.image2)

        ##### Define the URL to test the product page (replace with the correct URL)
        self.url = reverse('Catalogue')  
        print(self.url)
    
    def test_view_all_products(self):
       
        
        response = self.client.get(reverse('Catalogue'))
        self.assertEqual(response.status_code, 200)
        
        ##Check that both products are in the response content
        self.assertContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertContains(response, f'<p class="product-name">{self.product2.name}</p>')
        

   

    def test_filter(self):
       
        
        
        response = self.client.get("/catalogue?selected_filters=seasonal" )
        self.assertEqual(response.status_code, 200)
         # Check that both products are in the response content
        self.assertNotContains(response, f'<p class="product-name">{self.product1.name}</p>')
        self.assertNotContains(response, f'<p class="product-name">{self.product2.name}</p>')        
    
    



    def test_product_images_display(self):
        
        response = self.client.get(self.url)

        # Check if images are included for the variants
        self.assertContains(response, self.imagepath1.imagepath.url)  # URL of the image
        self.assertContains(response, self.imagepath2.imagepath.url)  # URL of the image
    




    
    def test_product_price_display(self):
        
        response = self.client.get(self.url)
        
        # Check the price of both products
        self.assertContains(response, f"£{self.variant1.price}")
        self.assertContains(response, f"£{self.variant2.price}")

    def test_orderName(self):

        response = self.client.get("/catalogue?order=name" )
        self.assertEqual(response.status_code, 200)
        ## Check that both products are in the response content
        content = response.content.decode('utf-8') 


        pos1 = content.find(f'<p class="product-name">{self.product1.name}</p>')
        pos2 = content.find(f'<p class="product-name">{self.product2.name}</p>')


        
        self.assertTrue(pos1 < pos2, "Products are not in the correct order.")

    def test_orderPrice(self):

        response = self.client.get("/catalogue?order=productvariant__price" )
        self.assertEqual(response.status_code, 200)
        ### Check that both products are in the response content
        content = response.content.decode('utf-8') 


        pos1 = content.find(f"£{self.variant1.price}")
        pos2 = content.find(f"£{self.variant2.price}")


        
        self.assertTrue(pos1 < pos2, "Products are not in the correct order.")

class ReviewModelTest(TestCase):

    def setUp(self): # create objects
        
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(name='Test Product', description= "Good product")

    def test_create_review(self):
   
        review = Review.objects.create(
            productID=self.product,
            userID=self.user,
            rating=5,
            title='Great Product!',
            description='I really reaaaallyyyyy liked this product. Highly recommend!'
        )

       
        self.assertEqual(review.productID, self.product)
        self.assertEqual(review.userID, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, 'Great Product!')
        self.assertEqual(review.description, 'I really reaaaallyyyyy liked this product. Highly recommend!')
        self.assertIsNotNone(review.reviewDate)

    def test_rating_validation(self):
        # Test invalid rating below 0
        with self.assertRaises(Exception):
            Review.objects.create(
                productID=self.product,
                userID=self.user,
                rating=-1,
                title='Invalid Rating',
                description='This rating is below 0'
            )

        # Test invalid rating above 5
        with self.assertRaises(Exception):
            Review.objects.create(
                productID=self.product,
                userID=self.user,
                rating=6,
                title='Invalid Rating',
                description='This rating is above 5'
            )


class ReviewIntegrationTest(TestCase):
    
    def setUp(self): # create objects
        #Create user, login, product and review
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.product = Product.objects.create(name='Test Product', description= "Good product")
    
        self.review = Review.objects.create(
            productID=self.product,
            userID=self.user,
            rating=5,
            title='Great Product!',
            description='I really reaaaallyyyyy liked this product. Highly recommend!'
        )

        

    def test_containsReview(self):
                
                
        response = self.client.get("/product/1" )
        self.assertEqual(response.status_code, 200)
        #Look for description
        self.assertContains(response, f"<p>{self.review.description}</p>")
        

        

class WishlistModelUnitTest(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(name="Test Product", description="Good product")

        self.wishlist = Wishlists.objects.create(userID=self.user, name="My Wishlist")

    def test_create_wishlist(self):
        # Ensure the wishlist was created successfully
        wishlist = Wishlists.objects.get(userID=self.user)
        self.assertEqual(wishlist.name, "My Wishlist")
        self.assertEqual(wishlist.userID, self.user)

    def test_create_wishlist_item(self):
    ##Create a wishlist item (product added to wishlist)
        wishlist_item = WishlistItem.objects.create(wishlistID=self.wishlist, productID=self.product)
        
      
        self.assertEqual(wishlist_item.wishlistID, self.wishlist)
        self.assertEqual(wishlist_item.productID, self.product)

    def test_wishlist_items_association(self):
       
        product2 = Product.objects.create(name="Test Product 2", description="Another test product")
        product3 = Product.objects.create(name="Test Product 3", description="Yet another test product")
        
        wishlist_item1 = WishlistItem.objects.create(wishlistID=self.wishlist, productID=self.product)
        wishlist_item2 = WishlistItem.objects.create(wishlistID=self.wishlist, productID=product2)
        wishlist_item3 = WishlistItem.objects.create(wishlistID=self.wishlist, productID=product3)

        # Check if all items are correctly associated with the wishlist
        self.assertEqual(self.wishlist.wishListID.count(), 3)  

    def test_delete_wishlist(self):
        # Create a wishlist item, delete it and assure if all items are deleted
        wishlist_item = WishlistItem.objects.create(wishlistID=self.wishlist, productID=self.product)
        self.wishlist.delete()

        

        with self.assertRaises(WishlistItem.DoesNotExist):

            WishlistItem.objects.get(id=wishlist_item.id)

    def test_delete_wishlist_item(self):
        # Create a wishlist item
        wishlist_item = WishlistItem.objects.create(wishlistID=self.wishlist, productID=self.product)
        wishlist_item.delete()

        with self.assertRaises(WishlistItem.DoesNotExist):
            WishlistItem.objects.get(id=wishlist_item.id)