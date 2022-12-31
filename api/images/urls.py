from django.urls import path
from .views import RegisterView, TestView
from rest_framework.authtoken import views

urlpatterns = [
    path('register', RegisterView.as_view(), name='register-user'),
    path('test', TestView.as_view(), name='test'),
    path('login', views.obtain_auth_token)
]
