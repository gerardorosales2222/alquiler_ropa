from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
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
def buscar(request):
    clientes = Cliente.objects.all()
    return render(request, 'buscar.html', {'cli':clientes})

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

@login_required
def registrar_alquiler(request):
    clientes = Cliente.objects.all()
    prendas = Prenda.objects.all()
    lista = {'clientes': clientes,
             'prendas': prendas,}
    return render(request, 'registrar_alquiler.html',lista)


@login_required
def guardar_alquiler(request):
#    id_hab=request.POST['hab']
#    h=habitación.objects.get(id=id_hab)
#    id_cli=request.POST['cliente']
#    c=cliente.objects.get(id=id_cli)
#    días=request.POST['días']
#    r = reserva.objects.create(habitación=h,cliente=c,cant_días=días)
#    h.ocupada='True'
#    h.save()
    return redirect('/reservas')

@login_required
def registrar_devolucion(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    if request.method == 'POST':
        alquiler.estado = 'reservado'
        if alquiler.traje:
            for traje in alquiler.traje.all():
                traje.disponible = True
                traje.save()
        if alquiler.pantalon:
            for pantalon in alquiler.pantalon.all():
                pantalon.disponible = True
                pantalon.save()
        if alquiler.saco:
            for saco in alquiler.saco.all():
                saco.disponible = True
                saco.save()
        if alquiler.prenda:
            for prenda in alquiler.prenda.all():
                prenda.disponible = True
                prenda.save()
        alquiler.save()
        return redirect('lista_alquileres')
    return render(request, 'registrar_devolucion.html', {'alquiler': alquiler})

@login_required
def lista_alquileres(request):
    hoy = timezone.now().date()
    hace_una_semana = hoy - timedelta(weeks=1)
    dentro_de_un_mes = hoy + timedelta(weeks=3)
    
    query_date = request.GET.get('fecha', '')
    ver_todos = request.GET.get('ver_todos', '')

    if ver_todos:
        alquileres = Alquiler.objects.all()
    elif query_date:
        alquileres = Alquiler.objects.filter(fecha_alquiler=query_date)
    else:
        alquileres = Alquiler.objects.filter(fecha_alquiler__range=(hace_una_semana, dentro_de_un_mes))

    return render(request, 'lista_alquileres.html', {'alquileres': alquileres, 'query_date': query_date})
