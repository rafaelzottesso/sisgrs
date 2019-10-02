
from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

from .views import UserUpdateView, FiscalCreateView, FiscalListView, FiscalUpdateView

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='usuarios/login.html',
            extra_context={'titulo': 'Autenticação'}
        ),
        name="login"
    ),

    path('sair/', auth_views.LogoutView.as_view(), name="logout"),

    path(
        'alterar-senha/',
        auth_views.PasswordChangeView.as_view(
            template_name='usuarios/user_base_form.html',
            success_url=reverse_lazy('index-auth'),
            extra_context={
                'titulo': 'Alterar senha atual',
                'botao_submit': 'Alterar senha',
                'botao_submit_class': 'btn-success',
                '': '',
            }
        ),
        name="user-alterar-senha"
    ),

    path('alterar/meus-dados/', UserUpdateView.as_view(),
         name='user-alterar-dados'),

    path('cadastrar/fiscal/', FiscalCreateView.as_view(), name='cadastrar-fiscal'),
    path('alterar/fiscal/<int:pk>/',
         FiscalUpdateView.as_view(), name='alterar-fiscal'),
    path('listar/fiscal/', FiscalListView.as_view(), name='listar-fiscal'),

    path('esqueci-senha/',
         auth_views.PasswordResetView.as_view(template_name='senha/password_reset_form.html'), name='password_reset'),

    path('senha-enviada/',
         auth_views.PasswordResetDoneView.as_view(template_name='senha/password_reset_done.html'), name='password_reset_done'),

    path('redefinir-senha/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='senha/password_reset_confirm.html'), name='password_reset_confirm'),

    path('senha-atualizada/',
         auth_views.PasswordResetCompleteView.as_view(template_name='senha/password_reset_complete.html'), name='password_reset_complete'),


]
