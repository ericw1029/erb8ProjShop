from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pages.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    print('cart_add->product_id',product_id)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
        
    print("cart_add finish")
    
    #return redirect('cart:cart_detail')
    return render(request, 'shopCart/detail.html', {'cart': cart})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    print("cart_detail start")
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial=
                        {
                            'quantity': item['quantity'],
                            'override': True
                        })
    return render(request, 'shopCart/detail.html', {'cart': cart})
