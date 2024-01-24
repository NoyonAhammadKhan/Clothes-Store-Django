from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('activate/<uid64>/', views.activate, name="activate"),
    
]
