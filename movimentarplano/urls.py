from django.urls import path

from .views import VisualizarPlanoView, ImprimirPlanoView, ImprimirDeclaracaoPlanoView, VisualizarPlanoViewByFiscal, ListarPlanosGRSView, ListarPlanosGRSEmAnalise, ListarPlanosGRSPendentes, SubmeterPlanoByEmpresa, AnalisarPlanoGRS, AdequarPlanoGRS, AdequarPlanoGRSPorChamado, AprovarPlanoGRS

urlpatterns = [

    path('visualizar/planogrs/', VisualizarPlanoView.as_view(),
         name='visualizar-plano'),

    path('imprimir/planogrs/', ImprimirPlanoView.as_view(),
         name='imprimir-plano'),

    path('imprimir/declaracao/planogrs/', ImprimirDeclaracaoPlanoView.as_view(),
         name='imprimir-declaracao-plano'),

    path('visualizar/planogrs/<int:pk>/',
         VisualizarPlanoViewByFiscal.as_view(), name='visualizar-plano-fiscal'),

    path('listar/planogrs/', ListarPlanosGRSView.as_view(), name='listar-planogrs'),
    path('listar/planogrs/pendente',
         ListarPlanosGRSPendentes.as_view(), name='listar-planogrs-pendente'),
    path('listar/planogrs/em-analise',
         ListarPlanosGRSEmAnalise.as_view(), name='listar-planogrs-emanalise'),

    path('submeter/planogrs/', SubmeterPlanoByEmpresa.as_view(), name="submeter-plano"),
    path('analisar/planogrs/<int:pk>/',
         AnalisarPlanoGRS.as_view(), name="analisar-plano"),
    path('adequar/planogrs/<int:pk>/',
         AdequarPlanoGRS.as_view(), name="adequar-plano"),
    path('chamado/<int:pk_chamado>/adequar/planogrs/<int:pk>/',
         AdequarPlanoGRSPorChamado.as_view(), name="adequar-plano-por-chamado"),
    path('aprovar/planogrs/<int:pk>/',
         AprovarPlanoGRS.as_view(), name="aprovar-plano"),

]
