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
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
    
    
class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Patient.objects.all())])
    
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'email', 'full_name')
    
    
class ImageSerializer(serializers.ModelSerializer):
    
    file = serializers.FileField(write_only=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    file_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Image
        fields = ('id', 'name', 'file', 'file_name', 'study', 'study_title', 'patient_full_name', 'url')
        
    def create(self, validated_data):
        file = validated_data.pop('file')
        validated_data['file_name'] = file.name
        return Image.objects.create(**validated_data)
        
    
class ImageDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ('id', 'name', 'file_name', 'study', 'study_title', 'patient_full_name', 'url', 'comments')
        
    def get_comments(self, obj):
        comments = obj.imagecomment_set.all()
        serializer = ImageCommentSerializer(comments, many=True)
        return serializer.data  
    
    
class StudySerializer(serializers.ModelSerializer):
    
    description = serializers.CharField(required=False)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Study
        fields = ('id', 'title', 'description', 'patient', 'images')
        
    def get_images(self, obj):
        images = obj.image_set.all()
        serializer = ImageSerializer(images, many=True)
        return serializer.data


class ImageCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageComment
        fields = ('id', 'comment', 'user_email', 'user_full_name', 'created_at')