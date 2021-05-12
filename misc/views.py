from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from users.models import Profile
# Create your views here.

class AboutUs(TemplateView):
    '''
    AboutUs
    This view class allows us to view the page which has all information
    regarding the Ship O' Cereal operation
    '''
    template_name = 'company_info/about_us.html'

    data = {}

    def get(self, request, *args, **kwargs):
        '''
        get
        This method has a mock where we can send the proper information
        regarding the company through the logic rather than the frontend
        '''
        return render(request, self.template_name, self.data)

class EmailNewsLetter(TemplateView):
    '''
    EmailNewsLetter
    This view class allows us to render the template which will enable the user
    to sign up for a news letter which has no functionality
    '''
    template_name = 'company_info/email_nws.html'
    data = {}

    def get(self, request, *args, **kwargs):
        '''
        get
        this method only renders the html requested by the user
        '''
        self.data['sub'] = Profile.is_user_subscribed(request.user.id)
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        '''
        post
        this method redirects the user after having submitted a post request
        via the frontend
        '''
        if 'sub' in request.POST:
            Profile.subscribed_to_newsletter(request.user.id)
        elif 'unsub' in request.POST:
            Profile.unsubscribe(request.user.id)
        return redirect('product_index')

class OpeningHours(TemplateView):
    template_name = 'proto_opening/proto_opening_hours.html'
    data = {}

    def get(self, request, *args, **kwargs):
        self.data['default'] = '21:00 - 9:00'
        self.data['weekend'] = 'Sat - Sun'
        self.data['business_days'] = 'Mon - Fri'
        self.data['hours_weekend'] = '22:00 - 8:00'
        return render(request, self.template_name, self.data)