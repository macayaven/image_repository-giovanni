from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.core.validators import FileExtensionValidator

from .models import User, Study, Patient, Image, ImageComment

class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirmation', 'first_name', 'last_name')
        
    def validate(self, attrs):
        
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({
                'password': 'Passwords must be equal.'
            })
        
        return attrs
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
    
    
class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Patient.objects.all())])
    
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'email')
    
    
class ImageSerializer(serializers.ModelSerializer):
    
    # file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])   
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ('name', 'file_name', 'study', 'comments')
        
    def get_comments(self, obj):
        comments = obj.imagecomment_set.all()
        serializer = ImageCommentSerializer(comments, many=True)
        return serializer.data
   
    
class StudySerializer(serializers.ModelSerializer):
    
    description = serializers.CharField(required=False)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Study
        fields = ('title', 'description', 'patient', 'images')
        
    def get_images(self, obj):
        images = obj.image_set.all()
        serializer = ImageSerializer(images, many=True)
        return serializer.data


class ImageCommentSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = ImageComment
        fields = ('comment', 'user', 'created_at')