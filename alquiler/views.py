from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def exit(request):
    logout(request)
    return redirect('index')

@login_required
def clientes(request):
    query = request.GET.get('q', '')
    if query:
        clientes = Cliente.objects.filter(nombre__icontains=query) | Cliente.objects.filter(apellido__icontains=query)
    else:
        clientes = Cliente.objects.all()
    
    return render(request, 'clientes.html', {'clientes': clientes, 'query': query})


