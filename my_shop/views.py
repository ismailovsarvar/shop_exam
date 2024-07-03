from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from my_shop.forms import ProductModelForm, CommentModelForm, OrderModelForm
from my_shop.models import Product, Category, Comment


# Create your views here.
@login_required(login_url='http://127.0.0.1:8000/admin/login/?next=/admin/')
def shop_list(request, category_slug=None):
    categories = Category.objects.all()
    search_query = request.GET.get('search')
    products = Product.objects.all()

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    filter_type = request.GET.get('filter')
    if filter_type == 'expensive':
        products = products.order_by('-price')
    elif filter_type == 'cheap':
        products = products.order_by('price')
    elif filter_type == 'sale':
        products = Product.objects.filter(on_sale=True)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def detail_list(request, slug):
    product = Product.objects.get(slug=slug)
    product_r = Product.objects.filter(category=product.category).exclude(slug=product.slug)
    comments = Comment.objects.filter(product__slug=slug)[0:3]
    comment_form = CommentModelForm()
    order_form = OrderModelForm()
    new_comment = None
    new_order = None

    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        order_form = OrderModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()

        elif order_form.is_valid():
            new_order = order_form.save(commit=False)
            new_order.product = product
            new_order.save()

            messages.success(request, 'Your order has been submitted!')
    context = {
        'product': product,
        'product_r': product_r,
        'comments': comments,
        'order_form': order_form,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'new_order': new_order
    }
    return render(request, 'shop/detail.html', context)


def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop_list')

    messages.success(request, 'Product has been added!')

    context = {
        'form': form,
    }
    return render(request, 'shop/add-product.html', context)
