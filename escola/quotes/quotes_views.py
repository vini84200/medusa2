from django.views.generic import TemplateView


class AllQuotesView(TemplateView):
    template_name = 'escola/quotes/all_quotes.html'
