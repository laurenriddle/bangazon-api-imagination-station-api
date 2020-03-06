from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models import Product, Customer, ProductType, Order, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

"""Tests for the product and product detail endpoints.

Author:
    Ryan Crowley
"""

print("test file loaded------------------------")


class TestProducts(TestCase):
    # used to get user auth to work
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1)
        self.product_type = ProductType.objects.create(name="type for testing")
        self.payment_type = PaymentType.objects.create(merchant_name="Visa", account_number="1234567", created_at="2020-03-04 20:41:57.004509", customer_id=self.customer.id, expiration_date="3020-12-31")
        self.order1 = Order.objects.create(created_at="2020-02-24 15:32:15.551752", customer_id=self.customer.id, payment_type_id=self.payment_type.id)
        self.order2 = Order.objects.create(created_at="2020-02-25 15:32:15.551752", customer_id=self.customer.id, payment_type_id=self.payment_type.id)
        self.order3 = Order.objects.create(created_at="2020-02-25 15:32:15.551752", customer_id=self.customer.id)


    def test_post_product(self):
        """TEST for create method on products view"""
        # define a product to be sent to the API
        new_product = {
              "name": "Hot Dog",
              "price": 3.00,
              "description": "Real good, fresh and not expired.",
              "quantity": 11,
              "location": "Franklin",
              "image_path": "./none_pic.jpg",
              "customer_id": self.customer.id,
              "product_type_id": self.product_type.id
            }
        
        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one Product instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Product.objects.get().name, 'Hot Dog')


    def test_get_product(self):
        """TEST for list method on products view"""

        new_product = Product.objects.create(
            name = "Hot Dog",
            price = 3.00,
            description = "Real good, fresh and not expired.",
            quantity = 11,
            location = "Franklin",
            image_path = "./none_pic.jpg",
            customer_id = self.customer.id,
            product_type_id = self.product_type.id
        )

        # Now we can grab all the products (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Hot Dog")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.name.encode(), response.content)


    def test_get_one_product(self):
        """TEST for retrieve method on products view"""

        # Create 2 products
        product_one = Product.objects.create(
            name = "Hot Dog",
            price = 3.00,
            description = "Real good, fresh and not expired.",
            quantity = 11,
            location = "Franklin",
            image_path = "./none_pic.jpg",
            customer_id = self.customer.id,
            product_type_id = self.product_type.id
        )

        product_two = Product.objects.create(
            name = "Cheesburger",
            price = 5.00,
            description = "Medium well!",
            quantity = 9,
            location = "Franklin",
            image_path = "./none_pic.jpg",
            customer_id = self.customer.id,
            product_type_id = self.product_type.id
        )

        # Retrieve product 1
        response = self.client.get(
            reverse('product-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert 200 response status and name == Hot Dog
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Hot Dog")

        # Retrieve product 2
        response = self.client.get(
            reverse('product-detail', kwargs={'pk': 2}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert 200 response status and name == Cheesburger
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Cheesburger")


    def test_delete_product(self):
        """TEST for destroy method on products view"""

        # Create a product
        new_product = Product.objects.create(
            name = "Hot Dog",
            price = 3.00,
            description = "Real good, fresh and not expired.",
            quantity = 11,
            location = "Franklin",
            image_path = "./none_pic.jpg",
            customer_id = self.customer.id,
            product_type_id = self.product_type.id
        )


        # Delete a product. As shown in our post and get tests above, new_product
        # will be the only product in the database, and will have an id of 1
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)

        # Confirm that the product is NOT in the database, which means no products will be
        # response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        # self.assertEqual(len(response.data), 0)
        response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)


    @skip("still working on this.")
    def test_num_sold(self):
        #  Create a new product.

        # Create an order product connecting the product to order 1 (sold)

        # Create an order product connecting the product to order 2 (sold)

        # Create an order product connecting the product to order 3 (not sold)
        pass


if __name__ == '__main__':
    unittest.main()