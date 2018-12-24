import unittest
import json
import time
from APIs import app
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
        self.dbq.drop_table('blacklisted_tokens')

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

    def test_admin_register_no_name(self):
        """Test admin can not register with empty name field
        """
        admin = dict(
            name='',
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

        self.assertEqual(reply['message'], 'Enter name / username in string format!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_register_no_username(self):
        """Test admin can not register with empty username field
        """
        admin = dict(
            name='Jonnie Pemba',
            username='',
            password='Andela8',
            role='admin'
        )

        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Enter name / username in string format!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_register_no_password(self):
        """Test admin can not register with empty password field
        """
        admin = dict(
            name='Jonnie Pemba',
            username='jonnie',
            password='',
            role='admin'
        )

        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_register_wrong_password(self):
        """Test admin can not register with invalid password field
        """
        admin = dict(
            name='Jonnie Pemba',
            username='jonnie',
            password='Andela',
            role='admin'
        )

        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_register_wrong_role(self):
        """Test admin can not register with invalid role field
        """
        admin = dict(
            name='Jonnie Pemba',
            username='jonnie',
            password='Andela8',
            role='keeper'
        )

        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'role should be admin!')
        self.assertEqual(resp.status_code, 400)

    def test_register_only_one_admin(self):
        """Test can not register more than one admin
        """
        reply = self.admin_register()

        admin = dict(
            name='Codjoe Ronnie',
            username='ronnie',
            password='Andela8',
            role='admin'
        )

        resp = self.client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(admin)
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Admin is already registered, please login!')
        self.assertEqual(resp.status_code, 400)

    def test_user_login(self):
        """Test that a user can login
        """
        reply = self.admin_register()
        user = dict(
            username='jonnie',
            password='Andela8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())


        self.assertEqual(reply['message'], 'Login sucessful!')
        self.assertTrue(reply['token'])
        self.assertEqual(resp.status_code, 200)

    def test_login_with_empty_username(self):
        """Test that a user cannot login with empty username field
        """
        reply = self.admin_register()
        user = dict(
            username='',
            password='Andela8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())


        self.assertEqual(reply['message'], 'Wrong username!')
        self.assertEqual(resp.status_code, 400)

    def test_login_with_empty_password(self):
        """Test that a user cannot login with empty password field
        """
        reply = self.admin_register()
        user = dict(
            username='jonnie',
            password=''
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())


        self.assertEqual(reply['message'], 'Wrong password!')
        self.assertEqual(resp.status_code, 400)

    def test_login_with_wrong_username(self):
        """Test that a user cannot login with wrong username field
        """
        reply = self.admin_register()
        user = dict(
            username='codjoe',
            password='Andela8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())


        self.assertEqual(reply['message'], 'Wrong username!')
        self.assertEqual(resp.status_code, 400)

    def test_login_with_wrong_password(self):
        """Test that a user cannot login with wrong password field
        """
        reply = self.admin_register()
        user = dict(
            username='jonnie',
            password='Andyandy8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(resp.data.decode())


        self.assertEqual(reply['message'], 'Wrong password!')
        self.assertEqual(resp.status_code, 400)
    
    def test_admin_create_user(self):
        """Test admin successfully creates a store attendant
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

        self.assertEqual(reply['message'], 'Summer Love has been registered')
        self.assertEqual(resp.status_code, 201)

    def test_cannot_create_user_with_blacklisted_token(self):
        """Test admin cannot create a store attendant 
        with blacklisted token
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

        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_cannot_create_user_with_empty_fields(self):
        """Test admin cannot create a store attendant with empty fields
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='',
            username='',
            password='',
            role=''
        )

        resp = self.client.post(
            '/api/v1/users',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Please input all fields!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_user_with_different_roles(self):
        """Test admin cannot create a store attendant with different roles
        other than 'admin' or 'attendant'
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love',
            password='Andela8',
            role='supervisor'
        )

        resp = self.client.post(
            '/api/v1/users',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'role should either be admin or attendant')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_user_with_invalid_name(self):
        """Test admin cannot create a store attendant with invalid name
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love3',
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

        self.assertEqual(reply['message'], 'Enter name in a correct string format, (john doe)!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_user_with_invalid_username(self):
        """Test admin cannot create a store attendant with invalid username
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love summer',
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

        self.assertEqual(reply['message'], 'Enter username in a correct string format no spaces, (johndoe)!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_user_with_invalid_password(self):
        """Test admin cannot create a store attendant with invalid password
        """
        resp = self.admin_register()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love',
            password='Andyandy',
            role='attendant'
        )

        resp = self.client.post(
            '/api/v1/users',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(resp.data.decode())

        self.assertEqual(reply['message'], 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_users_with_same_name(self):
        """Test admin cannot create store attendants with same names
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

        self.assertEqual(reply['message'], 'This name is already registered!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_create_users_with_same_username(self):
        """Test admin cannot create store attendants with same usernames
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

        user = dict(
            name='Paul Love',
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
        self.assertEqual(reply['message'], 'This username is already taken!')
        self.assertEqual(resp.status_code, 400)

    def admin_can_view_all_user_accounts(self):
        """Test admin can view all user accounts
        """
        resp = self.admin_create_user()
        reply = self.admin_create_user2()
        resp = self.admin_login()
        token = resp['token']

        resp = self.client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        
        self.assertIn('love', str(reply['users'][1]['username']))
        self.assertIn('walker', str(reply['users'][2]['username']))
        self.assertEqual(resp.status_code, 200)

    def attendants_cannot_view_user_accounts(self):
        """Test store attendants cannot view user accounts
        """
        reply = self.admin_create_user()
        resp = self.attendant_login()
        token = resp['token']
        resp = self.client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Unauthorized Access!')
        self.assertEqual(resp.status_code, 401)

    def test_cannot_view_all_users_with_blacklisted_token(self):
        """Tests that admin cannot view all users in the Inventory\
        with blacklisted token
        """
        resp = self.admin_create_user()
        reply = self.admin_create_user2()
        resp = self.admin_login()
        token = resp['token']

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)  

    def test_admin_update_user(self):
        """Test admin successfully updates a store attendant
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Lover',
            username='lover',
            password='Andela8',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'user updated!')
        self.assertEqual(resp.status_code, 200)

    def test_cannot_update_user_with_blacklisted_token(self):
        """Test admin cannot update a store attendant\
        with blacklisted token
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        user = dict(
            name='Summer Lover',
            username='lover',
            password='Andela8',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_cannot_update_user_with_empty_fields(self):
        """Test admin cannot update a store attendant with empty fields
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='',
            username='',
            password='',
            role=''
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Please input all fields!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_update_user_with_different_roles(self):
        """Test admin cannot update a store attendant with different roles\
        other than 'admin' or 'attendant'
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Lover',
            username='lover',
            password='Andela8',
            role='supervisor'
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'role should either be admin or attendant')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_update_user_with_invalid_name(self):
        """Test admin cannot update a store attendant with invalid name
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Lover3',
            username='lover',
            password='Andela8',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Enter name in a correct string format, (john doe)!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_update_user_with_invalid_username(self):
        """Test admin cannot update a store attendant with invalid username
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love summer',
            password='Andela8',
            role='attendant'
        )

        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Enter username in a correct string format no spaces, (johndoe)!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_update_user_with_invalid_password(self):
        """Test admin cannot update a store attendant with invalid password
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love',
            password='Andela',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/2',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!')
        self.assertEqual(resp.status_code, 400)
           
    def test_admin_cannot_update_user_with_vague_user_id(self):
        """Test admin cannot update a store attendant with vague user id
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Love',
            username='love',
            password='Andela8',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/kk',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'User_id should be numbers!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_update_non_existant_user(self):
        """Test admin cannot updates a user that doesnt exist
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        user = dict(
            name='Summer Lover',
            username='lover',
            password='Andela8',
            role='attendant'
        )
        resp = self.client.put(
            '/api/v1/users/5',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], "This user doesn't exist!")
        self.assertEqual(resp.status_code, 400)

    def test_admin_can_delete_a_user(self):
        """Test admin can delete a user
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        
        resp = self.client.delete(
            '/api/v1/users/2',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], "User deleted!")
        self.assertEqual(resp.status_code, 200)

    def test_cannot_delete_user_with_blacklisted_token(self):
        """Test admin cannot delete a store attendant\
        with blacklisted token
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/v1/users/2',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Invalid Authentication, Please Login!')
        self.assertEqual(resp.status_code, 401)

    def test_admin_cannot_delete_user_with_vague_user_id(self):
        """Test admin cannot delete a store attendant with vague user id
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        
        resp = self.client.delete(
            '/api/v1/users/kk',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'The user id should be a number!')
        self.assertEqual(resp.status_code, 400)

    def test_admin_cannot_delete_non_existant_user(self):
        """Test admin cannot delete a user that doesnt exist
        """
        resp = self.admin_create_user()
        reply = self.admin_login()
        token = reply['token']
        
        resp = self.client.delete(
            '/api/v1/users/5',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], "This attendant does not exist!")
        self.assertEqual(resp.status_code, 404)

    def test_user_logout(self):
        """Test user can logout before token expires
        """
        reply = self.admin_register()
        user = dict(
            username='jonnie',
            password='Andela8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Login sucessful!')
        self.assertTrue(reply['token'])
        self.assertEqual(resp.status_code, 200)

        token = reply['token']
        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

    def test_cannot_logout_with_blacklisted_token(self):
        """Test user cannot logout with a blacklisted token
        """
        reply = self.admin_register()
        user = dict(
            username='jonnie',
            password='Andela8'
        )
        resp = self.client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'Login sucessful!')
        self.assertTrue(reply['token'])
        self.assertEqual(resp.status_code, 200)

        token = reply['token']
        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are successfully logged out!')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/v1/logout',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(reply['message'], 'You are already logged out!')
        self.assertEqual(resp.status_code, 404)