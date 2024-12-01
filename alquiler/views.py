from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def colores(request):
    return render(request, 'colores.html')