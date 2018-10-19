
import unittest
import json
from APIs.app import app
 

class ManagerTestCase(unittest.TestCase):
    def setUp(self): 
        self.app_user = {
            "name": "Jonnie Pemba",
            "username":"jonnie",
            "password": "andela",
            "grade": "C"
        }
        self.product = {
            "prod_name": "bell_bottoms",
            "category": "pants",
            "stock": 20,
            "min_stock": 10,    
            "price": 200
        }
        self.sale = {
            "prod_name": "bell_bottoms",
            "category": "pants", 
            "price": 200
        }

        self.client = app.test_client(self)

    def tearDown(self):
        self.app_user.clear()
        self.product.clear()

    def test_create_user(self):
        resp = self.client.post(
            '/storemanager/api/v1/users',
            data=json.dumps(self.app_user),
            content_type='application/json'
            )
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Jonnie Pemba', str(resp.data))


    def test_update_user(self):

        rp = self.client.post(
            '/storemanager/api/v1/users',
            data=json.dumps({
            "name": "brenda Good",
            "username":"brenda",
            "password": "andela",
            "grade": "C"}), 
            content_type='application/json'
            )
        self.assertEqual(rp.status_code, 201)
        resp = self.client.put(
            '/storemanager/api/v1/users/1',
            data=json.dumps({"grade": "A"}),
            content_type='application/json'
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('A', str(resp.data))


    def test_delete_user(self):     
        resp = self.client.delete('/storemanager/api/v1/users/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))


    """
    Products
    """
    def test_create_product(self):
        resp = self.client.post(
            '/storemanager/api/v1/products',
            data=json.dumps(self.product),
            content_type='application/json'
            )
        self.assertEqual(resp.status_code, 201)
        self.assertIn('pants', str(resp.data))

    def test_update_product(self):
        rp = self.client.post(
            '/storemanager/api/v1/products',
            data=json.dumps({
            "prod_name": "bell_bottoms",
            "category": "pants",
            "stock": 20,
            "min_stock": 10,    
            "price": 200}), 
            content_type='application/json'
            )
        self.assertEqual(rp.status_code, 201)
        resp = self.client.put(
            '/storemanager/api/v1/products/1',
            data=json.dumps({"price": 300}),
            content_type='application/json'
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('300', str(resp.data))

    def test_view_a_product(self):
        resp = self.client.get('/storemanager/api/v1/products/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('pants', str(resp.data))
        self.assertIn('prod_id', str(resp.data))


    def test_view_all_products(self):
        resp = self.client.get('/storemanager/api/v1/products')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('pants', str(resp.data))
        self.assertIn('prod_id', str(resp.data))      


    def test_delete_product(self):
        resp = self.client.delete('/storemanager/api/v1/products/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))


    """
    Sales
    """
    def test_create_sale_order(self):
        resp = self.client.post(
            '/storemanager/api/v1/sales',
            data=json.dumps(self.sale),
            content_type='application/json'
            )
        self.assertEqual(resp.status_code, 201)
        self.assertIn('pants', str(resp.data))
        self.assertIn('sale_id', str(resp.data))


    def test_get_sale_record(self):
        resp = self.client.get('/storemanager/api/v1/sales/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('pants', str(resp.data))
        self.assertIn('sale_id', str(resp.data))    


    def test_get_all_sale_records(self):
        resp = self.client.get('/storemanager/api/v1/sales')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('pants', str(resp.data))
        self.assertIn('sale_id', str(resp.data))    