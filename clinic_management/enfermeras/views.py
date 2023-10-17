from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 

# Create your views here.

@login_required
def home_enfermeras(request):
    
    return render(request, 'enfermera.html', {'user': request.user})