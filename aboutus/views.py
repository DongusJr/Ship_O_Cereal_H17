from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class AboutUs(TemplateView):
    template_name = 'about_us.html'
    data = {}

    def get(self, request, *args, **kwargs):
        self.data['aboutus'] = 'lorem ipsum'
        self.data['terms'] = 'lorem ipsum'
        return render(request, self.template_name, self.data)
