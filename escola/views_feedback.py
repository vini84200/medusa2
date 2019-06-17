import logging
from escola.forms import FeedbackForm
from django.shortcuts import reverse
from django.views.generic import FormView

logger = logging.getLogger(__name__)


class FeedbackView(FormView):
    form_class = FeedbackForm
    template_name = 'escola/feedback/feedback_form.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('escola:index')
