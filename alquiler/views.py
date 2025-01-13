from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def exit(request):
    logout(request)
    return redirect('index')

@login_required
def add_prenda(request):
    if request.method == 'POST':
        try:
            categoria = Categoria.objects.get(id=request.POST['categoria_id'])
            color = Color.objects.get(id=request.POST['color_id'])
        except KeyError as e:
            return render(request, 'add_prenda.html', {
                'categorias': Categoria.objects.all(),
                'colores': Color.objects.all(),
                'error_message': f"Error en el formulario: {e}"
            })
            
        descripcion = request.POST.get('descripcion', '')
        
        busto = request.POST.get('busto')
        busto = int(busto) if busto else None
        
        cintura = request.POST.get('cintura')
        cintura = int(cintura) if cintura else None
        
        cadera = request.POST.get('cadera')
        cadera = int(cadera) if cadera else None
        
        largo = request.POST.get('largo')
        largo = int(largo) if largo else None
        
        talle = request.POST.get('talle', None)
        
        prenda = Prenda(
            categoria=categoria,
            color=color,
            descripcion=descripcion,
            busto=busto,
            cintura=cintura,
            cadera=cadera,
            largo=largo,
            talle=talle,
            disponible=True,  # Siempre verdadero
            tintoreria=False,  # Siempre falso
            reparacion=False,  # Siempre falso
        )
        prenda.save()

        return redirect('prendas')

    categorias = Categoria.objects.all()
    colores = Color.objects.all()
    return render(request, 'add_prenda.html', {'categorias': categorias, 'colores': colores})





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
    colores = Color.objects.all()
    query = request.GET.get('q', '')
    if query:
        trajes = Traje.objects.filter(nro_articulo__icontains=query).order_by('nro_articulo')
    else:
        trajes = Traje.objects.all().order_by('nro_articulo')
    return render(request, 'trajes.html', {'trajes': trajes, 'query': query, 'colores': colores})

@login_required
def nuevo_traje(request):
    if request.method == 'POST':
        traje_form = Traje.objects.create(nro_articulo=request.POST['nro_articulo'])
        return redirect('trajes')
    else:
        context = {'nro_articulo': ''}
    return render(request, 'add_traje.html', context)

@login_required
def prendas(request):
    query = request.GET.get('q', '')
    if query:
        terms = query.split()
        filters = Q()
        for term in terms:
            filters &= (Q(categoria__nombre__icontains=term) | Q(color__nombre__icontains=term))
        prendas = Prenda.objects.filter(filters)
    else:
        prendas = Prenda.objects.all()
    
    return render(request, 'prendas.html', {'prendas': prendas, 'query': query})

@login_required
def registrar_alquiler(request):
    if request.method == 'POST':
        cliente_id = request.POST['cliente'].split(' ')[0]
        cliente = Cliente.objects.get(id=cliente_id)

        prendas_ids = request.POST.getlist('prendas')
        prendas = [Prenda.objects.get(id=prenda.split(' ')[0]) for prenda in prendas_ids]

        alquiler = Alquiler(cliente=cliente)
        alquiler.save()
        
        for prenda in prendas:
            alquiler.prendas.add(prenda)

        return HttpResponse('Alquiler registrado con éxito')

    clientes = Cliente.objects.all()
    prendas = Prenda.objects.all()
    lista = {'clientes': clientes,
             'prendas': prendas,}
    return render(request, 'registrar_alquiler.html',lista)





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
