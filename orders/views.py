from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.core.mail import send_mail


@login_required
def order_create(request):
    current_user = User.objects.get(id=request.user.id)
    cart = Cart(request)
    if request.method == 'POST':
        checkoutEmail = request.POST["email"]
        checkoutFirstName = request.POST["first_name"]
        checkoutLastName = request.POST["last_name"]
        
        print("POST", checkoutEmail, checkoutFirstName, checkoutLastName)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],
                                        price=item['price'],quantity=item['quantity'])
            # clear the cart
            cart.clear()
            #----------send mail---------------------------------------------
            # send_mail(
            #     "ERB8 Shop",
            #     f"Your order has been successfully completed. Your order number is {order.id}",
            #     "",
            #     [checkoutEmail],
            #     fail_silently=False,
            # )
            #---------end Send mail------------------------------------------
            return render(
                request,
                "orders/order/created.html",
                {
                    "order": order,
                    "checkoutEmail": checkoutEmail,
                    "checkoutFirstName": checkoutFirstName,
                    "checkoutLastName": checkoutLastName,                    
                },
            )
    else:
        print("order create",request.user.id)
        current_user = User.objects.get(id=request.user.id)
        # Access the user object
          
        print("order create",current_user)
        form = OrderCreateForm()
        
    return render(
        request,
        "orders/order/create.html",
        {"cart": cart, "form": form, "current_user": current_user},
    )