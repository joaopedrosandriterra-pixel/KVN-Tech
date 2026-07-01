from django.urls import path

from .views import (
    about,
    activate,
    home,
    laboratory,
    login_view,
    logout_view,
    panel,
    project_detail,
    register,
)

urlpatterns = [
    path('', home, name='home'),
    path('sobre/', about, name='about'),
    path('laboratorio/', laboratory, name='laboratory'),
    path('laboratorio/<slug:slug>/', project_detail, name='project_detail'),
    path('painel/', panel, name='panel'),
    path('entrar/', login_view, name='login'),
    path('sair/', logout_view, name='logout'),
    path('cadastro/', register, name='signup'),
    path('ativar/<uidb64>/<token>/', activate, name='activate'),
]
