from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators  import login_required 
from django.core.paginator import Paginator 
from django.utils.functional import SimpleLazyObject
from .models import *
from .forms import *
from cart.forms import CartAddProductForm



def index_page(request):
    search_query = request.GET.get('search','')
    if search_query:
        products = Product.objects.filter(title__icontains=search_query)
        return render(request, 'product/search.html', {'products':products})
    return render(request, 'product/index.html')


def men_page(request):
    cart_product_form = CartAddProductForm()
    search_query = request.GET.get('search','')
    products = Product.objects.filter(slug__icontains='man').order_by('-views')
    products = products[:3]
    if search_query:
        products = Product.objects.filter(title__icontains=search_query)
        return render(request, 'product/search.html', {'products':products, 'cart_product_form': cart_product_form})
    return render(request, 'product/men.html', {'products':products, 'cart_product_form': cart_product_form})


def women_page(request):
    cart_product_form = CartAddProductForm()
    search_query = request.GET.get('search','')
    products = Product.objects.filter(slug__icontains='women').order_by('-views')
    products = products[:3]
    if search_query:
        products = Product.objects.filter(title__icontains=search_query)
        return render(request, 'product/search.html', {'products':products, 'cart_product_form': cart_product_form})
    return render(request, 'product/women.html', {'products':products, 'cart_product_form': cart_product_form})


def get_product(request, slug):
    cart_product_form = CartAddProductForm()
    products = Product.objects.filter(slug=slug)
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number)
    else:
        prev_url = ''
    
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {
        'page_object':page,
        'is_paginated':is_paginated,
        'next_url':next_url,
        'prev_url':prev_url,
        'cart_product_form': cart_product_form
    }
    if 'women' in slug:
        return render(request, 'product/productsw.html', context=context)
    return render(request, 'product/products.html', context=context)


def get_detail(request, pk):
    product = Product.objects.get(pk=pk)
    product.views +=1 
    product.save(update_fields=['views'])
    cart_product_form = CartAddProductForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.authored_by = request.user
            comment.save()
            return redirect('get_detail_url', pk=pk)
    form = CommentForm()
    return render(request, 'product/detail.html', {'product':product, 'form':form, 'cart_product_form': cart_product_form})

@login_required
def comment_update(request, pk, id):
    comment = get_object_or_404(Comment, pk=id)
    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            new_comment = form.save()
            return redirect('get_detail_url', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'product/comment.html', {'form': form})

@login_required
def comment_delete(request, pk, id):
    comment = Comment.objects.get(pk=id)
    if request.method == 'POST':
        comment.delete()
        return redirect('get_detail_url', pk=pk)
    return render(request, 'product/delete.html', {'comment':comment, 'pk':pk})
