from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def clientes(request):
    query = request.GET.get('q', '')
    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query) | Cliente.objects.filter(apellido__icontains=query)
    else:
        clientes = Cliente.objects.all()
    
    return render(request, 'clientes.html', {'clientes': clientes, 'query': query})