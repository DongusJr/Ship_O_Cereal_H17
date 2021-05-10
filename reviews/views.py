from django.shortcuts import render
from django.views.generic import TemplateView
from reviews.models import Review
from products.models import Products

# Create your views here.
class ReviewLogic(TemplateView):
    template_name = 'proto_review/proto_review.html'
    data = {}

    def get(self, request, *args, **kwargs):
        print(*args)
        product = Products.objects.get(pk=request.GET.get('product_id'))
        all_reviews = Review.objects.filter(product=product)
        self.data['reviews'] = all_reviews
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        product = Products.objects.get(pk=request.POST.get('product_id'))
        review_object = self.review_maker(request.user, product)
        if 'rating' in request.POST and review_object.rating:
            rating = request.POST.get('rating')
            review_object.rating = rating
            review_object.save()
        if 'review' in self.request.POST and review_object.comment:
            review = self.request.POST.get('review')
            review_object.comment = review
            review_object.save()
        self.data['reviews'] = Review.objects.filter(product=product)
        return render(request, self.template_name, self.data)

    def review_maker(self, user, product):
        return Review.objects.create(user=user, product=product)