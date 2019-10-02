from django.template import loader

from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,
)
# Create your views here.


def handler400(request, exception, template_name="erros/erro.html"):
    # HttpResponseBadRequest
    context = dict()
    context['title'] = 'Requisição inválida!'
    context['message'] = 'OPS! Não foi possível realizar essa requisição.'
    context['error_number'] = 'Erro: 400.'

    template = loader.get_template(template_name)
    return HttpResponseBadRequest(
        template.render(request=request, context=context)
    )


def handler403(request, exception, template_name="erros/erro.html"):
    # HttpResponseForbidden
    context = dict()
    context['title'] = 'Permissão negada!'
    context['message'] = 'OPS! Você não tem permissão para acessar esse ' \
                            'conteúdo.'
    context['error_number'] = 'Erro: 403.'

    template = loader.get_template(template_name)
    return HttpResponseForbidden(
        template.render(request=request, context=context)
    )


def handler404(request, exception, template_name="erros/erro.html"):
    # HttpResponseNotFound
    context = dict()
    context['title'] = 'Página não encontrada!'
    context['message'] = 'OPS! Não foi possível encontrar essa página.'
    context['error_number'] = 'Erro: 404.'

    template = loader.get_template(template_name)
    return HttpResponseNotFound(
        template.render(request=request, context=context)
    )


def handler500(request, template_name="erros/erro.html"):
    # HttpResponseServerError
    context = dict()
    context['title'] = 'Algo não aconteceu conforme o esperado!'
    context['message'] = 'OPS! Tem certeza que deseja e pode acessar esse endereço?'
    context['error_number'] = 'Erro: 500.'

    template = loader.get_template(template_name)
    return HttpResponseServerError(
        template.render(request=request, context=context)
    )
