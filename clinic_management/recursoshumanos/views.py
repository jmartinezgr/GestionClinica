from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 

# Create your views here.

@login_required
def home_recursos_humanos(request):

    return render(request, 'recursoshumanos.html', {'user': request.user})