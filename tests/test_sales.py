import unittest
import json
from APIs import app
from APIs.models.products import Product
from APIs.models.sales import Sale
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
        self.dbq.drop_table('sales')

    def test_attendant_make_a_sale(self):
        """Tests that 'attendant' can make a sale
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

    def test_only_attendant_can_make_a_sale(self):
        """Tests that only 'attendant' can make a sale
        """
        resp = self.admin_add_product()
        reply = self.admin_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)

    def test_cannot_make_sale_with_missing_fields(self):
        """Tests that 'attendant' cannot make a sale with missing fields
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'One of the fields is empty!')
        self.assertEqual(resp.status_code, 400)

    def test_cannot_make_sale_with_wrong_datatypes(self):
        """Tests that 'attendant' cannot make a sale with missing fields
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_345", 
                "quantity":'Kummi'
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'prod_name & quantity should be a character & number respectively!')
        self.assertEqual(resp.status_code, 400)

    def test_cannot_sale_nonexistant_product(self):
        """Tests that 'attendant' cannot sale a product thats not in the Inventory
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"Paris_heels", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'This product is not in the Inventory!')
        self.assertEqual(resp.status_code, 404)

    def test_cannot_sale_out_of_stock_product(self):
        """Tests that 'attendant' cannot sale a product thats out of stock
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":20
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'NY_denims is out of stock!')
        self.assertEqual(resp.status_code, 404)

    def test_cannot_sell_more_than_stock(self):
        """Tests that 'attendant' cannot sale more than stocked quantity
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":15
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Only 10 NY_denims available right now!')
        self.assertEqual(resp.status_code, 400)

    def test_get_sale_record(self):
        """Tests that admin or attendant can view a sale
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale fetched sucessfully!')
        self.assertEqual(resp.status_code, 200)

    def test_attendant_can_only_view_own_sale(self):
        """Tests that attendant can only view a sale they made
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Benja Maisha',
            username='maisha',
            password='Andela8',
            role='attendant'
        )

        resp = self.client.post(
            '/api/v1/users',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())

        user = dict(
            username='maisha',
            password='Andela8'
        )
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(response.data.decode())
        token = reply['token']

        resp = self.client.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'You have no access to this sale!')
        self.assertEqual(resp.status_code, 401)

    def test_cannot_get_empty_sales(self):
        """Tests that cannot view sales, if there no sales created yet
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']

        resp = self.client.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'This sale does not exist!')
        self.assertEqual(resp.status_code, 400)

    def test_get_all_sale_records(self):
        """Tests that admin can view all sale records
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        reply = self.admin_login()
        token = reply['token']

        resp = self.client.get(
            '/api/v1/sales',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'All Sale records fetched sucessfully!')
        self.assertEqual(resp.status_code, 200)

    def test_admin_only_can_get_all_sale_records(self):
        """Tests that admin only can view all sale records
        """
        reply = self.admin_add_product()

        resp = self.admin_create_user()
        reply = self.attendant_login()
        token = reply['token']
        sale = dict(products = [
            {
                "prod_name":"NY_denims", 
                "quantity":10
            }
	    ])
        resp = self.client.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Sale record created')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            '/api/v1/sales',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)