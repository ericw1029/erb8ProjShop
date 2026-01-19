from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.core.paginator import Paginator

import csv
import io
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .forms import CsvImportForm

from django.db import transaction
import os
from django.core.files import File


# Create your views here.
# todo
# !
## ericAdjustBranch test new folder eric
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
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
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
    print(request, request.path)
    # return HttpResponse("Pages-> index")
    return render(request, "pages/index.html")


def about(request):
    # return HttpResponse("Pages-> about")
    return render(request, "pages/about.html")


def import_product_csv(request):
    if request.method == "POST":
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            try:
                # Wrap ONLY the database processing in a transaction
                with transaction.atomic():
                    data_set = csv_file.read().decode('UTF-8')
                    io_string = io.StringIO(data_set)
                    reader = csv.reader(io_string, delimiter=',', quotechar='"')
                    next(reader)  # Skip header

                    for row in reader:
                        if len(row) < 6:
                            continue
                        
                        # CSV Mapping: 0:NAME, 1:Slug, 2:Image, 3:Description, 4:Price, 5:Availability
                        name, csv_slug_val, img_path, desc, price, avail = row[:6]

                        # 1. Category logic (using the Slug column as category name)
                        category, _ = Category.objects.get_or_create(
                            name=csv_slug_val,
                            defaults={'slug': slugify(csv_slug_val)}
                        )

                        # 2. Product instance
                        # Use the "Slug" column from CSV for the URL
                        clean_slug = slugify(csv_slug_val)
                        if not clean_slug:
                            clean_slug = slugify(name, allow_unicode=True) or "product"

                        product = Product(
                            category=category,
                            name=name,
                            slug=clean_slug,
                            description=desc,
                            price=price,
                            available=True if avail.lower() in ['all', 'yes', 'true'] else False
                        )

                        # 3. Image Logic (Handles both URL and Local path)
                        if img_path:
                            if img_path.startswith('http'):
                                try:
                                    response = requests.get(img_path, timeout=5)
                                    if response.status_code == 200:
                                        filename = img_path.split("/")[-1].split("?")[0]
                                        product.image.save(filename, ContentFile(response.content), save=False)
                                except Exception:
                                    pass
                            elif os.path.exists(img_path):
                                try:
                                    with open(img_path, 'rb') as f:
                                        filename = os.path.basename(img_path)
                                        product.image.save(filename, File(f), save=False)
                                except Exception:
                                    pass

                        product.save()

                messages.success(request, "CSV imported successfully.")
                return redirect("..")

            except Exception as e:
                messages.error(request, f"Import failed: {e}")
    else:
        form = CsvImportForm()

    return render(request, 'admin/csv_form.html', {'form': form, 'opts': Product._meta})