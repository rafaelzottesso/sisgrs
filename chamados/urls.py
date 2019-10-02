from django.urls import path

from .views import TipoCreateView, TipoUpdateView, TipoDeleteView, TipoList, ChamadoCreateView, ChamadoList, ChamadoAbertoList, ChamadoEncerrarUpdateView, ChamadoEncerrarComMensagemCreateView, MensagemCreateView, ChamadoDetailView

urlpatterns = [
    path('cadastrar/tipo', TipoCreateView.as_view(),
         name="cadastrar-tipochamado"),

    path('editar/tipo/<int:pk>', TipoUpdateView.as_view(),
         name="alterar-tipochamado"),
    path('excluir/tipo/<int:pk>', TipoDeleteView.as_view(),
         name="excluir-tipochamado"),
    path('listar/tipo', TipoList.as_view(), name="listar-tipochamado"),

    path('cadastrar/chamado', ChamadoCreateView.as_view(),
         name="cadastrar-chamado"),
    path('encerrar/chamado/<int:pk>',
         ChamadoEncerrarUpdateView.as_view(), name="encerrar-chamado"),
    path('listar/chamados', ChamadoList.as_view(), name="listar-chamado"),
    path('listar/chamados/abertos', ChamadoAbertoList.as_view(),
         name="listar-chamados-abertos"),
    path('ver/chamado/<int:pk>/', ChamadoDetailView.as_view(), name="ver-chamado"),

    path('comentar/chamado/<int:chamado_pk>/',
         MensagemCreateView.as_view(), name="cadastrar-mensagem"),
    path('fechar/chamado/<int:chamado_pk>/',
         ChamadoEncerrarComMensagemCreateView.as_view(), name="comentar-encerrar-chamado"),
]
