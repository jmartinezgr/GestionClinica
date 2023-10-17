from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 


@login_required
def home_personal_administrativo(request):
    return render(request, 'personaladministrativo.html', {'user': request.user})