import logging

from django.template.defaultfilters import register

from escola.user_check_mixin import has_role_permission

logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def has_role_perm(context, perm):
    return has_role_permission(context['user'], perm)
