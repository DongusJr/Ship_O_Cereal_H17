from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# Create your views here.

class AboutUs(TemplateView):
    '''
    AboutUs
    This view class allows us to view the page which has all information
    regarding the Ship O' Cereal operation
    '''
    template_name = 'proto_aboutus/proto_aboutus.html'
    data = {}

    def get(self, request, *args, **kwargs):
        '''
        get
        This method has a mock where we can send the proper information
        regarding the company through the logic rather than the frontend
        '''
        self.data['aboutus'] = 'lorem ipsum'
        self.data['terms'] = 'lorem ipsum'
        return render(request, self.template_name, self.data)

class EmailNewsLetter(TemplateView):
    '''
    EmailNewsLetter
    This view class allows us to render the template which will enable the user
    to sign up for a news letter which has no functionality
    '''
    template_name = 'email_nws.html'
    data = {}

    def get(self, request, *args, **kwargs):
        '''
        get
        this method only renders the html requested by the user
        '''
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        '''
        post
        this method redirects the user after having submitted a post request
        via the frontend
        '''
        return redirect('product_index')
