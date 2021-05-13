from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from users.models import Profile
from django.contrib.auth.models import User
# Create your views here.
# from misc.models import News

class AboutUs(TemplateView):
    template_name = 'company_info/about_us.html'
    data = {}
    '''
    AboutUs
    This view class allows us to view the page which has all information
    regarding the Ship O' Cereal operation
    '''


    def get(self, request, *args, **kwargs):
        '''
        get
        This method has a mock where we can send the proper information
        regarding the company through the logic rather than the frontend
        '''
        return render(request, self.template_name, self.data)

class EmailNewsLetter(TemplateView):
    template_name = 'company_info/email_nws.html'
    data = {}
    '''
    EmailNewsLetter
    This view class allows us to render the template which will enable the user
    to sign up for a news letter which has no functionality
    '''


    def get(self, request, *args, **kwargs):
        '''
        get
        this method only renders the html requested by the user
        '''
        #self.data['news'] = News.objects.all()
        self.data['news'] = False
        try:
            user = User.objects.get(id=request.user.id)
            self.data['sub'] = Profile.is_user_subscribed(request.user.id)
        except:
            self.data['sub'] = False
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        '''
        post
        this method redirects the user after having submitted a post request
        via the frontend
        '''
        if 'sub' in request.POST:
            Profile.subscribe_user_to_news_letter(request.user.id)
        elif 'unsub' in request.POST:
            Profile.unsubscribe(request.user.id)
        self.data['sub'] = Profile.is_user_subscribed(request.user.id)
        return render(request, self.template_name, self.data)

class OpeningHours(TemplateView):
    template_name = 'proto_opening/proto_opening_hours.html'
    data = {}

    def get(self, request, *args, **kwargs):
        self.data['default'] = '21:00 - 9:00'
        self.data['weekend'] = 'Sat - Sun'
        self.data['business_days'] = 'Mon - Fri'
        self.data['hours_weekend'] = '22:00 - 8:00'
        return render(request, self.template_name, self.data)
