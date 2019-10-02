from dal import autocomplete
from django.db.models import Q

from django.http import Http404

from planogrs.models import Residuo, PrestadorServico


# Create your views here.
class ResiduoAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        
        qs = Residuo.objects.all()

        if self.q:
            qs = qs.filter( Q(codigo__icontains=self.q) | Q(descricao__icontains=self.q) )

        return qs


class PrestadorServidoAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        
        qs = PrestadorServico.objects.all()

        if self.q:
            qs = qs.filter(
                Q(cnpj__icontains=self.q) |
                Q(razao_social__icontains=self.q) | 
                Q(nome_fantasia__icontains=self.q)
            )

        return qs
