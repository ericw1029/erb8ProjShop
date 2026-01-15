from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.core.paginator import Paginator

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
    #return HttpResponse("product_list")
    return render(request,'pages/index.html',{'category': category,'categories': categories,'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()

    # Get all reviews
    all_reviews = product.reviews.all().select_related('user').order_by('-created_at')    
    # This fetches reviews AND user data efficiently
    # reviews = product.reviews.all().select_related('user').order_by('-created_at')
    
    # The rating data
    # average_data = reviews.aggregate(Avg('rating'))
    average_data = all_reviews.aggregate(Avg('rating'))
    average_rating = average_data['rating__avg'] or 0
    # rating_breakdown = reviews.values('rating').annotate(total=Count('rating')).order_by('-rating')
    rating_breakdown = all_reviews.values('rating').annotate(total=Count('rating')).order_by('-rating')

    # Pagination Logic: 10 reviews per page
    paginator = Paginator(all_reviews, 10) 
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)

    return render(request, 'product/detail.html', {
            'product': product,
            'cart_product_form': cart_product_form, 
            'reviews': reviews,
            'average_rating': round(average_rating, 1), # Round to 1 decimal place
            'rating_breakdown': rating_breakdown,
        })


def index(request):
    print(request,request.path)
    #return HttpResponse("Pages-> index")
    return render(request,'pages/index.html')

def about(request):
    #return HttpResponse("Pages-> about")
    return render(request,'pages/about.html')