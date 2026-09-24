from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('create/', views.product_create_view, name='product_create'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
    path('<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete_view, name='product_delete'),

    path('<int:pk>/add-to-cart/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/create-intent/', views.create_payment_intent_view, name='create_payment_intent'),
    path('checkout/complete/', views.checkout_complete_view, name='checkout_complete'),
]