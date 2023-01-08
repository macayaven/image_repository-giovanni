from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.conf import settings

from azure.storage.blob import BlobServiceClient

from .serializers import RegisterSerializer, PatientSerializer, StudySerializer, ImageSerializer, ImageCommentSerializer, \
    ImageDetailSerializer
from .models import User, Patient, Study, Image, ImageComment


class RegisterView(generics.CreateAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    # I decided to bring this here for organization purposes
    def perform_create(self, serializer):
        user = User.objects.create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name')
        )
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        
        return Response(None, status=status.HTTP_201_CREATED)


class PatientView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class StudyView(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer   
        
    
class ImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    def get_serializer(self, *args, **kwargs):
        
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
            
        return super().get_serializer(*args, **kwargs)
    
    def perform_create(self, serializer):
        
        file = serializer.validated_data.get('file')
        
        try:
            blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container='images', blob=file.name)
            blob_client.upload_blob(file)
        except Exception as e:
            print(e)
            raise Exception('Error uploading image')
        
        serializer.save()
        
class ImageDetailView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageDetailSerializer
        
        
class ImageCommentView(generics.ListCreateAPIView):
    
    serializer_class = ImageCommentSerializer
    
    def get_queryset(self):
        image = Image.objects.get(id=self.kwargs['image_id'])
        return ImageComment.objects.filter(image=image)
    
    def perform_create(self, serializer):
        image = Image.objects.get(id=self.kwargs['image_id'])
        user = self.request.user
        serializer.save(image=image, user=user)
            
        
        
    
    