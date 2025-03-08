from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path("logout/", views.logout, name="logout"),
	path('profile/', views.profile, name="profile"),
	path('order/', views.order, name="order"),
	path('available/', views.available, name="available"),
	path('about/', views.about, name="about"),
	path('contact/', views.contact, name="contact"),
	path('cart/', views.cart, name="cart"),
    path('add_quantity/<int:fruit_id>/', views.add_quantity, name='add_quantity'),   
	path('add_to_cart/<int:fruit_id>/', views.add_to_cart, name="add_to_cart"),
    path('minus_quantity/<int:fruit_id>/', views.minus_quantity, name='minus_quantity'),
	path('remove_from_cart/<int:fruit_id>/', views.remove_from_cart, name='remove_from_cart'),
]


