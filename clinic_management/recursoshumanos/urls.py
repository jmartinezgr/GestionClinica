from django.urls import path
from . import views

urlpatterns = [
    path('home/recursos_humanos',views.home_recursos_humanos,name='home_recursos_humanos')
]