from django.shortcuts import render
from django.views.generic import TemplateView
from reviews.models import Review
from products.models import Products

# Create your views here.
class ReviewLogic(TemplateView):
    template_name = 'proto_review/proto_review_base.html'

    def get_context_data(self, **kwargs):
        data = super(ReviewLogic, self).get_context_data(**kwargs)
        product = Products.objects.get(pk=self.request.POST.get('product_id'))
        review_object = self.review_maker(self.request.user, product)
        if 'rating' in self.request.POST and review_object.rating:
            rating = self.request.POST.get('rating')
            review_object.rating = rating
            review_object.save()
            data['rating'] = int(rating)
        if 'review' in self.request.POST and review_object.comment:
            review = self.request.POST('review')
            review_object.comment = review
            review_object.save()
            data['review'] = review
        return data

    def review_maker(self, user, product):
        try:
            review = Review.objects.get(user=user, product=product)
        except:
            review= Review.objects.create(user, product=product)
        return review