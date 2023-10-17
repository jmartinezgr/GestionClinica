from django.urls import path
from . import views

urlpatterns = [
    path('home/enfermera',views.home_enfermeras,name='home_enfermera')
]