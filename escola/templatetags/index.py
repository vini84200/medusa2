from django.template.defaultfilters import register


@register.filter(name='index')
def index(List, i):
    return List[int(i)]


@register.filter(name='index1')
def index1(List, i):
    return List[int(i-1)]