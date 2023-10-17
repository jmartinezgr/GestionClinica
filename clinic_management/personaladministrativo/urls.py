from django.urls import path
from . import views

urlpatterns = [
    path('home/personal_administrativo',views.home_personal_administrativo,name='home_personal_administrativo')
]