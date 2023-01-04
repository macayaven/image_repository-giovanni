from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from ..models import Patient, Study, Image
from . import LoggedInTestCase


class ImageTestCase(LoggedInTestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.patient = Patient(first_name='Pedro', last_name='Rodríguez', email='pedro@email.com')
        cls.patient.save()
        
        cls.study = Study(title='Estudio 1', description='Estudio 1', patient=cls.patient)
        cls.study.save()
        
        cls.image = Image(name='Imagen 1', file_name='Imagen 1', study=cls.study)
        cls.image.save()
        
    def test_create_image(self):
        
        file_obj = SimpleUploadedFile('file.jpg', b'file contents')
        
        image_input = {
            'name':'Imagen 2',
            'file_name':'Imagen 2',
            'study': self.study.id,
            'file': file_obj
        }
        
        response = self.client.post(reverse('images'), data=image_input, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 2)
        
    def test_list_images(self):
        response = self.client.get(reverse('images'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Image.objects.count())
        
    def test_detail_image(self):
        response = self.client.get(reverse('images_detail', kwargs={'pk': self.image.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.image.id)
        self.assertEqual(response.data.get('name'), self.image.name)
        