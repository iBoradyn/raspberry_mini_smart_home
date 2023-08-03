"""Core views."""
# Django
from django.views.generic import TemplateView


class IndexView(TemplateView):  # noqa: D101
    template_name = 'index.html'
