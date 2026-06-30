from django.urls import path

from .views import (
    about,
    activate,
    home,
    laboratory,
    login_view,
    logout_view,
    register,
)

urlpatterns = [
    path('', home, name='home'),
    path('sobre/', about, name='about'),
    path('laboratorio/', laboratory, name='laboratory'),
    path('entrar/', login_view, name='login'),
    path('sair/', logout_view, name='logout'),
    path('cadastro/', register, name='signup'),
    path('ativar/<uidb64>/<token>/', activate, name='activate'),
]
