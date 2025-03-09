from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path("logout/", views.logout, name="logout"),
	path('order/', views.order_history, name="order"),
	path('available/', views.available, name="available"),
	path('about/', views.about, name="about"),
	path('cart/', views.cart, name="cart"),
    path('add_quantity/<int:fruit_id>/', views.add_quantity, name='add_quantity'),   
	path('add_to_cart/<int:fruit_id>/', views.add_to_cart, name="add_to_cart"),
    path('minus_quantity/<int:fruit_id>/', views.minus_quantity, name='minus_quantity'),
	path('remove_from_cart/<int:fruit_id>/', views.remove_from_cart, name='remove_from_cart'),
    

    path("dashboard/", views.dashboard, name="dashboard"),
    path("order_dash/", views.order_dash, name="order_dash"),
    path("product/", views.product, name="product"),
    path("user/", views.user, name="user"),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
      path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
      path('profile/<int:user_id>/', views.profile, name='profile'),
    path('remove-product/<int:product_id>/', views.remove_product, name='remove_product'),

    path('add_product/', views.add_product, name='add_product'),
    
     path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

]




