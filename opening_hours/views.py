from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class OpeningHours(TemplateView):
    template_name = 'proto_opening/proto_opening_hours.html'
    data = {}

    def get(self, request, *args, **kwargs):
        self.data['default'] = '21:00 - 9:00'
        self.data['weekend'] = 'Sat - Sun'
        self.data['business_days'] = 'Mon - Fri'
        self.data['hours_weekend'] = '22:00 - 8:00'
        return render(request, self.template_name, self.data)