import unittest
import json
from APIs import app
from database.db import DataBaseConnection
from database.dbqueries import DbQueries


class Utilities(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = DataBaseConnection()
        self.dbq = DbQueries()


    def admin_register(self):
        """Admin registration
        """
        admin = dict(
            name='Jonnie Pemba',
            username='jonnie',
            password='Andela8',
            role='admin'
        )
        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )
        reply = json.loads(resp.data.decode())
        return reply

    def admin_login(self):
        """Admin login
        """
        user = dict(
            username='jonnie',
            password='Andela8'
        )
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(response.data.decode())
        return reply

    def admin_create_user(self):
        """admin creates a store attendant
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love',
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
        return reply

    def admin_create_user2(self):
        """admin creates second store attendant
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Paul Walker',
            username='walker',
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
        return reply

    def attendant_login(self):
        """attendant login
        """
        user = dict(
            username='love',
            password='Andela8'
        )
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(response.data.decode())
        return reply

    def attendant2_login(self):
        """attendant2 login
        """
        user = dict(
            username='walker',
            password='Andela8'
        )
        response = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(response.data.decode())
        return reply

    def admin_add_product(self):
        """admin adds a product to the inventory
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
        return reply