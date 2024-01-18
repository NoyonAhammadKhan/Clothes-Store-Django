from django.shortcuts import render, redirect
from .models import Clothes, Category, WishList, Order, Review, Rating, SIZE_CHOICES, COLOR_CHOICES
from . import forms


def home(request):
    size = request.GET.get('size')
    color = request.GET.get('color')
    popularity = request.GET.get('popularity')
    price = request.GET.get('price')
    sizes = dict(SIZE_CHOICES)
    colors = dict(COLOR_CHOICES)

    if color and size:
        clothes = Clothes.objects.filter(color=color, size=size)
    elif color:
        clothes = Clothes.objects.filter(color=color)
    elif size:
        clothes = Clothes.objects.filter(size=size)
    else:
        clothes = Clothes.objects.all()

    if popularity == 'desc':
        clothes = clothes.order_by('-pro_rating')
    elif popularity == 'asc':
        clothes = clothes.order_by('pro_rating')
    if price == 'asc':
        clothes = clothes.order_by('price')
    elif price == 'desc':
        clothes = clothes.order_by('-price')

    categories = Category.objects.all()

    return render(request, 'home.html', {'clothes': clothes, 'categories': categories, 'sizes': sizes, 'colors': colors})


def product_details(request, id):
    cloth = Clothes.objects.get(pk=id)
    reviews = Review.objects.filter(product=cloth)
    ratings = Rating.objects.filter(product=cloth)

    return render(request, 'product_details.html', {'cloth': cloth, 'reviews': reviews, 'ratings': ratings, })


def buy_product(request, id):
    cloth = Clothes.objects.get(pk=id)
    user = request.user
    purchase = Order.objects.create(user=user, product=cloth)
    purchase.save()
    return redirect('add_review', id=purchase.id)


def add_review(request, id):
    order = Order.objects.get(pk=id)
    product = order.product
    user = request.user
    review = Review.objects.filter(order=order)

    if review:
        form = review
        reviewed = True
    else:
        form = forms.ReviewForm()
        reviewed = False
        if request.method == 'POST':
            form = forms.ReviewForm(request.POST)
            if form.is_valid():
                review_form = form.save(commit=False)
                review_form.user = user
                review_form.order = order
                review_form.product = product
                review_form.save()
                return redirect('add_review', id=order.pk)
    return render(request, 'review_form.html', {'form': form, 'order': order, 'reviewed': reviewed})


def add_rating(request, id):
    order = Order.objects.get(pk=id)
    product = order.product
    user = request.user
    ratings = Rating.objects.filter(product=order.product)
    pro_rating = Rating.objects.filter(order=order)

    if ratings:
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        rating_count = ratings.count()
        avg_rating = total_rating/rating_count
        product.pro_rating = avg_rating
        product.save()

    if pro_rating.count() > 0:
        form = rating
        rated = True
    else:
        rated = False
        form = forms.RatingForm()
        if request.method == 'POST':
            form = forms.RatingForm(request.POST)
            if form.is_valid():
                review_form = form.save(commit=False)
                review_form.user = user
                review_form.order = order
                review_form.product = product
                review_form.save()
                return redirect('home')
    return render(request, 'rating_form.html', {'form': form, 'rated': rated, 'order': order})


def add_wishlist(request, id):
    cloth = Clothes.objects.get(pk=id)
    user = request.user
    wish = WishList.objects.create(user=user, product=cloth)
    wish.save()
    return redirect('wishlist')


def wishlist(request):
    clothes = WishList.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'clothes': clothes})


def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})
