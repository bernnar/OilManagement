from django.conf import settings
from django.conf.urls import include, url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^repostajes/$', views.repostajes, name='repostajes'),
    url(r'^repostajes/new/$', views.repostajes_new, name='repostajes_new'),
    url(r'^cobros/$', views.cobros, name='cobros'),
    url(r'^cobros/new/$', views.cobros_new, name='cobros_new'),
    url(r'^ajax/get_precio/$', views.get_precio, name='get_precio'),



    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^deposito/new/$', views.deposito_new, name='deposito_new'),
    url(r'^cuenta/new/$', views.cuenta_new, name='cuenta_new'),
    url(r'^conductor/new/$', views.conductor_new, name='conductor_new'),
    url(r'^vehiculo/new/$', views.vehiculo_new, name='vehiculo_new'),

    url(r'^cuentas/', views.cuenta_view),


]
