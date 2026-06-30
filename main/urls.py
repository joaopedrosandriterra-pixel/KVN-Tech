from django.urls import path

from .views import about, home, laboratory

urlpatterns = [
    path('', home, name='home'),
    path('sobre/', about, name='about'),
    path('laboratorio/', laboratory, name='laboratory'),
]
