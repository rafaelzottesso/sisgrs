from django import forms

from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .validators import validate_CNPJ

from .models import Empresa, ResiduosSetor, PrestadorServico


class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = [
            'cnpj',
            'razao_social',
            'nome_fantasia',

            'inscricao_estadual',
            'cadastro_imobiliario',
            'cnae',
            'atividade_especifica',

            'cep',
            'endereco',
            'bairro',
            'numero',
            'complemento',

            'telefone_comercial',
            'telefone_celular',
            'email',

            'nome_tecnico',
            'conselho_numero_tecnico',
            'rg_tecnico',
            'cpf_tecnico',
            'telefone_tecnico',
            'email_tecnico',
            'art_num',
            'art_anexo',

            'licenca_iap',
            'num_lincenca',
            'num_protocolo',
            'data_validade',

            'area_construida',
            'descricao_empreendimento',
            'descricao_processo_produtivo',

            'metas_minimizacao',
            'acoes_preventivas',
            # 'responsavel_juridico',

        ]

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtar setor só deste usuário
        # self.fields['responsavel_juridico'].queryset = self.fields['responsavel_juridico'].queryset.filter(
        #     user=user)

        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados Cadastrais',
                Row(
                    Column('cnpj', css_class='form-group col-lg mb-0'),
                    Column('razao_social', css_class='form-group col-lg mb-0'),
                    Column('nome_fantasia', css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Dados gerais, de endereço e de contato',
                Row(
                    Column('inscricao_estadual',
                           css_class='form-group col-lg mb-0'),
                    Column('cadastro_imobiliario',
                           css_class='form-group col-lg mb-0'),
                    Column('cnae', css_class='form-group col-lg mb-0'),
                    Column('atividade_especifica',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cep', css_class='form-group col-lg-2 mb-0'),
                    Column('endereco', css_class='form-group col-lg mb-0'),
                    Column('bairro', css_class='form-group col-lg mb-0'),
                    Column('numero', css_class='form-group col-lg-2 mb-0'),
                    Column('complemento', css_class='form-group col-lg-2 mb-0'),
                ),
                Row(
                    Column('telefone_comercial',
                           css_class='form-group col-lg mb-0'),
                    Column('telefone_celular',
                           css_class='form-group col-lg mb-0'),
                    Column('email', css_class='form-group col-lg-6 mb-0'),
                    css_class='form-row'
                ),
            ),

            Fieldset(
                'Dados do Responsável Técnico da Empresa',
                Row(
                    Column('nome_tecnico', css_class='form-group col-lg-5 mb-0'),
                    Column('rg_tecnico', css_class='form-group col-lg mb-0'),
                    Column('cpf_tecnico', css_class='form-group col-lg mb-0'),
                    Column('conselho_numero_tecnico',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('telefone_tecnico',
                           css_class='form-group col-lg mb-0'),
                    Column('email_tecnico', css_class='form-group col-lg-4 mb-0'),
                    Column('art_num', css_class='form-group col-lg mb-0'),
                    Column('art_anexo', css_class='form-group col-lg-4 mb-0'),
                ),
            ),

            Fieldset(
                'Dados da Licança no IAP',
                Row(
                    Column('licenca_iap', css_class='form-group col-lg mb-0'),
                    Column('num_lincenca', css_class='form-group col-lg mb-0'),
                    Column('num_protocolo', css_class='form-group col-lg mb-0'),
                    Column('data_validade', css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Demais informações sobre a Empresa',
                Row(
                    Column('area_construida',
                           css_class='form-group col-lg-2 mb-0'),
                    Column('descricao_empreendimento',
                           css_class='form-group col-lg mb-0'),
                    Column('descricao_processo_produtivo',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('metas_minimizacao',
                           css_class='form-group col-lg mb-0'),
                    Column('acoes_preventivas',
                           css_class='form-group col-lg mb-0'),
                    # Column('responsavel_juridico',
                    #        css_class='form-group col-lg mb-0'),
                ),
            ),

            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check" aria-hidden="true"></i>
                            Salvar
                        </button>
                    """),
                    HTML("""
                        <a href="#" class="btn btn-secondary btn-cancelar">
                            <i class="fa fa-undo" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class EmpresaFormUpdate(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = [
            # 'cnpj',
            # 'razao_social',
            'nome_fantasia',

            'inscricao_estadual',
            'cadastro_imobiliario',
            'cnae',
            'atividade_especifica',

            'cep',
            'endereco',
            'bairro',
            'numero',
            'complemento',

            'telefone_comercial',
            'telefone_celular',
            'email',

            'nome_tecnico',
            'conselho_numero_tecnico',
            'rg_tecnico',
            'cpf_tecnico',
            'telefone_tecnico',
            'email_tecnico',
            'art_num',
            'art_anexo',

            'licenca_iap',
            'num_lincenca',
            'num_protocolo',
            'data_validade',

            'area_construida',
            'descricao_empreendimento',
            'descricao_processo_produtivo',

            'metas_minimizacao',
            'acoes_preventivas',
            # 'responsavel_juridico',
            # 'user',
        ]

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtar setor só deste usuário
        # self.fields['responsavel_juridico'].queryset = self.fields['responsavel_juridico'].queryset.filter(
        #     user=user)

        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados Cadastrais',
                Row(
                    # Column('cnpj', css_class='form-group col-lg mb-0'),
                    # Column('razao_social', css_class='form-group col-lg mb-0'),
                    Column('nome_fantasia', css_class='form-group col-lg mb-0'),
                    Column('inscricao_estadual',
                           css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Dados gerais, de endereço e de contato',
                Row(
                    Column('cadastro_imobiliario',
                           css_class='form-group col-lg mb-0'),
                    Column('cnae', css_class='form-group col-lg mb-0'),
                    Column('atividade_especifica',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cep', css_class='form-group col-lg-2 mb-0'),
                    Column('endereco', css_class='form-group col-lg mb-0'),
                    Column('bairro', css_class='form-group col-lg mb-0'),
                    Column('numero', css_class='form-group col-lg-2 mb-0'),
                    Column('complemento', css_class='form-group col-lg-2 mb-0'),
                ),
                Row(
                    Column('telefone_comercial',
                           css_class='form-group col-lg mb-0'),
                    Column('telefone_celular',
                           css_class='form-group col-lg mb-0'),
                    Column('email', css_class='form-group col-lg-6 mb-0'),
                    css_class='form-row'
                ),
            ),

            Fieldset(
                'Dados do Responsável Técnico da Empresa',
                Row(
                    Column('nome_tecnico', css_class='form-group col-lg-5 mb-0'),
                    Column('rg_tecnico', css_class='form-group col-lg mb-0'),
                    Column('cpf_tecnico', css_class='form-group col-lg mb-0'),
                    Column('conselho_numero_tecnico',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('telefone_tecnico',
                           css_class='form-group col-lg mb-0'),
                    Column('email_tecnico', css_class='form-group col-lg-4 mb-0'),
                    Column('art_num', css_class='form-group col-lg mb-0'),
                    Column('art_anexo', css_class='form-group col-lg-4 mb-0'),
                ),
            ),

            Fieldset(
                'Dados da Licança no IAP',
                Row(
                    Column('licenca_iap', css_class='form-group col-lg mb-0'),
                    Column('num_lincenca', css_class='form-group col-lg mb-0'),
                    Column('num_protocolo', css_class='form-group col-lg mb-0'),
                    Column('data_validade', css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Demais informações sobre a Empresa',
                Row(
                    Column('area_construida',
                           css_class='form-group col-lg-2 mb-0'),
                    Column('descricao_empreendimento',
                           css_class='form-group col-lg mb-0'),
                    Column('descricao_processo_produtivo',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('metas_minimizacao',
                           css_class='form-group col-lg mb-0'),
                    Column('acoes_preventivas',
                           css_class='form-group col-lg mb-0'),
                    # Column('responsavel_juridico',
                    #        css_class='form-group col-lg mb-0'),
                ),
            ),

            # Somente para desenvolvimento...
            # Fieldset(
            #     'Remover a opção depois!',
            #     Row(
            #         Column('user', css_class='form-group col-lg mb-0'),
            #     ),
            # ),

            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check" aria-hidden="true"></i>
                            Salvar
                        </button>
                    """),
                    HTML("""
                        <a href="#" class="btn btn-secondary btn-cancelar">
                            <i class="fa fa-undo" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class ResiduosSetorForm(forms.ModelForm):

    class Meta:
        model = ResiduosSetor
        fields = [
            'tipo_residuo',
            'setor',

            'residuo',
            'especificar_residuo',

            'estado_fisico',
            'armazenamento',
            'especificar_armazenamento',

            'prestador_servico',
            'destinacao_final',
            'especificar_destinacao_final',

            'volume',
            'unidade_medida',
            'periodicidade_coleta',

            'informacoes_complementares',
        ]
        widgets = {
            'residuo': autocomplete.ModelSelect2(
                url='residuo-autocomplete',
                attrs={
                    # Set some placeholder
                    'data-placeholder': 'Digite o Código ou Descrição para buscar',
                    # Only trigger autocompletion after 3 characters have been typed
                    'data-minimum-input-length': 3,
                },
            ),
            'prestador_servico': autocomplete.ModelSelect2(
                url='prestadorservico-autocomplete',
                attrs={
                    # Set some placeholder
                    'data-placeholder': 'CNPJ, Razão Social ou Nome Fantasia',
                    # Only trigger autocompletion after 3 characters have been typed
                    'data-minimum-input-length': 2,
                },
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtar setor só deste usuário
        self.fields['setor'].queryset = self.fields['setor'].queryset.filter(
            user=user)

        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Informações Gerais',
                Row(
                    Column('tipo_residuo', css_class='form-group col-lg mb-0'),
                    Column('setor', css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Detalhamento do Resíduo',
                Row(
                    Column('residuo', css_class='form-group col-lg mb-0'),
                    Column('especificar_residuo',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('armazenamento', css_class='form-group col-lg mb-0'),
                    Column('especificar_armazenamento',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('prestador_servico',
                           css_class='form-group col-lg mb-0'),
                    Column('destinacao_final',
                           css_class='form-group col-lg mb-0'),
                    Column('especificar_destinacao_final',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('estado_fisico', css_class='form-group col-lg mb-0'),
                    Column('volume', css_class='form-group col-lg-2 mb-0'),
                    Column('unidade_medida',
                           css_class='form-group col-lg-2 mb-0'),
                    Column('periodicidade_coleta',
                           css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('informacoes_complementares',
                           css_class='form-group col-lg mb-0'),
                ),
            ),

            # Fieldset(
            #     'Dados do Responsável Técnico da Empresa',

            # ),

            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check" aria-hidden="true"></i>
                            Salvar
                        </button>
                    """),
                    HTML("""
                        <a href="#" class="btn btn-secondary btn-cancelar">
                            <i class="fa fa-undo" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class UserEmpresaByPrefituraForm(forms.Form):
    cnpj = forms.CharField(max_length=18, label="CNPJ")
    razao_social = forms.CharField(max_length=75, label="Razão Social")
    email = forms.EmailField(max_length=100, label="E-mail")

    # Verifica se o CNPJ já está cadastrado
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']

        # Valida o CNPJ
        validate_CNPJ(cnpj)
        
        if Empresa.objects.filter(cnpj=cnpj).exists():
            raise ValidationError(
                "Já existe uma empresa cadastrada com o CNPJ {}.".format(cnpj))

        return cnpj

    # Valida se o email informado já existe em algum usuário
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "O e-mail {} já está em uso por algum Usuário.".format(email))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Informações da Empresa',
                Row(
                    Column('cnpj', css_class='form-group col-lg mb-0'),
                    Column('razao_social', css_class='form-group col-lg mb-0'),
                ),
            ),

            Fieldset(
                'Dados para Autenticação',
                Row(
                    Column('email', css_class='form-group col-lg mb-0'),
                ),
            ),

            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check" aria-hidden="true"></i>
                            Salvar
                        </button>
                    """),
                    HTML("""
                        <a href="#" class="btn btn-secondary btn-cancelar">
                            <i class="fa fa-undo" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class PrestadorServicoForm(forms.ModelForm):

    class Meta:
        model = PrestadorServico
        fields = [
            'cnpj',
            'razao_social',
            'nome_fantasia',
            'cnae',
            'cep',
            'endereco',
            'bairro',
            'numero',
            'complemento',
            'telefone_comercial',
            'telefone_celular',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados cadastrais e de contato',
                Row(
                    Column('cnpj', css_class='form-group col-lg-3 mb-0'),
                    Column('razao_social', css_class='form-group col-lg mb-0'),
                    Column('nome_fantasia', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cnae', css_class='form-group col-lg mb-0'),
                    Column('telefone_comercial',
                           css_class='form-group col-lg-3 mb-0'),
                    Column('telefone_celular',
                           css_class='form-group col-lg-3 mb-0'),
                ),
            ),
            Fieldset(
                'Endereço eletrônico e local',
                Row(
                    Column('email', css_class='form-group col-lg-6 mb-0'),
                    Column('cep', css_class='form-group col-lg-2 mb-0'),
                    Column('endereco', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('bairro', css_class='form-group col-lg mb-0'),
                    Column('numero', css_class='form-group col-lg-2 mb-0'),
                    Column('complemento', css_class='form-group col-lg mb-0'),
                ),
            ),

            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-primary">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="#" class="btn btn-secondary btn-cancelar">
                                <i class="fa fa-undo" aria-hidden="true"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )

class PrestadorServicoFormUpdate(forms.ModelForm):

    class Meta:
        model = PrestadorServico
        fields = [
            'nome_fantasia',
            'cnae',
            'cep',
            'endereco',
            'bairro',
            'numero',
            'complemento',
            'telefone_comercial',
            'telefone_celular',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados cadastrais e de contato',
                Row(
                    Column('nome_fantasia', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cnae', css_class='form-group col-lg mb-0'),
                    Column('telefone_comercial',
                           css_class='form-group col-lg-3 mb-0'),
                    Column('telefone_celular',
                           css_class='form-group col-lg-3 mb-0'),
                ),
            ),
            Fieldset(
                'Endereço eletrônico e local',
                Row(
                    Column('email', css_class='form-group col-lg-6 mb-0'),
                    Column('cep', css_class='form-group col-lg-2 mb-0'),
                    Column('endereco', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('bairro', css_class='form-group col-lg mb-0'),
                    Column('numero', css_class='form-group col-lg-2 mb-0'),
                    Column('complemento', css_class='form-group col-lg mb-0'),
                ),
            ),

            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-primary">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="#" class="btn btn-secondary btn-cancelar">
                                <i class="fa fa-undo" aria-hidden="true"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )
