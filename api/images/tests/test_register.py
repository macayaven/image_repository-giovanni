from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import User
from . import BaseTestCase


class RegisterTestCase(BaseTestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        #Create user for login testing
        cls.registered_user = User(
            username='test_username',
            email='test_email@email.com',
            first_name='first name',
            last_name='last name'
        )
        cls.registered_user.set_password('password')
        cls.registered_user.save()
    
    def test_signup(self):
        
        register_input = {
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'password_confirmation': 'password',
            'first_name': 'first name',
            'last_name': 'last_name'
        }
        
        response = self.client.post(reverse('register-user'), register_input)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        
    def test_login(self):
        
        login_input = {
            'username': 'test_email@email.com',
            'password': 'password'
        }
        
        response = self.client.post(reverse('login-user'), login_input)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_access_unauthorized_route(self):
        
        response = self.client.get(reverse('patients'))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)