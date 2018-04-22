from django.shortcuts import render, redirect
from django.utils import timezone
from django.db import transaction
from django_tables2 import RequestConfig
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DepositoForm, CuentaForm, VehiculoForm, ConductorForm, OperacionForm, ApunteForm
from .models import Operacion, Deposito, Cuenta
from .tables import CuentaTable, OperacionTable
from django.http import JsonResponse


def home(request):
    return render(request, 'om/home.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('om/home.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.GET['next'])
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages.add_message(request, messages.ERROR, 'Su cuenta está desactivada.')
                    return render(request, 'om/login.html')
            else:
                messages.add_message(request, messages.ERROR, 'Usuario o clave inválidos.')
                return render(request, 'om/login.html')
        else:
            return render(request, 'om/login.html')

@login_required
def repostajes(request):
    table = OperacionTable(Operacion.objects.all())
    RequestConfig(request, paginate={'per_page': 50}).configure(table)
    return render(request, 'om/core/repostajes.html', {'table': table})

def cobros(request):
    if request.user.is_authenticated:
        table = CuentaTable(Cuenta.objects.all())
        RequestConfig(request, paginate={'per_page': 50}).configure(table)
        return render(request, 'om/core/cobros.html', {'table': table})
    else:
        return render(request, 'om/login.html')

def repostajes_new(request):
    form = OperacionForm(request.POST or None)
    if form.is_valid():
        model = form.save(commit=False)
        model.user = request.user
        model.create_date = timezone.now()
        model.save()
        return redirect('home')
    return render(request, 'om/core/repostajes_new.html', {'form': form})

def get_precio(request):
    fecha = request.GET.get('fecha', None)
    data = {
        'precio': Operacion.objects.filter(fecha__lte = fecha).order_by('-fecha').first().precio if len(Operacion.objects.filter(fecha__lte = fecha)) > 0 else 0
    }
    return JsonResponse(data)

def cobros_new(request):
    #TO-do: la inicializacion para filtrar Acreedor, evita las alert de validacion
    form = ApunteForm(request.POST or request.GET or None)
    #form = ApunteForm(default_data)
    if form.is_valid():
        model = form.save(commit=False)
        model.user = request.user
        model.create_date = timezone.now()
        model.save()
        return redirect('home')
    return render(request, 'om/core/cobros_new.html', {'form': form})

def deposito_new(request):
    form= DepositoForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.create_date = timezone.now()
        item.save()
        return redirect('home')
    return render(request, 'om/deposito_edit.html', {'form': form})

def cuenta_new(request):
    form = CuentaForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.create_date = timezone.now()
        item.save()
        return redirect('home')
    return render(request, 'om/cuenta_edit.html', {'form': form})

def cuenta_view(request):
    table = CuentaTable(Cuenta.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'om/cuentas.html', {'table': table})

def vehiculo_new(request):
    form = VehiculoForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.create_date = timezone.now()
        item.save()
        return redirect('home')
    return render(request, 'om/vehiculo_edit.html', {'form': form})


def conductor_new(request):
    form = ConductorForm(request.POST or None)
    if form.is_valid():
        model = form.save(commit=False)
        model.user = request.user
        model.create_date = timezone.now()
        model.save()
        return redirect('home')
    return render(request, 'om/conductor_edit.html', {'form': form})
