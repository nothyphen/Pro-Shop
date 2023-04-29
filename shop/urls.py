from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout_item, name='checkout'),
    path('detail/<slug:slug>/', views.detail_product, name='detailproduct'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('payment/', views.paymentinfo, name='payment_info'),
]
