from django.urls import reverse
from rest_framework import status

from ..models import Patient, Study
from . import LoggedInTestCase


class StudyTestCase(LoggedInTestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.patient = Patient(first_name='Pedro', last_name='Rodríguez', email='pedro@email.com')
        cls.patient.save()
        
        cls.study = Study(title='Estudio 1', description='Estudio 1', patient=cls.patient)
        cls.study.save()
        
    def test_create_study(self):
        
        study_input = {
            'title':'Estudio 2',
            'description':'Estudio 2',
            'patient': self.patient.id       
        }
        
        response = self.client.post(reverse('studies'), study_input)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Study.objects.count(), 2)
        
    def test_list_studies(self):
        response = self.client.get(reverse('studies'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Study.objects.count())