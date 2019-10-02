from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.models import User, Group

from planogrs.models import Classe, Residuo, Setor, TipoResiduo, Armazenamento, DestinacaoFinal, ResponsavelJuridico, Cnae, PrestadorServico, Empresa, TipoSituacao, Situacao, ResiduosSetor
from chamados.models import Tipo, Chamado, Mensagem

from django.conf import settings
from django.utils import timezone

from django.shortcuts import get_object_or_404
# Create your views here.


class VisualizarPlanoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = u"Empresa"
    template_name = 'movimentarplano/visualizar_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(VisualizarPlanoView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Visualizar Plano de Gerenciamento de Resíduos Sólidos (Plano GRS)"
        # context['urllista'] = reverse_lazy('listar-empresa')
        context['responsaveis'] = ResponsavelJuridico.objects.filter(
            user=self.request.user)
        context['empresa'] = Empresa.objects.get(user=self.request.user)
        context['setores'] = Setor.objects.filter(user=self.request.user)
        context['residuos'] = ResiduosSetor.objects.filter(
            user=self.request.user)
        context['situacoes'] = Situacao.objects.filter(user=self.request.user)
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()

        return context


class ImprimirPlanoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = u"Empresa"
    template_name = 'movimentarplano/imprimir_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ImprimirPlanoView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Plano de Gerenciamento de Resíduos Sólidos"
        # context['urllista'] = reverse_lazy('listar-empresa')
        context['responsaveis'] = ResponsavelJuridico.objects.filter(
            user=self.request.user)
        context['empresa'] = Empresa.objects.get(user=self.request.user)
        context['setores'] = Setor.objects.filter(user=self.request.user)
        context['residuos'] = ResiduosSetor.objects.filter(
            user=self.request.user)
        context['situacoes'] = Situacao.objects.filter(user=self.request.user)
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()

        return context


class ImprimirDeclaracaoPlanoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = u"Empresa"
    template_name = 'movimentarplano/imprimir_declaracao_situacao.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ImprimirDeclaracaoPlanoView, self).get_context_data(
            *args, **kwargs)

        context['timezone'] = timezone.now()
        context['prefeitura_nome'] = settings.PREFEITURA_NOME
        context['prefeitura_cidade'] = settings.PREFEITURA_CIDADE
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()

        return context


class VisualizarPlanoViewByFiscal(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    template_name = 'movimentarplano/visualizar_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(VisualizarPlanoViewByFiscal, self).get_context_data(
            *args, **kwargs)

        context['titulo'] = "Visualizar Plano de Gerenciamento de Resíduos Sólidos (Plano GRS)"

        # Busca os dados do usuário, desde que ele seja uma empresa
        user = get_object_or_404(
            User, pk=self.kwargs['pk'], groups__name='Empresa')

        if user:
            context['empresa'] = Empresa.objects.get(user=user)
            context['setores'] = Setor.objects.filter(user=user)
            context['residuos'] = ResiduosSetor.objects.filter(
                user=user)
            context['situacoes'] = Situacao.objects.filter(user=user)
            context['situacao_atual'] = Situacao.objects.filter(
                user=user).last()

        return context


#############################################################################


class ListarPlanosGRSView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    template_name = 'movimentarplano/list_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ListarPlanosGRSView, self).get_context_data(
            *args, **kwargs)

        context['titulo'] = "Situação atual dos Planos GRS das Empresas"

        q = self.request.GET.get('q')
        buscar_por = self.request.GET.get('buscar_por')

        termos = ('cnpj', 'razao_social', 'nome_fantasia',
                  'telefone_comercial', 'telefone_celular', 'email')

        if q and buscar_por and buscar_por in termos:
            fields = {
                '{0}__{1}'.format(buscar_por, 'icontains'): q,
            }
            context['empresas'] = Empresa.objects.filter(**fields)
        else:
            context['empresas'] = ''

        if q:
            context['q'] = q

        if buscar_por:
            context['buscar_por'] = buscar_por

        # Lista todos os usuários que são de empresas
        # usuarios = User.objects.filter(groups__name='Empresa')
        # context['usuarios'] = usuarios

        # Cria as listas para armazenar as informações de cada usuário
        context['situacao_atual'] = {}
        context['mostrar_form'] = True

        # Para cada usuário
        for emp in context['empresas']:

            # Dentro de cada lista, cria outras listas com as informações das empresas
            context['situacao_atual'][emp.user.pk] = Situacao.objects.filter(
                user=emp.user).last()

        return context


class ListarPlanosGRSPendentes(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    template_name = 'movimentarplano/list_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ListarPlanosGRSPendentes, self).get_context_data(
            *args, **kwargs)

        context['titulo'] = "Lista de Empresas com Planos GRS 'Pendentes'"

        # Lista todos os usuários que são de empresas
        usuarios = User.objects.filter(groups__name='Empresa')

        # Cria as listas para armazenar as informações de cada usuário
        context['situacao_atual'] = {}
        context['empresas'] = []
        context['busca_situacao'] = 'Pendente'

        # Para cada usuário
        for user in usuarios:

            try:
                situacao = Situacao.objects.filter(user=user).last()

                if situacao.tipo_situacao.nome == "Pendente":
                    # Dentro de cada lista, cria outras listas com as informações das empresas
                    context['situacao_atual'][user.pk] = situacao
                    context['empresas'].append(user.empresa)
            except:
                pass

        return context


class ListarPlanosGRSEmAnalise(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    template_name = 'movimentarplano/list_planogrs.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ListarPlanosGRSEmAnalise, self).get_context_data(
            *args, **kwargs)

        context['titulo'] = "Lista de Empresas com Planos GRS 'Em análise'"

        # Lista todos os usuários que são de empresas
        usuarios = User.objects.filter(groups__name='Empresa')

        # Cria as listas para armazenar as informações de cada usuário
        context['situacao_atual'] = {}
        context['empresas'] = []
        context['busca_situacao'] = 'Em análise'

        # Para cada usuário
        for user in usuarios:

            situacao = Situacao.objects.filter(user=user).last()
            try:
                if situacao.tipo_situacao.nome == "Em análise":
                    # Dentro de cada lista, cria outras listas com as informações das empresas
                    context['situacao_atual'][user.pk] = situacao
                    context['empresas'].append(user.empresa)
            except:
                pass

        return context

#############################################################################


class SubmeterPlanoByEmpresa(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'movimentarplano/form.html'
    success_url = reverse_lazy('listar-situacao')
    fields = [
        # 'user',
        # 'tipo_situacao',
        'informacoes_complementares',
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):
        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome == "Em adequação" or situacao_atual.tipo_situacao.nome == "Andamento inicial":
            form.instance.user = self.request.user
            form.instance.movimentado_por = self.request.user
            form.instance.tipo_situacao = TipoSituacao.objects.get(
                nome='Pendente')
            return super(SubmeterPlanoByEmpresa, self).form_valid(form)
        # Se não, dê um erro
        else:
            form.add_error(None, 'Você não pode movimentar seu Plano GRS porque ele está "{}"!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(SubmeterPlanoByEmpresa, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Submeter Plano de Gerenciamento de Resíduos Sólidos"
        context['botao_submit'] = "Submeter"
        context['botao_submit_class'] = "btn-success"
        context['urlcancelar'] = 'index-auth'
        context['usuario'] = self.request.user
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        context['mostrarform'] = True if context['situacao_atual'].tipo_situacao.nome == "Em adequação" or context[
            'situacao_atual'].tipo_situacao.nome == "Andamento inicial" else False
        return context


class AnalisarPlanoGRS(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'movimentarplano/form.html'
    success_url = reverse_lazy('listar-planogrs-emanalise')
    fields = [
        # 'user',
        # 'tipo_situacao',
        'informacoes_complementares',
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):
        # Busca informações do usuário
        user = User.objects.get(pk=self.kwargs['pk'])
        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=user).last()
        # Se for pendente pode movimentar
        if situacao_atual.tipo_situacao.nome == "Pendente":
            form.instance.user = user
            form.instance.movimentado_por = self.request.user
            form.instance.tipo_situacao = TipoSituacao.objects.get(
                nome='Em análise')
            return super(AnalisarPlanoGRS, self).form_valid(form)
        # Se não, dê um erro
        else:
            form.add_error(None, 'Você está tentando alterar o Plano GRS da Empresa {} para "Em análise". Porém, atualmente ele está: "{}".'.format(
                user.empresa.razao_social, situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AnalisarPlanoGRS, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Enviar Plano de Gerenciamento de Resíduos Sólidos para Análise"
        context['botao_submit'] = "Enviar Plano GRS para Análise"
        context['botao_submit_class'] = "btn-warning"
        context['urlcancelar'] = 'index-auth'
        context['usuario'] = User.objects.get(pk=self.kwargs['pk'])
        context['situacao_atual'] = Situacao.objects.filter(
            user=context['usuario']).last()
        # Recebe True se a situação atual bater com a condição
        context['mostrarform'] = True if context['situacao_atual'].tipo_situacao.nome == "Pendente" else False

        return context


class AdequarPlanoGRS(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'movimentarplano/form.html'
    success_url = reverse_lazy('listar-planogrs')
    fields = [
        # 'user',
        # 'tipo_situacao',
        'informacoes_complementares',
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):
        # Busca informações do usuário
        user = User.objects.get(pk=self.kwargs['pk'])
        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=user).last()
        # Se for em análise pode alterar ele
        if situacao_atual.tipo_situacao.nome == "Em análise" or situacao_atual.tipo_situacao.nome == "Aprovado":
            form.instance.user = user
            form.instance.movimentado_por = self.request.user
            form.instance.tipo_situacao = TipoSituacao.objects.get(
                nome='Em adequação')
            return super(AdequarPlanoGRS, self).form_valid(form)
        # Se não, dê um erro
        else:
            form.add_error(None, 'Você está tentando alterar o Plano GRS da Empresa {} para "Em adequação". Porém, atualmente ele está: "{}".'.format(
                user.empresa.razao_social, situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AdequarPlanoGRS, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Enviar Plano de Gerenciamento de Resíduos Sólidos para Adequação"
        context['botao_submit'] = "Solicitar Adequação do Plano"
        context['botao_submit_class'] = "btn-danger"
        context['urlcancelar'] = 'index-auth'
        context['usuario'] = User.objects.get(pk=self.kwargs['pk'])
        context['situacao_atual'] = Situacao.objects.filter(
            user=context['usuario']).last()
        # Recebe True se a situação atual bater com a condição
        situacao = context['situacao_atual'].tipo_situacao.nome
        context['mostrarform'] = True if (
            situacao == "Em análise" or situacao == "Aprovado") else False

        return context


class AdequarPlanoGRSPorChamado(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'movimentarplano/form.html'
    success_url = reverse_lazy('listar-chamados-abertos')
    fields = [
        # 'user',
        # 'tipo_situacao',
        'informacoes_complementares',
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):
        # Busca informações do usuário
        user = User.objects.get(pk=self.kwargs['pk'])
        chamado = get_object_or_404(
            Chamado, pk=self.kwargs['pk_chamado'], aberto_por=user, tipo__descricao="Liberação de cadastros", fechado_em__isnull=True)

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=user).last()

        # Se for em análise pode alterar ele
        if situacao_atual.tipo_situacao.nome == "Pendente" or situacao_atual.tipo_situacao.nome == "Em análise" or situacao_atual.tipo_situacao.nome == "Aprovado":
            form.instance.user = user
            form.instance.movimentado_por = self.request.user
            form.instance.tipo_situacao = TipoSituacao.objects.get(
                nome='Em adequação')
            # Altera o plano para adequação
            redirect_url = super(AdequarPlanoGRSPorChamado,
                                 self).form_valid(form)
            # Cria uma mensagem para o Chamado
            comentario = "Chamado encerrado porque o Plano GRS foi alterado para Adequação e os cadastros foram liberados."
            mensagem = Mensagem.objects.create(
                chamado=chamado, user=self.request.user, mensagem=comentario)
            # Coloca o usuário e a data de agora para fechar o chamado
            chamado.fechado_em = timezone.now()
            chamado.fechado_por = self.request.user
            chamado.save()

            return redirect_url

        # Se não, dê um erro
        else:
            form.add_error(None, 'Você está tentando alterar o Plano GRS da Empresa {} para "Em adequação" devido o Chamado #{}. Porém, o Plano GRS da Empresa já está liberado para alterações.'.format(
                user.empresa.razao_social, self.kwargs['pk_chamado']))
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AdequarPlanoGRSPorChamado, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Chamado #{} - Liberação de cadastros".format(
            self.kwargs['pk_chamado'])
        context['botao_submit'] = "Alterar Plano GRS para Adequação"
        context['botao_submit_class'] = "btn-warning"
        context['urlcancelar'] = 'index-auth'
        context['usuario'] = User.objects.get(pk=self.kwargs['pk'])
        context['situacao_atual'] = Situacao.objects.filter(
            user=context['usuario']).last()

        # Recebe True se a situação atual bater com a condição
        user = User.objects.get(pk=self.kwargs['pk'])
        chamado = get_object_or_404(
            Chamado, pk=self.kwargs['pk_chamado'], aberto_por=user, tipo__descricao="Liberação de cadastros", fechado_em__isnull=True)
        context['chamado'] = chamado
        if chamado:
            context['mostrarform'] = True
        else:
            context['mostrarform'] = False
        context['informacoes_comp'] = "Plano GRS alterado para Adequação por causa do Chamado #{} de Liberação de cadastros.".format(
            self.kwargs['pk_chamado'])

        return context


class AprovarPlanoGRS(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Fiscal", u"Prefeitura"]
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'movimentarplano/form.html'
    success_url = reverse_lazy('listar-planogrs')
    fields = [
        # 'user',
        # 'tipo_situacao',
        'informacoes_complementares',
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):
        # Busca informações do usuário
        user = User.objects.get(pk=self.kwargs['pk'])
        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=user).last()
        # Se for Em análise pode movimentar
        if situacao_atual.tipo_situacao.nome == "Em análise":
            form.instance.user = user
            form.instance.movimentado_por = self.request.user
            form.instance.tipo_situacao = TipoSituacao.objects.get(
                nome='Aprovado')
            return super(AprovarPlanoGRS, self).form_valid(form)
        # Se não, dê um erro
        else:
            form.add_error(None, 'Você está tentando alterar o Plano GRS da Empresa {} para "Aprovado". Porém, atualmente ele está: "{}".'.format(
                user.empresa.razao_social, situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AprovarPlanoGRS, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Aprovar o Plano de Gerenciamento de Resíduos Sólidos"
        context['botao_submit'] = "Aprovar o Plano GRS"
        context['botao_submit_class'] = "btn-success"
        context['urlcancelar'] = 'index-auth'
        context['usuario'] = User.objects.get(pk=self.kwargs['pk'])
        context['situacao_atual'] = Situacao.objects.filter(
            user=context['usuario']).last()
        # Recebe True se a situação atual bater com a condição
        context['mostrarform'] = True if context['situacao_atual'].tipo_situacao.nome == "Em análise" else False

        return context
