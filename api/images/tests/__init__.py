from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import User


class BaseTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        
        
class LoggedInTestCase(BaseTestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        # User to use for login
        cls.user = User(
            username ='test',
            email = 'test@example.com',
            first_name ='test',
            last_name ='test'             
        )
        cls.user.set_password('password')
        cls.user.save()
        
    # Doing this separately because I don't want to execute "setUpTestData" content on every test
    def setUp(self):
        self.client.force_authenticate(self.user)