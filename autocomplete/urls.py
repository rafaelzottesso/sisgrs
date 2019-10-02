from django.urls import path

from .views import ResiduoAutoComplete, PrestadorServidoAutoComplete

urlpatterns = [
    path('buscar/residuo/', ResiduoAutoComplete.as_view(), name='residuo-autocomplete'),
    path('buscar/prestador-servico/', PrestadorServidoAutoComplete.as_view(),
         name='prestadorservico-autocomplete'),
]
