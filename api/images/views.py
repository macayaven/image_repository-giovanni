from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer
from .models import User

# Create your views here.

class RegisterView(generics.CreateAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class TestView(generics.GenericAPIView):
    
    def get(self, request):
        return Response('Esto es un test', status=status.HTTP_200_OK)
        
        
    
    