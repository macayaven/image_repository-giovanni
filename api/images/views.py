from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, PatientSerializer, StudySerializer, ImageSerializer, ImageCommentSerializer
from .models import User, Patient, Study, Image, ImageComment

# Create your views here.

class RegisterView(generics.CreateAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    # I decided to bring this here for organization purposes
    def perform_create(self, serializer):
        user = User.objects.create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email'),
            first_name=serializer.data.get('first_name'),
            last_name=serializer.data.get('last_name')
        )
        user.set_password(serializer.data.get('password'))
        user.save()
        
        return Response(None, status=status.HTTP_201_CREATED)

class PatientView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class StudyView(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    
    def perform_create(self, serializer):
        
        # if images in serializer: create them else save
        if serializer.validated_data.get('images'):
            #AzureService.upload_batch(request.data.get('images')))
            print('uploading images')

        serializer.save()                
        
    
class ImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    def perform_create(self, serializer):
        
        try:
            #AzureService.upload(request.data.get('file'))
            pass
        except Exception as e:
            print(e)
            return Response({'message': 'Error uploading image'})
        
        serializer.save()
        
class ImageCommentView(generics.ListCreateAPIView):
    
    serializer_class = ImageCommentSerializer
    
    def get_queryset(self):
        image = Image.objects.get(id=self.kwargs['image_id'])
        return ImageComment.objects.filter(image=image)
    
    def perform_create(self, serializer):
        image = Image.objects.get(id=self.kwargs['image_id'])
        user = self.request.user
        serializer.save(image=image, user=user)
            
        
        
    
    