# Este arquivo serve para criar filtros que podem ser utilizados no template.

'''
Por padrão, há poucos e a maioria das funções em Python não podem ser utilizadas lá...
Primeiro registre um filtro e depois faça a função com um retorno
É possível passar parâmetros, ex:

def cut(value, arg):
    # Removes all values of arg from the given string
    return value.replace(arg, '')

Para usá-lo no template: {{ somevariable|cut:"|" }}

Assim, ficaria a chamada: cut(somevariable, "|")
'''
from django import template

register = template.Library()


# "Transforma" um objeto para poder usá-lo como dicionário {chave: valor} e não mais obj.chave
@register.filter(name='iterar')
def iterar(obj):
    return obj.__dict__.items()


# Verifica se um usuário está em um determinado grupo
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# Retorna um atributo de um objeto
@register.filter(name='get')
def get(obj, key):
    atr = getattr(obj, key)
    if atr:
        return atr
    else:
        return ''


# Retorna um atributo de um objeto
@register.filter(name='getDict')
def getDict(obj, key):
    return obj[key]


# Retorna um valor convertido em int
@register.filter(name='inteiro')
def inteiro(value):
    try:
        return int(value)
    except:
        return value


# Retorna um valor convertido em string
@register.filter(name='string')
def string(value):
    try:
        return str(value)
    except:
        return value


# Retorna o nome do usuário
@register.filter(name='formatarUsuario')
def formatarUsuario(user):
    try:
        if user.first_name:
            return "{} (Cód. {})".format(user.first_name, user.pk)
        elif user.empresa:
            return "" + user.empresa.cnpj
        else:
            return "" + user.username
    except:
        return "" + user.username


# Retorna a classe do objeto
@register.filter(name='get_class')
def get_class(object):
  return object._meta.verbose_name.capitalize()


# Concatena duas strings
@register.filter(name='concat')
def concat(str1, str2):
    return str(str1) + str(str2)