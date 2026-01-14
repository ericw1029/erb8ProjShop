from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse


# Create your views here.
# todo
# !

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    # Pagination with 3 posts per page
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        page = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        page = paginator.page(paginator.num_pages)
    #return HttpResponse("product_list")
    return render(request,'pages/index.html',{'category': category,'categories': categories,'products': products,
                  'page': page})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    return render(request,'product/detail.html',{'product': product,'cart_product_form': cart_product_form})


def index(request):
    #print(request,request.path)
    #return HttpResponse("Pages-> index")
    return render(request,'pages/index.html')

def about(request):
    #return HttpResponse("Pages-> about")
    return render(request,'pages/about.html')
