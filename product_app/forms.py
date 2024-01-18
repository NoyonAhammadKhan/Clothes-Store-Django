from product_app.models import Category, Clothes, Rating, Review
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review",]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating",]
