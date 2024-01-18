from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:id>/', views.product_details, name="details"),
    path('purchase/<int:id>/', views.buy_product, name='purchase'),
    path('add_wishlist/<int:id>/', views.add_wishlist, name='add_wishlist'),
    path('review/<int:id>/', views.add_review, name='add_review'),
    path('rating/<int:id>/', views.add_rating, name='rating'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('orders/', views.orders, name='orders')
]
