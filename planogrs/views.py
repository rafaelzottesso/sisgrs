from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import ListView

from .models import Classe, Residuo, Setor, TipoResiduo, Armazenamento, DestinacaoFinal, ResponsavelJuridico, Cnae, PrestadorServico, Empresa, TipoSituacao, Situacao, ResiduosSetor
from chamados.models import Chamado

from django.contrib.auth.models import User, Group

from .forms import EmpresaForm, EmpresaFormUpdate, ResiduosSetorForm, UserEmpresaByPrefituraForm, PrestadorServicoForm, PrestadorServicoFormUpdate

from django.shortcuts import get_object_or_404

# Usado para fazer um and/or
from django.db.models import Q


class IndexView(TemplateView):
    template_name = "planogrs/base.html"


class SobreView(TemplateView):
    template_name = "planogrs/sobre.html"


class AjudaView(TemplateView):
    template_name = "planogrs/ajuda.html"


class IndexAutenticadoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "planogrs/index_auth.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexAutenticadoView, self).get_context_data(
            *args, **kwargs)

        # if self.request.user.groups.filter( Q(name='Fiscal') | Q(name='Prefeitura') ).exists():
        #     context['empresas'] = Empresa.objects.all().count()
        #     context['prestadores'] = PrestadorServico.objects.all().count()

        if self.request.user.groups.filter(name='Empresa').exists():
            context['responsaveis'] = ResponsavelJuridico.objects.filter(
                user=self.request.user).count()
            context['setores'] = Setor.objects.filter(
                user=self.request.user).count()
            context['residuos'] = ResiduosSetor.objects.filter(
                user=self.request.user).count()
            context['situacao_atual'] = Situacao.objects.filter(
                user=self.request.user).last()
        
        elif self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            
            context['chamados'] = Chamado.objects.filter(
                fechado_em__isnull=True).count()

        return context


class DownloadFileView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')

    # O template não importa porque ele vai fazer download
    template_name = "planogrs/download_file.html"

    # Sobrescreve o método que gera a resposta à solicitação HTTP
    def dispatch(self, *args, **kwargs):

        # Verifica se usuário está logado
        if self.request.user.is_authenticated:

            # Verifica se o ID do usuário é igual o que está na URL
            if (self.request.user.pk == self.kwargs['pk']) or (self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists()):

                # Importa biblioteca os
                import os
                # Gera o caminho do arquivo local: .../uploads/1/arquivo.xxx
                file_path = os.path.join(settings.MEDIA_ROOT, str(
                    self.kwargs['pk']), self.kwargs['file'])

                # Verifica se o arquivo existe
                if os.path.exists(file_path):

                    # Abre, faz a leitura do arquivo e prepara o conteúdo prepara para download
                    with open(file_path, 'rb') as pdf:

                        # Para arquivos PDF
                        if file_path[-4:] == ".pdf":
                            response = HttpResponse(
                                pdf.read(), content_type='application/pdf')
                        # Para outros formatos (acho que não vamos precisar, mas...)
                        else:
                            response = HttpResponse(
                                pdf.read(), content_type="application/vnd.ms-excel")

                        # Formata esta informação no cabeçalho da requisição
                        response['Content-Disposition'] = 'inline; filename=' + \
                            os.path.basename(file_path)

                        # Fecha o arquivo
                        pdf.closed

                        # Retorna a requisição com o arquivo
                        return response

        # Da um Erro 404
        raise Http404


class ClasseCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    redirect_field_name = 'login'

    model = Classe
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-classe')
    fields = [
        'nome',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ClasseCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Classe"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-classe'
        return context


class ClasseUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Classe
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-classe')
    fields = [
        'nome',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ClasseUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Classe"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-classe'
        return context


class ClasseList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Classe
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ClasseList, self).get_context_data(*args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Nome',
            'Descrição',
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'nome',
            'descricao',
        ]

        # Título da página
        context['titulo'] = 'Lista de Classes cadastradas'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Classe'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-classe'
        context['urlalterar'] = 'alterar-classe'
        context['urlexcluir'] = 'excluir-classe'

        return context


class ClasseDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Classe
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-classe')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-classe'
        context['botao_submit'] = 'Deletar'
        return context


########################################################################


class ResiduoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Residuo
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-residuo')
    fields = [
        'codigo',
        'descricao',
        'classificacao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Residuo"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-residuo'
        return context


class ResiduoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Residuo
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-residuo')
    fields = [
        'codigo',
        'descricao',
        'classificacao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Residuo"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-residuo'
        return context


class ResiduoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Residuo
    template_name = "planogrs/list_residuo.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduoList, self).get_context_data(*args, **kwargs)

        # Título da página
        context['titulo'] = 'Lista de Residuos cadastradas'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Residuo'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-residuo'
        context['urlalterar'] = 'alterar-residuo'
        context['urlexcluir'] = 'excluir-residuo'

        return context

class ResiduoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Residuo
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-residuo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-residuo'
        context['botao_submit'] = 'Deletar'
        return context

############################################################################


class SetorCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Setor
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-setor')
    fields = [
        # 'user',
        'nome',
        'informacoes_complementares'
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.user = self.request.user
        return super(SetorCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(SetorCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Setor"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-setor'
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class SetorUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Setor
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-setor')
    fields = [
        'nome',
        'informacoes_complementares'
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Valida o formulário normalmente...
        return super(SetorUpdateView, self).form_valid(form)

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Setor, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(SetorUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Setor"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-setor'
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class SetorList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Setor
    template_name = "planogrs/list_base.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):
        # O Visual acusa erro, mas está correto! Classe.objects.filter(...)
        self.object_list = Setor.objects.filter(user=self.request.user)
        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SetorList, self).get_context_data(*args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            # 'Empresa',
            'Nome',
            'Informações Complementares'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            # 'user',
            'nome',
            'informacoes_complementares'
        ]

        # Título da página
        context['titulo'] = 'Lista de Setores cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Setor'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-setor'
        context['urlalterar'] = 'alterar-setor'
        context['urlexcluir'] = 'excluir-setor'

        return context


class SetorDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Setor
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-setor')

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Setor, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-setor'
        context['botao_submit'] = 'Deletar'
        return context



###############################################################################


class TipoResiduoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoResiduo
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-tiporesiduo')
    fields = [
        'nome',
        'informacoes_complementares'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoResiduoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Tipo de Resíduo"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tiporesiduo'
        return context


class TipoResiduoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoResiduo
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-tiporesiduo')
    fields = [
        'nome',
        'informacoes_complementares'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoResiduoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Tipo de Resíduo"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tiporesiduo'
        return context


class TipoResiduoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoResiduo
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TipoResiduoList, self).get_context_data(
            *args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Nome',
            'Informações Complementares'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'nome',
            'informacoes_complementares'
        ]

        # Título da página
        context['titulo'] = 'Lista de Tipos de Resíduos cadastradas'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Tipo'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-tiporesiduo'
        context['urlalterar'] = 'alterar-tiporesiduo'
        context['urlexcluir'] = 'excluir-tiporesiduo'

        return context


class TipoResiduoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoResiduo
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-tiporesiduo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-tiporesiduo'
        context['botao_submit'] = 'Deletar'
        return context

############################################################################


class ArmazenamentoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Armazenamento
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-armazenamento')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ArmazenamentoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Armazenamento"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-armazenamento'
        return context


class ArmazenamentoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Armazenamento
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-armazenamento')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(ArmazenamentoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Armazenamento"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-armazenamento'
        return context


class ArmazenamentoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Armazenamento
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArmazenamentoList, self).get_context_data(
            *args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Código',
            'Descrição'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'codigo',
            'descricao'
        ]
        # Título da página
        context['titulo'] = 'Lista de Armazenamentos cadastradas'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Armazenamento'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-armazenamento'
        context['urlalterar'] = 'alterar-armazenamento'
        context['urlexcluir'] = 'excluir-armazenamento'

        return context


class ArmazenamentoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Armazenamento
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-armazenamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-armazenamento'
        context['botao_submit'] = 'Deletar'
        return context

##########################################################################


class DestinacaoFinalCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = DestinacaoFinal
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-destinacaofinal')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(DestinacaoFinalCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Destinação Final"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-destinacaofinal'
        return context


class DestinacaoFinalUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = DestinacaoFinal
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-destinacaofinal')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(DestinacaoFinalUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Destinação Final"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-destinacaofinal'
        return context


class DestinacaoFinalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = DestinacaoFinal
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DestinacaoFinalList, self).get_context_data(
            *args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Código',
            'Descrição'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'codigo',
            'descricao'
        ]
        # Título da página
        context['titulo'] = 'Lista de Destinacões Finais cadastradas'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Destinação Final'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-destinacaofinal'
        context['urlalterar'] = 'alterar-destinacaofinal'
        context['urlexcluir'] = 'excluir-destinacaofinal'

        return context


class DestinacaoFinalDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = DestinacaoFinal
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-destinacaofinal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-destinacaofinal'
        context['botao_submit'] = 'Deletar'
        return context

################################################################################


class ResponsavelJuridicoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResponsavelJuridico
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-responsaveljuridico')
    fields = [
        # 'user',
        'nome',
        'rg',
        'cpf',
        'telefone',
        'email',
        'cargo'
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.user = self.request.user
        return super(ResponsavelJuridicoCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ResponsavelJuridicoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Responsavel Juridico"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-responsaveljuridico'
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class ResponsavelJuridicoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResponsavelJuridico
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-responsaveljuridico')
    fields = [
        # 'user',
        'nome',
        'rg',
        'cpf',
        'telefone',
        'email',
        'cargo'
    ]

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Valida o formulário normalmente...
        return super(ResponsavelJuridicoUpdateView, self).form_valid(form)

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            ResponsavelJuridico, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(ResponsavelJuridicoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Responsavel Juridico"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-responsaveljuridico'
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class ResponsavelJuridicoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResponsavelJuridico
    template_name = "planogrs/list_base.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):
        # O Visual acusa erro, mas está correto! Classe.objects.filter(...)
        self.object_list = ResponsavelJuridico.objects.filter(
            user=self.request.user)
        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(ResponsavelJuridicoList, self).get_context_data(
            *args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Nome',
            'RG',
            'CPF',
            'Cargo'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'nome',
            'rg',
            'cpf',
            'cargo',
        ]
        # Título da página
        context['titulo'] = 'Lista de Responsáveis Jurídicos cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Responsável Jurídico'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-responsaveljuridico'
        context['urlalterar'] = 'alterar-responsaveljuridico'
        context['urlexcluir'] = 'excluir-responsaveljuridico'

        return context

class ResponsavelJuridicoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResponsavelJuridico
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-responsaveljuridico')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            ResponsavelJuridico, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-responsaveljuridico'
        context['botao_submit'] = 'Deletar'
        return context



#######################################################################################


class CnaeCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Cnae
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-cnae')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(CnaeCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Cnae"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-cnae'
        return context


class CnaeUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Cnae
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-cnae')
    fields = [
        'codigo',
        'descricao'
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(CnaeUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Cnae"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-cnae'
        return context


class CnaeList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Cnae
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CnaeList, self).get_context_data(
            *args, **kwargs)

        context['colunas'] = [
            'Código',
            'Descrição'
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'codigo',
            'descricao'
        ]
        # Título da página
        context['titulo'] = 'Lista de CNAEs cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Novo CNAE'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-cnae'
        context['urlalterar'] = 'alterar-cnae'
        context['urlexcluir'] = 'excluir-cnae'

        return context


class CnaeDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Cnae
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-cnae')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-cnae'
        context['botao_submit'] = 'Deletar'
        return context

###############################################################################


class PrestadorServicoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Prefeitura", u"Fiscal"]
    template_name = 'planogrs/form_crispy.html'
    model = PrestadorServico
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('listar-prestadorservico')
    form_class = PrestadorServicoForm

    def get_context_data(self, *args, **kwargs):
        context = super(PrestadorServicoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar novo Prestador de Serviço"
        context['urllista'] = reverse_lazy('listar-prestadorservico')
        return context


class PrestadorServicoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Prefeitura", u"Fiscal"]
    template_name = 'planogrs/form_crispy.html'
    model = PrestadorServico
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('listar-prestadorservico')
    form_class = PrestadorServicoFormUpdate

     

    def get_context_data(self, *args, **kwargs):
        context = super(PrestadorServicoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar dados do Prestador de Serviço"
        context['urllista'] = reverse_lazy('listar-prestadorservico')
        return context


class PrestadorServicoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Prefeitura", u"Fiscal"]
    login_url = reverse_lazy('login')
    model = PrestadorServico
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PrestadorServicoList, self).get_context_data(
            *args, **kwargs)
    # Define o título de cada coluna na tabela
        context['colunas'] = [
            'CNPJ',
            'Razão Social',
            'Nome fantasia',
            # 'CNAE',
            'CEP',
            # 'Número',
            'Telefone',
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'cnpj',
            'razao_social',
            'nome_fantasia',
            # 'cnae',
            'cep',
            # 'numero',
            'telefone_comercial',
        ]
        # Título da página
        context['titulo'] = 'Lista de Prestadores de Serviço cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Prestador de Serviço'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-prestadorservico'
        context['urlalterar'] = 'alterar-prestadorservico'
        context['urlexcluir'] = 'excluir-prestadorservico'

        return context


class PrestadorServicoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = PrestadorServico
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-prestadorservico')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-prestadorservico'
        context['botao_submit'] = 'Deletar'
        return context


################################################################################


class TipoSituacaoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoSituacao
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-tiposituacao')
    fields = [
        'nome',
        'pode_alterar_cadastros',
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoSituacaoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Tipo de Situação"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tiposituacao'
        return context


class TipoSituacaoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoSituacao
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-tiposituacao')
    fields = [
        'nome',
        'pode_alterar_cadastros',
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(TipoSituacaoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Tipo de Situação"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-tiposituacao'
        return context


class TipoSituacaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = TipoSituacao
    template_name = "planogrs/list_base.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TipoSituacaoList, self).get_context_data(
            *args, **kwargs)

        # Define o título de cada coluna na tabela
        context['colunas'] = [
            'Nome',
            'Permitir alteração nos cadastros?',
        ]
        # Define quais campos serão listados na tebela
        context['fields'] = [
            'nome',
            'pode_alterar_cadastros',
        ]
        # Título da página
        context['titulo'] = 'Lista de Tipos de Situações cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Tipo de Situação'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-tiposituacao'
        context['urlalterar'] = 'alterar-tiposituacao'
        context['urlexcluir'] = 'alterar-tiposituacao'

        return context


##################################################################################


class SituacaoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-situacao')
    fields = [
        'user',
        'tipo_situacao',
        'informacoes_complementares',
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(SituacaoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar Situação"
        context['botao_submit'] = "Cadastrar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-situacao'
        return context


class SituacaoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'planogrs/form_base.html'
    success_url = reverse_lazy('listar-situacao')
    fields = [
        'user',
        'tipo_situacao',
        'informacoes_complementares',
    ]

    def get_context_data(self, *args, **kwargs):
        context = super(SituacaoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Alterar Situação"
        context['botao_submit'] = "Alterar"
        context['botao_submit_class'] = "btn-primary"
        context['urlcancelar'] = 'listar-situacao'
        return context


class SituacaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Prefeitura", u"Fiscal", u"Empresa"]
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = "planogrs/list_situacao.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):
        # Se for alguém da prefeitura mostra tudo
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            self.object_list = Situacao.objects.all().order_by("-data_movimentacao")
        else:
            self.object_list = Situacao.objects.filter(
                user=self.request.user).order_by("-data_movimentacao")

        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SituacaoList, self).get_context_data(
            *args, **kwargs)

        # Título da página
        context['titulo'] = 'Histórico de Movimentações'

        # Título dos botão cadastrar
        # context['tituloinserir'] = 'Cadastrar Situação'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-situacao'
        context['urlalterar'] = 'alterar-situacao'
        context['urlexcluir'] = 'alterar-situacao'

        return context


##################################################################################


class EmpresaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Prefeitura"
    login_url = reverse_lazy('login')
    model = Empresa
    template_name = 'planogrs/form_crispy.html'
    success_url = reverse_lazy('listar-empresa')
    form_class = EmpresaForm

    def get_context_data(self, *args, **kwargs):
        context = super(EmpresaCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar nova Empresa"
        context['urllista'] = reverse_lazy('listar-empresa')
        return context


class EmpresaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = Empresa
    template_name = 'planogrs/form_crispy.html'
    success_url = reverse_lazy('listar-empresa')
    form_class = EmpresaFormUpdate

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Valida o formulário normalmente...
        return super(EmpresaUpdateView, self).form_valid(form)

    # Para passar o usuário logado no forms para aplicar filtros
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        # Assim, o admin não é permitido alterar Empresa
        self.object = get_object_or_404(
            Empresa, pk=self.kwargs['pk'], user=self.request.user)
        
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(EmpresaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Atualizar dados da Empresa"
        context['urllista'] = reverse_lazy('listar-empresa')
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class EmpresaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Prefeitura", u"Empresa", u"Fiscal"]
    login_url = reverse_lazy('login')
    model = Empresa
    template_name = "planogrs/list_empresa.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):

        # Se for alguém da prefeitura mostra tudo
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            q = self.request.GET.get('q')
            buscar_por = self.request.GET.get('buscar_por')

            termos = ('cnpj', 'razao_social', 'nome_fantasia',
                      'telefone_comercial', 'telefone_celular', 'email')

            if q and buscar_por and buscar_por in termos:
                
                kwargs = {
                    '{0}__{1}'.format(buscar_por, 'icontains'): q,
                }

                self.object_list = Empresa.objects.filter(**kwargs)
            else:
                self.object_list = ''

        # Se for um usuário comum...
        else:
            self.object_list = Empresa.objects.filter(user=self.request.user)

        return self.object_list

    # Envia alguns dados para o template
    def get_context_data(self, *args, **kwargs):
        context = super(EmpresaList, self).get_context_data(*args, **kwargs)

        # Título da página
        if self.request.user.groups.filter(Q(name='Fiscal') | Q(name='Prefeitura')).exists():
            context['titulo'] = 'Lista de Empresas cadastradas'
        else:
            context['titulo'] = 'Minha Empresa'

        # Título dos botão cadastrar
        # context['tituloinserir'] = 'Cadastrar Empresa'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        # context['urlcadastrar'] = 'cadastrar-empresa'
        context['urlalterar'] = 'alterar-empresa'
        context['urlexcluir'] = 'alterar-empresa'

        # Lista de Tipos de situação
        context['situacoes'] = TipoSituacao.objects.all()

        context['urlexcluir'] = 'alterar-empresa'

        return context


#############################################################################


class ResiduosSetorCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResiduosSetor
    template_name = 'planogrs/form_crispy.html'
    success_url = reverse_lazy('listar-residuossetor')
    form_class = ResiduosSetorForm

    # Para passar o usuário logado no forms para aplicar filtros
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Define o usuário como usuário logado
        form.instance.user = self.request.user
        return super(ResiduosSetorCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduosSetorCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar novo Resíduo por Setor"
        context['urllista'] = reverse_lazy('listar-residuossetor')
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class ResiduosSetorUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResiduosSetor
    template_name = 'planogrs/form_crispy.html'
    success_url = reverse_lazy('listar-residuossetor')
    form_class = ResiduosSetorForm

    # Sobrescreve o método de validação do formulário
    def form_valid(self, form):

        # Verifica a última situação do plano
        situacao_atual = Situacao.objects.filter(user=self.request.user).last()
        # Se for Em adequação ou andamento inicial, a empresa pode movimentar
        if situacao_atual.tipo_situacao.nome != "Em adequação" and situacao_atual.tipo_situacao.nome != "Andamento inicial":
            form.add_error(None, 'Você não pode inserir ou alterar seus cadastros porque seu Plano GRS está {}!'.format(
                situacao_atual.tipo_situacao.nome))
            return self.form_invalid(form)

        # Valida o formulário normalmente...
        return super(ResiduosSetorUpdateView, self).form_valid(form)

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            ResiduosSetor, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    # Para passar o usuário logado no forms para aplicar filtros
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduosSetorUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Atualizar cadastro de Resíduo por Setor"
        context['urllista'] = reverse_lazy('listar-residuossetor')
        context['situacao_atual'] = Situacao.objects.filter(
            user=self.request.user).last()
        return context


class ResiduosSetorList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResiduosSetor
    template_name = "planogrs/list_residuossetor.html"

    # Altera a query padrão para buscar somente dados do usuário logado
    def get_queryset(self):
        # O Visual acusa erro, mas está correto! Classe.objects.filter(...)
        self.object_list = ResiduosSetor.objects.filter(user=self.request.user)
        return self.object_list

    def get_context_data(self, *args, **kwargs):
        context = super(ResiduosSetorList, self).get_context_data(
            *args, **kwargs)

        # Título da página
        context['titulo'] = 'Lista de Resíduos por Setor cadastrados'

        # Título dos botão cadastrar
        context['tituloinserir'] = 'Cadastrar Resíduo por Setor'

        # Nome da URL que vai nos botões cadastrar/alterar/excluir
        context['urlcadastrar'] = 'cadastrar-residuossetor'
        context['urlalterar'] = 'alterar-residuossetor'
        context['urlexcluir'] = 'excluir-residuossetor'

        return context


class ResiduosSetorDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Empresa"
    login_url = reverse_lazy('login')
    model = ResiduosSetor
    template_name = 'planogrs/delete.html'
    success_url = reverse_lazy('listar-residuossetor')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            ResiduosSetor, pk=self.kwargs['pk'], user=self.request.user)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Exclusão de Registros'
        context['urlcancelar'] = 'listar-residuossetor'
        context['botao_submit'] = 'Deletar'
        return context



#############################################################################


class UserAndEmpresaByPrefeituraCreateForm(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Prefeitura", u"Fiscal"]
    template_name = 'planogrs/form_crispy.html'
    form_class = UserEmpresaByPrefituraForm
    success_url = reverse_lazy('listar-empresa')
    login_url = reverse_lazy('login')

    def form_valid(self, form):

        try:
            # importa para gerar uma senha aleatória e remover máscara do cnpj
            import random
            import string
            import re

            cnpj = form.cleaned_data['cnpj']
            razao_social = form.cleaned_data['razao_social']
            email = form.cleaned_data['email']

            # Deixa só os números
            usuario = re.sub("[^0-9]", '', cnpj)

            # Cria uma "biblioteca" de letras e números
            password_characters = string.ascii_letters + \
                string.digits + string.ascii_letters.upper()
            # Pega caracteres aleatórios da biblioteca acima - 8 caracteres
            senha = ''.join(random.choice(password_characters)
                            for i in range(8))

        except:
            form.add_error(None, 'Erro ao validar os dados.')
            return self.form_invalid(form)

        # Tenta criar um usuário
        try:
            user = User.objects.create_user(usuario, email, senha)
            # Adicionar grupos de parceiros
            grupo = Group.objects.get(name='Empresa')
            user.groups.add(grupo)
        except:
            form.add_error(None, 'Erro ao tentar cadastrar esse usuário.')
            return self.form_invalid(form)

        # Tenta criar uma empresa
        try:
            empresa = Empresa.objects.create(
                user=user,
                cnpj=cnpj,
                razao_social=razao_social,
                nome_fantasia='',
                cadastro_imobiliario='',
                cep='',
                endereco='',
                bairro='',
                numero='',
                telefone_comercial='',
                telefone_celular='',
                email=email,
                nome_tecnico='',
                conselho_numero_tecnico='',
                rg_tecnico='',
                cpf_tecnico='',
                telefone_tecnico='',
                email_tecnico='',
                art_num='',
                art_anexo='',
                licenca_iap='',
                area_construida='',
                descricao_empreendimento=''
            )
        except:
            form.add_error(None, "Erro ao tentar cadastar uma empresa.")
            user.delete()
            return self.form_invalid(form)

        # Coloca a situação em Andamento inicial
        try:
            tipo_situacao = TipoSituacao.objects.get(nome="Andamento inicial")
            situacao = Situacao.objects.create(
                user=user,
                movimentado_por=self.request.user,
                tipo_situacao=tipo_situacao,
                informacoes_complementares='Cadastro da empresa e do usuário realizados na Prefeitura.'
            )
        except:
            form.add_error(None, "Erro ao cadastrar a situação inicial.")
            empresa.delete()
            user.delete()
            return self.form_invalid(form)


        # Envia email para usuário com sua senha
        try:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string

            subject = "[SisGRS] Cadastro de usuário"
            message = render_to_string('planogrs/email/registro_texto_email.html', {
                'usuario': usuario,
                'cnpj': cnpj,
                'razao_social': razao_social,
                'senha': senha,
                'prefeitura_nome': settings.PREFEITURA_NOME,
                'prefeitura_fone': settings.PREFEITURA_FONE,
                'prefeitura_endereco': settings.PREFEITURA_ENDERECO,
                'dominio': self.request.META['HTTP_HOST'],
            })
            from_email = settings.EMAIL_HOST_USER

            if subject and message and from_email:
                send_mail(subject, message, from_email, [email])

        except:
            pass
            # form.add_error(None, 'O cadastro foi realizado com sucesso, porém houve um erro ao enviar um email com a senha para {}. Você pode sair desta página e o usuário pode solicitar uma nova senha na página de login.'.format(email))
            # return self.form_invalid(form)

        # Se tudo ocorreu bem, finaliza
        return super(UserAndEmpresaByPrefeituraCreateForm, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(UserAndEmpresaByPrefeituraCreateForm, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = "Cadastrar nova Empresa"
        context['urllista'] = reverse_lazy('listar-empresa')
        return context


#############################################################################
