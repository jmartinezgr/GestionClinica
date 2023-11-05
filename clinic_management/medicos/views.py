from django.shortcuts import render, redirect
from .forms import HistoriaClinicaForm

def crear_historia_clinica(request):
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            # Puedes redirigir a una página de éxito o a donde desees
            return redirect('crear_historia_clinica')
    else:
        form = HistoriaClinicaForm()

    return render(request, 'crear_historia.html', {'form': form})