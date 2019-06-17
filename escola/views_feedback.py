import logging

from crispy_forms.utils import render_crispy_form
from django.http import JsonResponse
from django.shortcuts import reverse
from django.template.context_processors import csrf
from django.views.generic import FormView

from escola.forms import FeedbackForm

logger = logging.getLogger(__name__)


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            ctx = {}
            ctx.update(csrf(self.request))
            form_html = render_crispy_form(form, context=ctx)
            return JsonResponse({'form_html': form_html, 'success': False})
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({'success': True})
        else:
            return response


class FeedbackView(AjaxableResponseMixin, FormView):
    form_class = FeedbackForm
    template_name = 'escola/feedback/feedback_form.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('escola:index')
