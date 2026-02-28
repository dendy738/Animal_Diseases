from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AnimalTypeView.as_view(), name='animal_type'),
    path('<int:pet>', views.DiseaseSymptomsView.as_view(), name='symptoms_info'),
    path('<int:pet>/result', views.ResultView.as_view(), name='result'),
]