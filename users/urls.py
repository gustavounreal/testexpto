from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.redirect_to_login),
    path('cadastrar/', views.cadastrar_dados_usuario, name='cadastrar_dados_usuario'),
    path('alterar/', views.alterar_dados_usuario, name='alterar_dados_usuario'),
    path('atualizar/', views.atualizar_dados_usuario, name='atualizar_dados_usuario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'), 
    path('cadastro-clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path('buscar-vendedor/', views.buscar_vendedor, name='buscar_vendedor'),
    path('cadastro-vendas/', views.cadastro_vendas, name='cadastro_vendas'),
    path('vendas/', views.minhas_vendas, name='vendas'),
    path('buscar-boletos/', views.buscar_boletos, name='buscar_boletos'),
    path('alterar-status-boleto/<int:boleto_id>/', views.alterar_status_boleto, name='alterar_status_boleto'),
]

