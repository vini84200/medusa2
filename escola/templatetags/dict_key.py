import logging

from django.template.defaultfilters import register

logger = logging.getLogger(__name__)


@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[k]


@register.filter(name='contain_key')
def contain_key(d, k):
    return k in d


@register.simple_tag
def get_p(turno, dia, p, ta):
    return ta[dia][turno.cod].periodo_set.filter(num=p)[0].materia


@register.simple_tag
def dia_teste(turno, dia, ta):
    return dia in ta and turno.cod in ta[dia]
