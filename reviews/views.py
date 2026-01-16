from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from pages.models import Product
from .models import Review

@login_required
def add_review(request, product_id):
    # We only care about POST requests (form submissions)
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Get data from the POST form dictionary
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        # Create the review object in the database
        if content and rating:
            Review.objects.create(
                product=product,
                user=request.user,
                content=content,
                rating=rating
            )
        
        # Redirect back to the food detail page
        return redirect(product.get_absolute_url())

    # If it's a GET request, just send them back to the list
    return redirect('pages:product_list')

# @login_required
# def edit_review(request, review_id):
#     review = get_object_or_404(Review, id=review_id, user=request.user)
    
#     if request.method == 'POST':
#         review.content = request.POST.get('content')
#         review.rating = request.POST.get('rating')
#         review.save()
#         messages.success(request, "Your review has been updated!")
        
#     return redirect('pages:product_detail', id=review.product.id, slug=review.product.slug)

@login_required
def edit_review(request, review_id):
    # This line ensures ONLY the person who wrote it can edit it
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        if content and rating:
            review.content = content
            review.rating = rating
            review.save() # This triggers the 'updated_at' timestamp
            messages.success(request, "Your review has been updated!")
        else:
            messages.error(request, "Update failed. Please provide content and rating.")
            
    # Redirect back to the detail page
    return redirect(review.product.get_absolute_url())

