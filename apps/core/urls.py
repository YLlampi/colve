from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('add_buy/', views.buy_form, name='add_buy'),
    path('add_sale/', views.sale_form, name='add_sale'),

    path('save_sale/', views.save_sale, name='save_sale'),
    path('save_buy/', views.save_buy, name='save_buy'),

    path('detail/', views.DetailView.as_view(), name='detail'),
    path('cart_view/', views.CartView.as_view(), name='cart_view'),

    path('carrito/', views.carrito, name='carrito'),

]
