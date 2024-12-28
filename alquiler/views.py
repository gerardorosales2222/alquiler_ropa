from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
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
        terms = query.split()
        filters = Q()
        for term in terms:
            filters |= Q(nombre__icontains=term) | Q(apellido__icontains=term)
        clientes = Cliente.objects.filter(filters)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes, 'query': query})


@login_required
def trajes(request):
    query = request.GET.get('q', '')
    if query:
        trajes = Traje.objects.filter(nro_articulo__icontains=query)
    else:
        trajes = Traje.objects.all()
    return render(request, 'trajes.html', {'trajes': trajes, 'query': query})

@login_required
def nuevo_traje(request):
    if request.method == 'POST':
        traje_form = TrajeForm(request.POST)
        pantalon_form = PantalonForm(request.POST)
        saco_form = SacoForm(request.POST)
        
        if traje_form.is_valid() and pantalon_form.is_valid() and saco_form.is_valid():
            traje = traje_form.save()
            pantalon = pantalon_form.save(commit=False)
            saco = saco_form.save(commit=False)
            pantalon.traje = traje
            saco.traje = traje
            pantalon.save()
            saco.save()
            return redirect('trajes')
            
    else:
        traje_form = TrajeForm()
        pantalon_form = PantalonForm()
        saco_form = SacoForm()
        
    return render(request, 'nuevo_traje.html', {
        'traje_form': traje_form,
        'pantalon_form': pantalon_form,
        'saco_form': saco_form,
    })

@login_required
def prendas(request):
    query = request.GET.get('q', '')
    if query:
        terms = query.split()
        filters = Q()
        for term in terms:
            filters |= Q(categoria__nombre__icontains=term) | Q(color__nombre__icontains=term)
        prendas = Prenda.objects.filter(filters)
    else:
        prendas = Prenda.objects.all()
    
    return render(request, 'prendas.html', {'prendas': prendas, 'query': query})
