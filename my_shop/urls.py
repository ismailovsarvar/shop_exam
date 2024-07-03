from django.urls import path

from my_shop.views import shop_list, detail_list, add_product, add_comment, add_order

urlpatterns = [
    path('home/', shop_list, name='shop_list'),
    path('category/<slug:category_slug>/products/', shop_list, name='products_of_category'),
    path('detail/<slug:slug>', detail_list, name='detail_list'),
    path('add-product/', add_product, name='add_product'),
    path('product/<slug:product_slug>/detail/add-comment/', add_comment, name='add_comment'),
    path('product/<slug:product_slug>/detail/add-order/', add_order, name='add_order'),
]
