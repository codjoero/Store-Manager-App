import unittest
import json
from APIs import app
from database.db import DataBaseConnection
from .test_base import ManagerTestCase


class TestUsers(ManagerTestCase):
    """Class tests admin register and user login 
    """
    def setUp(self):
        self.client = app.test_client()
        self.db = DataBaseConnection()
        self.base = ManagerTestCase()
