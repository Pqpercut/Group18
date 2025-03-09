from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import Product, ProductVariant, ImagePath
from django.core.files.uploadedfile import SimpleUploadedFile

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



