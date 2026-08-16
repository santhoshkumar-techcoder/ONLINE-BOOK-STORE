from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('category/<slug:category_slug>/', views.book_list, name='book_list_by_category'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    
    # Newsletter
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Shopping Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:book_id>/', views.cart_update, name='cart_update'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
