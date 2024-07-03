from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from my_shop.forms import ProductModelForm, CommentModelForm, OrderModelForm
from my_shop.models import Product, Category


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
    comments = product.comments.filter(is_possible=True)
    contex = {
        'product': product,
        'product_r': product_r,
        'comments': comments
    }
    return render(request, 'shop/detail.html', contex)


def add_comment(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.product = product
            comment.save()
            print('Save done!')
            return redirect('detail_list', slug=product_slug)
    else:
        form = CommentModelForm(request.GET)
        print('Get method running')

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'shop/detail.html', context)


def add_order(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            print('Save done!')
            return redirect('detail_list', slug=product_slug)
    else:
        form = OrderModelForm()
        print('Get method running')

    context = {
        'form': form,
        'product': product
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
