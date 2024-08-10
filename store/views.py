from .models import Product, Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .order_models import Order, OrderItem

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_details.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('store:product_list')  # Redirect to the product list or cart page

@login_required
def cart_view(request):
    try:
        # Attempt to get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # If the cart does not exist, you can create a new one or handle the error as needed
        cart = Cart.objects.create(user=request.user)
        # You can also choose to redirect the user to the store page or some other page
        # return redirect('store:product_list')  # Uncomment to redirect to the product list

    # Get all the cart items associated with the cart
    cart_items = CartItem.objects.filter(cart=cart)
    # Calculate the total price of all the items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)
    # Count the total number of items in the cart
    total_items = cart_items.count()

    # Render the cart page with the cart items, total price, and total items
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    })
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is 0 or less
    return redirect('store:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('store:cart_view')


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})
@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    
     # Debugging line

    if request.method == 'POST':
        # Handle payment processing here

        # Clear the cart (optional)
        cart_items.delete()

        return render(request, 'store/order_success.html', {'total_price': total_price})

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
