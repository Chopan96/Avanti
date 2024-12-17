from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def personal(request):
    return render(request, 'administrativo/main.html')

def paciente(request):
    return render(request, 'paciente/ver_ficha.html')

def medico(request):
    return render(request, 'medico/main.html')

