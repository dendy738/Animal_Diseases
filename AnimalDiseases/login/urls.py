from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('reset_password', views.EmailView.as_view(), name='email_form'),
    path('reset_password/<int:pk>', views.ResetPasswordView.as_view(), name='reset_password'),
]