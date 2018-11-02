import unittest
import json
from APIs import app
from database.db import DataBaseConnection
from database.dbqueries import DbQueries


class ManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = DataBaseConnection()
        self.dbq = DbQueries()
    
    def tearDown(self):
        self.dbq.drop_table('users')

    def test_admin_register(self):
        """Test admin successful registration
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

        self.assertEqual(reply['message'], 'Jonnie Pemba has been registered')
        self.assertEqual(resp.status_code, 201)

    def login_user(self):
        """User login method 
        """
        user = dict(
            username='jonnie',
            password='Andela8'
        )

        resp = self.client.post('/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())

        return reply