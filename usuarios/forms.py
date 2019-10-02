from django import forms
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML
from django.contrib.auth.models import User


class UserUpdateEmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

    # Valida se o email informado já existe em algum usuário
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "O email {} já está em uso.".format(email))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = "O formulário não será salvo com o mesmo email."
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Informe um email diferente do atual',
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
                            <i class="fa fa-refresh" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class FiscalCreateForm(forms.ModelForm):

    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label="Sobrenome")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
            ]

    # Valida se o email informado já existe em algum usuário
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "O email {} já está em uso.".format(email))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Informe os dados do Fiscal',
                Row(
                    Column('first_name', css_class='form-group col-lg mb-0'),
                    Column('last_name', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('username', css_class='form-group col-lg mb-0'),
                    Column('email', css_class='form-group col-lg mb-0'),
                ),
            ),

            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check" aria-hidden="true"></i>
                            Cadastrar
                        </button>
                    """),
                    HTML("""
                        <a href="#" class="btn btn-secondary btn-cancelar">
                            <i class="fa fa-refresh" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout


class FiscalUpdateForm(forms.ModelForm):

    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label="Sobrenome")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Atualize os dados do Fiscal',
                Row(
                    Column('first_name', css_class='form-group col-lg mb-0'),
                    Column('last_name', css_class='form-group col-lg mb-0'),
                ),
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
                            <i class="fa fa-refresh" aria-hidden="true"></i>
                            Cancelar
                        </a>
                    """),
                ),
            )  # Fim do Button
        )  # Fim do layout
