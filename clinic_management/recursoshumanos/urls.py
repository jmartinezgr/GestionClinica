from django.urls import path
from . import views
from user.views import registro_view

urlpatterns = [
    path('home/recursos_humanos',registro_view,name='home_recursos_humanos')
]