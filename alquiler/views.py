from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.db import transaction
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
        except (KeyError, Categoria.DoesNotExist, Color.DoesNotExist) as e:
            return render(request, 'add_prenda.html', {
                'categorias': Categoria.objects.all(),
                'colores': Color.objects.all(),
                'error_message': f"Error en el formulario: {e}.  Por favor, asegúrese de seleccionar una categoría y un color válidos."
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

        return redirect('prendas')  # Reemplaza 'prendas' con la URL correcta

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

    for traje in trajes:
        print(f"Traje: {traje.nro_articulo}")
        print(f"  Pantalones asociados: {traje.prendas.filter(categoria__nombre='Pantalon')}")

    return render(request, 'trajes.html', {
        'trajes': trajes,
        'query': query,
        'colores': colores,
    })

@login_required
def listar_pantalones(request, traje_id):
    """Lista pantalones y sacos disponibles, excluyendo los que están asociados a OTROS trajes."""
    traje = get_object_or_404(Traje, pk=traje_id)

    # Obtiene los IDs de los pantalones asociados a trajes *DISTINTOS* al actual
    pantalones_asociados_otros_trajes_ids = Prenda.objects.filter(
        categoria__nombre='Pantalon',
        trajes__isnull=False
    ).exclude(trajes=traje).values_list('id', flat=True).distinct()

    # Obtiene los IDs de los sacos asociados a trajes *DISTINTOS* al actual
    sacos_asociados_otros_trajes_ids = Prenda.objects.filter(
        categoria__nombre='Saco',
        trajes__isnull=False
    ).exclude(trajes=traje).values_list('id', flat=True).distinct()

    # Obtiene pantalones y sacos disponibles y no asociados a OTROS trajes
    prendas = Prenda.objects.filter(
        (Q(categoria__nombre='Pantalon') & ~Q(id__in=pantalones_asociados_otros_trajes_ids)) |
        (Q(categoria__nombre='Saco') & ~Q(id__in=sacos_asociados_otros_trajes_ids)),
        disponible=True
    )

    return render(request, 'listar_pantalones.html', {'traje': traje, 'prendas': prendas})

@login_required
def asociar_prenda(request):
    if request.method == 'POST':
        print("Datos recibidos en request.POST:", request.POST)  # Imprimir los datos

        traje_id = request.POST.get('traje_id')
        pantalon_id = request.POST.get('pantalon_id')
        saco_id = request.POST.get('saco_id')

        traje = get_object_or_404(Traje, pk=traje_id)

        # Procesar el pantalón
        if pantalon_id:
            pantalon = get_object_or_404(Prenda, pk=pantalon_id)

            # Eliminar el pantalón existente del traje (si existe)
            pantalon_actual = traje.prendas.filter(categoria__nombre='Pantalon').first()
            if pantalon_actual:
                traje.prendas.remove(pantalon_actual)

            # Agregar el nuevo pantalón al traje
            traje.prendas.add(pantalon)
            messages.success(request, f'{pantalon.categoria.nombre} {pantalon} asociado al traje {traje}')

        # Procesar el saco
        if saco_id:
            saco = get_object_or_404(Prenda, pk=saco_id)

            # Eliminar el saco existente del traje (si existe)
            saco_actual = traje.prendas.filter(categoria__nombre='Saco').first()
            if saco_actual:
                traje.prendas.remove(saco_actual)

            # Agregar el nuevo saco al traje
            traje.prendas.add(saco)
            messages.success(request, f'{saco.categoria.nombre} {saco} asociado al traje {traje}')

        return redirect('trajes')
    else:
        return redirect('trajes')


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
        form = AlquilerForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener datos del formulario
                    cliente = form.cleaned_data['cliente']
                    prendas = form.cleaned_data['prendas']
                    sacos = form.cleaned_data['sacos']
                    pantalones = form.cleaned_data['pantalones']
                    trajes = form.cleaned_data['trajes']
                    fecha_alquiler = form.cleaned_data['fecha_alquiler']
                    precio_alquiler = form.cleaned_data['precio_alquiler']
                    estado = form.cleaned_data['estado']
                    seña = form.cleaned_data['seña']

                    # Crear el alquiler
                    alquiler = Alquiler(
                        cliente=cliente,
                        fecha_alquiler=fecha_alquiler,
                        precio_alquiler=precio_alquiler,
                        estado=estado,
                        seña=seña,
                        usuario=request.user
                    )
                    alquiler.save()

                    # Asocia todas las prendas al alquiler
                    alquiler.prenda.set(prendas)
                    alquiler.prenda.add(*sacos)
                    alquiler.prenda.add(*pantalones)

                    # Asocia los trajes al alquiler
                    alquiler.traje.set(trajes)
                    alquiler.save()

                    # **ASOCIAR LAS PRENDAS DEL TRAJE AL ALQUILER**
                    for traje in trajes:
                        for prenda in traje.prendas.all():
                            alquiler.prenda.add(prenda) #Asociar prenda individual
                            print(f"Asociando Prenda {prenda.id} del Traje {traje.nro_articulo} al Alquiler") #Debug

                    # Marcar trajes como no disponibles y sus prendas asociadas
                    for traje in trajes:
                        print(f"Traje {traje.nro_articulo} - Disponible antes: {traje.disponible}")  # DEBUG
                        traje.disponible = False
                        traje.save()
                        print(f"Traje {traje.nro_articulo} - Disponible después: {traje.disponible}")  # DEBUG
                        for prenda in traje.prendas.all():
                            print(f"Prenda {prenda.id} - Disponible antes: {prenda.disponible}")  # DEBUG
                            prenda.disponible = False
                            prenda.save()
                            print(f"Prenda {prenda.id} - Disponible después: {prenda.disponible}")  # DEBUG

                    # Marcar sacos y pantalones como no disponibles
                    for prenda in sacos:
                        print(f"Prenda (saco) {prenda.id} - Disponible antes: {prenda.disponible}")  # DEBUG
                        prenda.disponible = False
                        prenda.save()
                        print(f"Prenda (saco) {prenda.id} - Disponible después: {prenda.disponible}")  # DEBUG
                    for prenda in pantalones:
                        print(f"Prenda (pantalón) {prenda.id} - Disponible antes: {prenda.disponible}")  # DEBUG
                        prenda.disponible = False
                        prenda.save()
                        print(f"Prenda (pantalón) {prenda.id} - Disponible después: {prenda.disponible}")  # DEBUG
                    for prenda in prendas:
                        print(f"Prenda (otra prenda) {prenda.id} - Disponible antes: {prenda.disponible}")  # DEBUG
                        prenda.disponible = False
                        prenda.save()
                        print(f"Prenda (otra prenda) {prenda.id} - Disponible después: {prenda.disponible}")  # DEBUG

                    # Si se alquilan sacos o pantalones individualmente, marcar los trajes correspondientes como no disponibles
                    # **PERO NO MARCAR LAS PRENDAS INDIVIDUALES COMO NO DISPONIBLES**
                    # **ASOCIAR EL TRAJE AL ALQUILER**
                    for saco in sacos:
                        trajes_con_saco = Traje.objects.filter(prendas=saco)
                        for traje in trajes_con_saco:
                            print(f"Traje (por saco) {traje.nro_articulo} - Disponible antes: {traje.disponible}")  # DEBUG
                            traje.disponible = False
                            traje.save()
                            print(f"Traje (por saco) {traje.nro_articulo} - Disponible después: {traje.disponible}")  # DEBUG
                            alquiler.traje.add(traje) # Asociar traje al alquiler

                    for pantalon in pantalones:
                        trajes_con_pantalon = Traje.objects.filter(prendas=pantalon)
                        for traje in trajes_con_pantalon:
                            print(f"Traje (por pantalon) {traje.nro_articulo} - Disponible antes: {traje.disponible}")  # DEBUG
                            traje.disponible = False
                            traje.save()
                            print(f"Traje (por pantalon) {traje.nro_articulo} - Disponible después: {traje.disponible}")  # DEBUG
                            alquiler.traje.add(traje)
                            

                return redirect('lista_alquileres')

            except forms.ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                form.add_error(None, "Ocurrió un error inesperado al registrar el alquiler.")

    else:
        form = AlquilerForm()

    return render(request, 'registrar_alquiler.html', {'form': form})



@login_required
def registrar_devolucion(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)

    if request.method == 'POST':
        with transaction.atomic():
            print(f"Alquiler ID: {alquiler.id}")
            print(f"Trajes asociados: {alquiler.traje.all()}")
            print(f"Prendas asociadas: {alquiler.prenda.all()}")
            # Marcar los artículos como disponibles
            for prenda in alquiler.prenda.all():
                print(f"Prenda (devolución) {prenda.id} - Disponible antes: {prenda.disponible}")
                prenda.disponible = True
                prenda.save()
                print(f"Prenda (devolución) {prenda.id} - Disponible después: {prenda.disponible}")

            # Marcar trajes como disponibles
            for traje in alquiler.traje.all():
                print(f"Traje (devolución) {traje.nro_articulo} - Disponible antes: {traje.disponible}")
                traje.disponible = True
                traje.save()
                print(f"Traje (devolución) {traje.nro_articulo} - Disponible después: {traje.disponible}")
                # Verificar si todas las prendas del traje están disponibles
                todas_disponibles = True
                for prenda in traje.prendas.all():
                    if not prenda.disponible:
                        todas_disponibles = False
                        break
                # Solo marcar el traje como disponible si todas sus prendas están disponibles
                if todas_disponibles:
                    print(f"Traje (devolución) {traje.nro_articulo} - Disponible antes: {traje.disponible}")
                    traje.disponible = True
                    traje.save()
                    print(f"Traje (devolución) {traje.nro_articulo} - Disponible después: {traje.disponible}")
                else:
                    print(f"Traje (devolución) {traje.nro_articulo} - No se marca como disponible porque no todas sus prendas están disponibles")

            # Cambiar el estado del alquiler a "devuelto"
            alquiler.estado = 'devuelto'
            alquiler.save()

        messages.success(request, f"Devolución del alquiler {alquiler.id} registrada con éxito.")

        return redirect('lista_alquileres_activos_devolucion')
    return redirect('lista_alquileres_activos_devolucion')
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


@login_required
def lista_alquileres_activos_para_devolucion(request):
    """Lista los alquileres activos (alquilados o reservados)."""
    alquileres = Alquiler.objects.filter(estado__in=['alquilado', 'reservado'])
    return render(request, 'lista_alquileres_activos_devolucion.html', {'alquileres': alquileres})


@login_required
def cancelar_reserva(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)

    if request.method == 'POST':
        if alquiler.prenda:
            for prenda in alquiler.prenda.all():
                prenda.disponible = True
                prenda.save()
        if alquiler.saco:
            for saco in alquiler.saco.all():
                saco.disponible = True
                saco.save()
        if alquiler.pantalon:
            for pantalon in alquiler.pantalon.all():
                pantalon.disponible = True
                pantalon.save()
        if alquiler.traje:
            for traje in alquiler.traje.all():
                saco = traje.saco_set.first()
                pantalon = traje.pantalon_set.first()
                if saco:
                    saco.disponible = True
                    saco.save()
                if pantalon:
                    pantalon.disponible = True
                    pantalon.save()
        # Cambiar el estado del alquiler a un valor adecuado (por ejemplo, "cancelado")
        alquiler.estado = 'cancelado'  # O el estado que prefieras
        alquiler.save()

        return redirect('lista_alquileres_activos_devolucion')

    return render(request, 'cancelar_reserva.html', {'alquiler': alquiler})


@login_required
def lista_trajes_alquilados_reservados(request):
    """Lista los trajes que están alquilados o reservados."""
    trajes_alquilados_reservados = Traje.objects.filter(
        alquiler__estado__in=['alquilado', 'reservado']
    ).distinct()  # Usar distinct() para evitar duplicados

    return render(request, 'lista_trajes_alquilados_reservados.html', {'trajes': trajes_alquilados_reservados})
