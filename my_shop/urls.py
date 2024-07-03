from django.urls import path

from my_shop.views import shop_list, detail_list, add_product

urlpatterns = [
    path('home/', shop_list, name='shop_list'),
    path('category/<slug:category_slug>/products/', shop_list, name='products_of_category'),
    path('detail/<slug:slug>', detail_list, name='detail_list'),
    path('add-product/', add_product, name='add_product'),
]
