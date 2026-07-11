from django.urls import path

from .views import (
    about,
    activate,
    contact_view,
    delete_contact,
    faq,
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
    path('faq/', faq, name='faq'),
    path('laboratorio/', laboratory, name='laboratory'),
    path('laboratorio/<slug:slug>/', project_detail, name='project_detail'),
    path('painel/', panel, name='panel'),
    path('painel/solicitacao/<int:contact_id>/excluir/', delete_contact, name='delete_contact'),
    path('contato/', contact_view, name='contact'),
    path('entrar/', login_view, name='login'),
    path('sair/', logout_view, name='logout'),
    path('cadastro/', register, name='signup'),
    path('ativar/<uidb64>/<token>/', activate, name='activate'),
]

