
from django.urls import path

from .views import IndexView, SobreView, AjudaView, IndexAutenticadoView, UserAndEmpresaByPrefeituraCreateForm, DownloadFileView, ClasseCreateView, ClasseUpdateView, ClasseList, ClasseDeleteView, ResiduoCreateView, ResiduoUpdateView, ResiduoList, ResiduoDeleteView, SetorCreateView, SetorUpdateView, SetorList, SetorDeleteView, TipoResiduoCreateView, TipoResiduoUpdateView, TipoResiduoList, TipoResiduoDeleteView, ArmazenamentoCreateView, ArmazenamentoUpdateView, ArmazenamentoList, ArmazenamentoDeleteView, DestinacaoFinalCreateView, DestinacaoFinalUpdateView, DestinacaoFinalList, DestinacaoFinalDeleteView, ResponsavelJuridicoCreateView, ResponsavelJuridicoUpdateView, ResponsavelJuridicoList, ResponsavelJuridicoDeleteView,CnaeCreateView, CnaeUpdateView, CnaeList, CnaeDeleteView, PrestadorServicoCreateView, PrestadorServicoUpdateView, PrestadorServicoList, PrestadorServicoDeleteView, TipoSituacaoCreateView, TipoSituacaoUpdateView, TipoSituacaoList, SituacaoCreateView, SituacaoUpdateView, SituacaoList, EmpresaCreateView, EmpresaUpdateView, EmpresaList, ResiduosSetorCreateView, ResiduosSetorUpdateView, ResiduosSetorList, ResiduosSetorDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    
    path('home/', IndexAutenticadoView.as_view(), name='index-auth'),
    
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('ajuda/', AjudaView.as_view(), name='ajuda'),

    path('uploads/<int:pk>/<str:file>/',
         DownloadFileView.as_view(), name="downloadfile-view"),

    path('cadastrar/classe/', ClasseCreateView.as_view(), name="cadastrar-classe"),
    path('editar/classe/<int:pk>/', ClasseUpdateView.as_view(), name="alterar-classe"),
    path('listar/classes/', ClasseList.as_view(), name="listar-classe"),
    path('excluir/classes/<int:pk>/', ClasseDeleteView.as_view(), name="excluir-classe"),

    path('cadastrar/residuo/', ResiduoCreateView.as_view(), name="cadastrar-residuo"),
    path('editar/residuo/<int:pk>/', ResiduoUpdateView.as_view(), name="alterar-residuo"),
    path('listar/residuos/', ResiduoList.as_view(), name="listar-residuo"),
    path('excluir/residuos/<int:pk>/', ResiduoDeleteView.as_view(), name="excluir-residuo"),    

    path('cadastrar/setor/', SetorCreateView.as_view(), name="cadastrar-setor"),
    path('editar/setor/<int:pk>/', SetorUpdateView.as_view(), name="alterar-setor"),
    path('listar/setor/', SetorList.as_view(), name="listar-setor"),
    path('excluir/setor/<int:pk>/', SetorDeleteView.as_view(), name="excluir-setor"),
    
    path('cadastrar/tiporesiduo/', TipoResiduoCreateView.as_view(), name="cadastrar-tiporesiduo"),
    path('editar/tiporesiduo/<int:pk>/', TipoResiduoUpdateView.as_view(), name="alterar-tiporesiduo"),
    path('listar/tiporesiduo/', TipoResiduoList.as_view(), name="listar-tiporesiduo"),
    path('excluir/tiporesiduo/<int:pk>/', TipoResiduoDeleteView.as_view(), name="excluir-tiporesiduo"),
    
    path('cadastrar/armazenamento/', ArmazenamentoCreateView.as_view(), name="cadastrar-armazenamento"),
    path('editar/armazenamento/<int:pk>/', ArmazenamentoUpdateView.as_view(), name="alterar-armazenamento"),
    path('listar/armazenamento/', ArmazenamentoList.as_view(), name="listar-armazenamento"),
    path('excluir/armazenamento/<int:pk>/', ArmazenamentoDeleteView.as_view(), name="excluir-armazenamento"),
    
    path('cadastrar/destinacaofinal/', DestinacaoFinalCreateView.as_view(), name="cadastrar-destinacaofinal"),
    path('editar/destinacaofinal/<int:pk>/', DestinacaoFinalUpdateView.as_view(), name="alterar-destinacaofinal"),
    path('listar/destinacaofinal/', DestinacaoFinalList.as_view(), name="listar-destinacaofinal"),
    path('excluir/destinacaofinal/<int:pk>/', DestinacaoFinalDeleteView.as_view(), name="excluir-destinacaofinal"),

    path('cadastrar/responsaveljuridico/', ResponsavelJuridicoCreateView.as_view(), name="cadastrar-responsaveljuridico"),
    path('editar/responsaveljuridico/<int:pk>/', ResponsavelJuridicoUpdateView.as_view(), name="alterar-responsaveljuridico"),
    path('listar/responsaveljuridico/', ResponsavelJuridicoList.as_view(), name="listar-responsaveljuridico"),
    path('excluir/responsaveljuridico/<int:pk>/', ResponsavelJuridicoDeleteView.as_view(), name="excluir-responsaveljuridico"),

    path('cadastrar/cnae/', CnaeCreateView.as_view(), name="cadastrar-cnae"),
    path('editar/cnae/<int:pk>/', CnaeUpdateView.as_view(), name="alterar-cnae"),
    path('listar/cnae/', CnaeList.as_view(), name="listar-cnae"),
    path('excluir/cnae/<int:pk>/', CnaeDeleteView.as_view(), name="excluir-cnae"),

    
    path('cadastrar/prestadorservico/', PrestadorServicoCreateView.as_view(), name="cadastrar-prestadorservico"),
    path('editar/prestadorservico/<int:pk>/', PrestadorServicoUpdateView.as_view(), name="alterar-prestadorservico"),
    path('listar/prestadorservico/', PrestadorServicoList.as_view(), name="listar-prestadorservico"),
    path('excluir/prestadorservico/<int:pk>/', PrestadorServicoDeleteView.as_view(), name="excluir-prestadorservico"),

    path('cadastrar/tiposituacao/', TipoSituacaoCreateView.as_view(), name="cadastrar-tiposituacao"),
    path('editar/tiposituacao/<int:pk>/', TipoSituacaoUpdateView.as_view(), name="alterar-tiposituacao"),
    path('listar/tiposituacao/', TipoSituacaoList.as_view(), name="listar-tiposituacao"),    

    path('cadastrar/situacao/', SituacaoCreateView.as_view(), name="cadastrar-situacao"),
    path('editar/situacao/<int:pk>/', SituacaoUpdateView.as_view(), name="alterar-situacao"),
    path('listar/situacao/', SituacaoList.as_view(), name="listar-situacao"),

    path('credenciar/empresa/',
         UserAndEmpresaByPrefeituraCreateForm.as_view(), name='credenciar-empresa'),
#     path('cadastrar/empresa', EmpresaCreateView.as_view(), name="cadastrar-empresa"),
    path('editar/empresa/<int:pk>/', EmpresaUpdateView.as_view(), name="alterar-empresa"),
    path('listar/empresas/', EmpresaList.as_view(), name="listar-empresa"),

    path('cadastrar/residuossetor/', ResiduosSetorCreateView.as_view(), name="cadastrar-residuossetor"),
    path('editar/residuossetor/<int:pk>/', ResiduosSetorUpdateView.as_view(), name="alterar-residuossetor"),
    path('listar/residuossetor/', ResiduosSetorList.as_view(), name="listar-residuossetor"),
    path('excluir/residuossetor/<int:pk>/', ResiduosSetorDeleteView.as_view(), name="excluir-residuossetor"),
    

    # path('atualizar/estado/<int:pk>/',
        #  EstadoUpdate.as_view(), name="atualizar-estado"),
]
