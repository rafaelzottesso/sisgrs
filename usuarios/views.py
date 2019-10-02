from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

from django.views.generic import TemplateView
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.contrib.auth.models import Group, User

from .forms import UserUpdateEmailForm, FiscalCreateForm, FiscalUpdateForm

class UsuarioTesteView(TemplateView):
    template_name = "planogrs/base.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = User
    template_name = "planogrs/form_crispy.html"
    success_url = reverse_lazy('index-auth')
    form_class = UserUpdateEmailForm

    def get_object(self, queryset=None):
        self.object = User.objects.get(pk=self.request.user.pk)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(UserUpdateView, self).\
            get_context_data(*args, **kwargs)
        context['titulo'] = "Atualizar e-mail de recuperação de senha"
        context['urllista'] = reverse_lazy('index-auth')
        return context


class FiscalCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = User
    template_name = "planogrs/form_crispy.html"
    success_url = reverse_lazy('listar-fiscal')
    form_class = FiscalCreateForm

    def form_valid(self, form):
        # Faz o padrão
        response = super(FiscalCreateView, self).form_valid(form)
        # Adiciona o usuário ao grupo Fiscal
        self.object.groups.add(Group.objects.get(name='Fiscal'))
        return response

    def get_context_data(self, *args, **kwargs):
        context = super(FiscalCreateView, self).\
            get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar novo Fiscal"
        context['urllista'] = reverse_lazy('listar-fiscal')
        return context


class FiscalUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = User
    template_name = "planogrs/form_crispy.html"
    success_url = reverse_lazy('listar-fiscal')
    form_class = FiscalUpdateForm

    def get_object(self, queryset=None):
        self.object = User.objects.get(pk=self.kwargs['pk'], groups__name='Fiscal')
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(FiscalUpdateView, self).\
            get_context_data(*args, **kwargs)
        context['titulo'] = "Alterar nome do Fiscal"
        context['urllista'] = reverse_lazy('listar-fiscal')
        return context


class FiscalListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = User
    template_name = "planogrs/list_base.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):
        # O Visual acusa erro, mas está correto! Classe.objects.filter(...)
        self.object_list = User.objects.filter(groups__name='Fiscal')
        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(FiscalListView, self).get_context_data(*args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            # 'Empresa',
            'Nome',
            'Sobrenome',
            'Usuário',
            'Email'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]
        # Título da página
        context['titulo'] = 'Lista de Fiscais cadastrados'
        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Fiscal'
        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-fiscal'
        context['urlalterar'] = 'alterar-fiscal'

        return context
