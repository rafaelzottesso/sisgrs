from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from .models import Tipo, Chamado, Mensagem

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

from django.utils import timezone

# Usado para fazer um and/or
from django.db.models import Q


class TipoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Tipo
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-tipochamado')
    fields = [
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Tipo"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tipochamado'
        return context


class TipoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Tipo
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-tipochamado')
    fields = [
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Tipo"
        context['botao_submit'] = "Salvar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tipochamado'
        return context


class TipoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Tipo
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-tipochamado')

    # Método utilizado para enviar dados ao template
    def get_context_data(self, *args, **kwargs):
        # Chamar o "pai" para que sempre tenha o comportamento padrão, além do nosso
        context = super(TipoDeleteView, self).get_context_data(*args, **kwargs)

        # Adicionar coisas ao contexto que serão enviadas para o html
        context['titulo'] = "Deseja excluir esse registro?"
        context['botao_submit'] = "Excluir"
        context['botao_submit_class'] = "btn-danger"
        context['urlcancelar'] = 'listar-tipochamado'

        # Devolve/envia o context para seu comportamento padrão
        return context


class TipoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Tipo
    template_name = "chamados/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TipoList, self).get_context_data(*args, **kwargs)
        context['colunas'] = [
            'Descrição',
        ]
        context['fields'] = [
            'descricao',
        ]
        context['titulo'] = 'Lista de Tipos cadastrados'
        context['tituloinserir'] = 'Cadastrar Tipo'
        context['urlcadastrar'] = 'cadastrar-tipochamado'
        context['urlalterar'] = 'alterar-tipochamado'
        context['urlexcluir'] = 'excluir-tipochamado'

        return context


class ChamadoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Empresa", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Chamado
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-chamados-abertos')
    fields = [
        'tipo',
        'assunto',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Abrir Chamado"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-chamados-abertos'
        return context

    def form_valid(self, form):
        form.instance.aberto_por = self.request.user
        return super(ChamadoCreateView, self).form_valid(form)


class ChamadoEncerrarUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Chamado
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-chamados-abertos')
    fields = [
        # 'assunto',
        # 'tipo',
        # 'descricao',
        # 'fechado_em',
        # 'fechado_por'
    ]

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):

        # Se for alguém da prefeitura mostra tudo
        # if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
        #     self.object = get_object_or_404(Chamado, pk=self.kwargs['pk'])
        # else:

        # O chamado pra ser fechado tem que ser da empresa e ainda não ter sido fechado
        self.object = get_object_or_404(
            Chamado, pk=self.kwargs['pk'], aberto_por=self.request.user, fechado_em__isnull=True)

        return self.object

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Se fechado da erro
        if self.object.fechado_em and self.object.fechado_por:
            form.add_error(None, 'Este chamado está fechado!')
            return self.form_invalid(form)

        try:
            # Define o usuário como usuário logado
            form.instance.fechado_por = self.request.user
            form.instance.fechado_em = timezone.now()
        except:
            form.add_error(
                None, 'Houve um problema ao encerrar o chamado. Tente novamente em alguns instantes.')
            return self.form_invalid(form)

        return super(ChamadoEncerrarUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoEncerrarUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Encerrar Chamado: #{} {}".format(
            self.object.pk, self.object.assunto)
        context['botao_submit'] = "Sim, quero encerrar!"
        context['botao_submit_class'] = "btn-danger"
        context['urlcancelar'] = 'listar-chamados-abertos'
        return context


class ChamadoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Fiscal", u"Empresa", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Chamado
    template_name = "chamados/list_chamado.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):

        # Se for alguém da prefeitura mostra tudo
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            self.object_list = Chamado.objects.all()
        else:
            self.object_list = Chamado.objects.filter(
                aberto_por=self.request.user)

        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoList, self).get_context_data(*args, **kwargs)
        context['fields'] = [
            'tipo',
            'assunto',
            'descricao',
            'aberto_em',
            'fechado_em',
        ]
        context['titulo'] = 'Lista de Chamados'
        context['tituloinserir'] = 'Abrir Chamado'
        context['urlcadastrar'] = 'cadastrar-chamado'
        context['urldetail'] = 'excluir-tipochamado'

        return context


class ChamadoAbertoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Empresa", u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Chamado
    template_name = "chamados/list_chamado.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):

        # Se for alguém da prefeitura mostra todos abertos
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            self.object_list = Chamado.objects.filter(fechado_em__isnull=True)
        # Se não, só os do usuário
        else:
            self.object_list = Chamado.objects.filter(
                fechado_em__isnull=True, aberto_por=self.request.user)

        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoAbertoList, self).get_context_data(
            *args, **kwargs)
        context['fields'] = [
            'tipo',
            'assunto',
            'descricao',
            'aberto_em',
            'fechado_em',
        ]
        context['titulo'] = 'Lista de Chamados'
        context['tituloinserir'] = 'Abrir Chamado'
        context['urlcadastrar'] = 'cadastrar-chamado'
        context['urldetail'] = 'excluir-tipochamado'

        return context


class ChamadoDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = [u"Fiscal", u"Empresa", u"Prefeitura"]
    login_url = reverse_lazy('login')
    template_name = 'chamados/ver_chamado.html'
    models = Chamado

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):

        # Se for alguém da prefeitura mostra tudo
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            self.object = get_object_or_404(Chamado, pk=self.kwargs['pk'])
        else:
            self.object = get_object_or_404(
                Chamado, pk=self.kwargs['pk'], aberto_por=self.request.user)

        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoDetailView, self).get_context_data(
            *args, **kwargs)

        context['mensagens'] = Mensagem.objects.filter(chamado=self.object)
        return context


class MensagemCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Empresa", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Mensagem
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-chamados-abertos')
    fields = [
        'mensagem'
    ]

    # Busca o chamado na hora que vai abrir o form da mensagem
    def dispatch(self, request, *args, **kwargs):

        # Se for alguém da prefeitura pode comentar qualquer chamado
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            self.chamado = get_object_or_404(
                Chamado, pk=kwargs['chamado_pk'], fechado_em__isnull=True)
        # Se não for, precisa ser um chamado do usuário
        else:
            # Busca o chamado do usuário
            self.chamado = get_object_or_404(
                Chamado, pk=kwargs['chamado_pk'], aberto_por=request.user, fechado_em__isnull=True)

        return super().dispatch(request, *args, **kwargs)

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Se fechado da erro
        if self.chamado.fechado_em:
            form.add_error(None, 'Este chamado está fechado!')
            return self.form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.user = self.request.user
        # Define o chamado dessa mensagem
        form.instance.chamado = self.chamado

        return super(MensagemCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(MensagemCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Comentar chamado #{} {}".format(
            self.chamado.pk, self.chamado.assunto)
        context['botao_submit'] = "Enviar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-chamados-abertos'
        return context


class ChamadoEncerrarComMensagemCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Mensagem
    template_name = 'chamados/form.html'
    success_url = reverse_lazy('listar-chamados-abertos')
    fields = [
        'mensagem'
    ]

    # Busca o chamado na hora que vai abrir o form da mensagem
    def dispatch(self, request, *args, **kwargs):

        # Como é só Fiscal e Prefeitura, pode buscar direto o chamado
        self.chamado = get_object_or_404(
            Chamado, pk=kwargs['chamado_pk'], fechado_em__isnull=True)

        return super().dispatch(request, *args, **kwargs)

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Se fechado da erro
        if self.chamado.fechado_em:
            form.add_error(None, 'Este chamado está fechado!')
            return self.form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.user = self.request.user
        # Define o chamado dessa mensagem
        form.instance.chamado = self.chamado

        # Executa o procedimento padrão para salvar a mensagem
        redirect_url = super(
            ChamadoEncerrarComMensagemCreateView, self).form_valid(form)

        # Fecha o chamado
        self.chamado.fechado_por = self.request.user
        self.chamado.fechado_em = timezone.now()
        self.chamado.save()

        return redirect_url

    def get_context_data(self, *args, **kwargs):
        context = super(ChamadoEncerrarComMensagemCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Comentar e encerrar Chamado #{}: {}".format(
            self.chamado.pk, self.chamado.assunto)
        context['botao_submit'] = "Comentar e encerrar"
        context['botao_submit_class'] = "btn-danger"
        context['urlcancelar'] = 'listar-chamados-abertos'
        return context
