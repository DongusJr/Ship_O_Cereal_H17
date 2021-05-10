from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class AboutUs(TemplateView):
    template_name = 'proto_aboutus/proto_aboutus.html'
    data = {}

    def get(self, request, *args, **kwargs):
        self.data['aboutus'] = 'lorem ipsum'
        self.data['terms'] = 'lorem ipsum'
        return render(request, self.template_name, self.data)
