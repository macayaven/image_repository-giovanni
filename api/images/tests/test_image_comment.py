from django.urls import reverse
from rest_framework import status

from ..models import Patient, Study, Image, ImageComment
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
        
        cls.image_comment = ImageComment(image=cls.image, user=cls.user, comment="Comentario")
        cls.image_comment.save()
        
    def test_create_image_comment(self):
        
        image_comment_input = {
            'user': self.user.id,
            'comment':'Comentario'      
        }
        
        response = self.client.post(reverse('images_comments', kwargs={'image_id': self.image.id}), image_comment_input)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImageComment.objects.count(), 2)
        
    def test_list_images(self):
        response = self.client.get(reverse('images_comments', kwargs={'image_id': self.image.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ImageComment.objects.count())