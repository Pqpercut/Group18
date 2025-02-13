from django.test import TestCase
from django.contrib.auth.models import User
from ecommerceapp.models import Basket, Product, BasketItem

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
        #form wont submit if its negative anyway so do we need this test? 
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




