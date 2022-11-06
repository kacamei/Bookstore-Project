
from django.views.generic import TemplateView, ListView

from .models import Books


class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Books
    template_name = 'home.html'
