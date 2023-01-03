from django.urls import path
from .views import RegisterView, PatientView, StudyView, ImageView, ImageCommentView
from rest_framework.authtoken import views

urlpatterns = [
    path('register', RegisterView.as_view(), name='register-user'),
    path('login', views.obtain_auth_token, name='login-user'),
    path('patients', PatientView.as_view(), name='patients'),
    path('studies', StudyView.as_view(), name='studies'),    
    path('images', ImageView.as_view(), name='images'),
    path('images/<int:image_id>/comments', ImageCommentView.as_view(), name='images_comments')
]
