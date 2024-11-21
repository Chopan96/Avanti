from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def personal(request):
    return render(request, 'administrativo/main.html')

def paciente(request):
    return render(request, 'paciente/main.html')

