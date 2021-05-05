from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import User, Order, OrderProduct

# Create your views here.
class Profile(TemplateView):
    template_name = 'proto_account/proto_order.html'

    def get_context_data(self, **kwargs):
        data = super(Profile, self).get_context_data(**kwargs)
        user = User.objects.get(session_id=self.session_id)
        data['user'] = user
        data['previous_order'] = user.order
        previous_order = Order.objects.get(prev=user.order)
        dic = {}
        for order in previous_order:
            dic[order] = OrderProduct.objects.get(order=order)
        data['order'] = dic
        return data