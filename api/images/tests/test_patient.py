from django.urls import reverse
from rest_framework import status

from ..models import Patient
from . import LoggedInTestCase


class PatientTestCase(LoggedInTestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.patient = Patient(
            first_name='Pedro',
            last_name='Rodríguez',
            email='pedro@email.com'
        )
        cls.patient.save()
        
    def test_create_patient(self):
        
        patient_input = {
            'first_name':'Pepa',
            'last_name':'Domínguez',
            'email': 'pepa@email.com'       
        }
        
        response = self.client.post(reverse('patients'), patient_input)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)
        
    def test_list_patients(self):
        response = self.client.get(reverse('patients'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Patient.objects.count())
        