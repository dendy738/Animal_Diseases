from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserStatisticView.as_view(), name='user_statistic'),
]