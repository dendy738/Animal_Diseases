from django.urls import path
from . import views

urlpatterns = [
    path('', views.StatisticView.as_view(), name='choice'),
    path('<str:pet>', views.CertainAnimalView.as_view(), name='certain'),
    path('<str:pet>/<str:feat>', views.StatisticPlotView.as_view(), name='plot'),
]