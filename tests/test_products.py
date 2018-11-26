import unittest
import json
from APIs import app
from APIs.models.products import Product
from database.db import DataBaseConnection
from database.dbqueries import DbQueries
from .test_utils import Utilities


class ManagerTestCase(Utilities):
    def setUp(self):
        self.client = app.test_client()
        self.db = DataBaseConnection()
        self.dbq = DbQueries()

    def tearDown(self):
        self.dbq.drop_table('users')
        self.dbq.drop_table('products')

    def test_only_admin_can_create_product(self):
        """Tests that only 'admin' can add a product
        """
        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_create_product(self):
        """Tests that 'admin' can add a product
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

    def test_cannot_create_product_with_blacklisted_token(self):
        """Test admin cannot create a product with a blacklisted token
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_cannot_create_product_with_empty_fields(self):
        """Tests that 'admin' cannot add a product with empty fields
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='',
            category='',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Please enter all fields!')
        self.assertEqual(resp.status_code, 400)

    def test_Product_name_cannot_contain_a_number(self):
        """Tests that product_name field cannot contain a number
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_3',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Please enter strings in name and category!')
        self.assertEqual(resp.status_code, 400)

    def test_category_cannot_contain_a_number(self):
        """Tests that category field cannot contain a number
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='4dens',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Please enter strings in name and category!')
        self.assertEqual(resp.status_code, 400)

    def test_stock_and_price_must_be_numbers(self):
        """Tests that stock and price fields must be numbers
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock='stock',
            price='money'
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'The Stock and Price must be numbers!')
        self.assertEqual(resp.status_code, 400)

    def test_product_exists_in_inventory(self):
        """Tests that product already exists in the Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'This product exists in the Inventory!')
        self.assertEqual(resp.status_code, 400)

    def test_view_a_product(self):
        """Tests that a user can view a product in the Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertIn('NY_denims', str(reply['product']))
        self.assertEqual(resp.status_code, 200)

    def test_cannot_view_a_product_with_blacklisted_token(self):
        """Tests that a user cannot view a product in the Inventory with blacklisted token
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_view_all_products(self):
        """Tests that a user can view all products in the Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertIn('NY_denims', str(reply['products']))
        self.assertEqual(resp.status_code, 200)

    def test_cannot_view_all_products_with_blacklisted_token(self):
        """Tests that a user cannot view all products in the Inventory with blacklisted token
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)    

    def test_view_product_that_doesnot_exist_in_inventory(self):
        """Tests that a user cannot view a product that doesnot exist in the Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get(
            '/api/v1/products/2',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(resp.status_code, 404)

    def test_view_products_from_empty_inventory(self):
        """Tests that a user cannot view products from empty Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']

        resp = self.client.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'There are no products yet!')
        self.assertEqual(resp.status_code, 404)

    def test_view_product_with_invalid_id(self):
        """Tests that a user cannot view a product with invalid id
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get(
            '/api/v1/products/2kk',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Try an interger for product id')
        self.assertEqual(resp.status_code, 400)

    def test_update_product(self):
        """Test that product can be updated successfully
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        product_update = dict(
            prod_name='NY_jeans',
            category='denims',
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'product updated!')
        self.assertEqual(resp.status_code, 200)

    def test_cannot_update_product_with_blacklisted_token(self):
        """Test that product cannot be updated successfully
        with blacklisted token
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        product_update = dict(
            prod_name='NY_jeans',
            category='denims',
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_update_nonexistant_product(self):
        """Test that you cant updated a nonexistant product"""
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product_update = dict(
            prod_name='NY_jeans',
            category='denims',
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], "This product doesn't exists in the Inventory!")
        self.assertEqual(resp.status_code, 400)

    def test_unauthorized_product_update(self):
        """Test that product cannot be updated with unauthorised user
        """
        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        product_update = dict(
            prod_name='NY_jeans',
            category='denims',
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)

    def test_update_product_with_empty_fields(self):
        """Test that product cannot be updated with empty fields
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        product_update = dict(
            prod_name='',
            category='',
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'prod_name and category cannot be empty!')
        self.assertEqual(resp.status_code, 400)

    def test_update_product_with_numbers_for_strings(self):
        """Test that product cannot be updated with numbers for strings
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        product_update = dict(
            prod_name=4562,
            category=5248,
            stock=50,
            price=180
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'prod_name and category should be characters!')
        self.assertEqual(resp.status_code, 400)

    def test_update_product_with_characters_for_numbers(self):
        """Test that product cannot be updated with strings for numbers
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        product_update = dict(
            prod_name='NY_denims',
            category='denims',
            stock='many',
            price='pesa'
        )
        resp = self.client.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product_update),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'The Stock and Price must be numbers!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_delete_product(self):
        """Test that admin can delete a product
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/products/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Product deleted!')
        self.assertEqual(resp.status_code, 200)

    def test_admin_cannot_delete_product_with_blacklisted_token(self):
        """Test that admin can delete a product
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/v1/products/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_non_admin_cannot_delete_product(self):
        """Test that a non admin cannot delete a product
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        resp = self.client.delete(
            '/api/v1/products/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_cannot_delete_product_from_empty_Inventory(self):
        """Test that admin cannnot delete a product from empty Inventory
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        
        resp = self.client.delete(
            '/api/v1/products/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'There are no products in Inventory!')
        self.assertEqual(resp.status_code, 404)

    def test_admin_cannot_delete_nonexistant_product(self):
        """Test that admin cannnot delete a non-existant product
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/products/2',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'This product does not exist in Inventory!')
        self.assertEqual(resp.status_code, 404)

    def test_admin_cannot_delete_product_with_non_integer_prod_id(self):
        """Test that admin cannnot delete a product with no-integer prod_id
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        product = dict(
            prod_name='NY_denims',
            category='denims',
            stock=20,
            price=150
        )
        resp = self.client.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Product successfully added to Inventory!')
        self.assertEqual(resp.status_code, 201)

        resp = self.client.delete(
            '/api/v1/products/kk',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'The product id should be a number!')
        self.assertEqual(resp.status_code, 400)