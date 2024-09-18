from .models import Product, Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .order_models import Order, OrderItem
from django.urls import reverse
import urllib.parse


def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    
    # Pass cart item count if the user is authenticated
    cart_item_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).count()
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_item_count': cart_item_count,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Pass cart item count if the user is authenticated
    cart_item_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).count()
    
    return render(request, 'store/product_details.html', {
        'product': product,
        'cart_item_count': cart_item_count,
    })

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('store:product_list')  # Redirect to the product list or cart page

@login_required(login_url='/login/')
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
   
    # Render the cart page with the cart items, total price, and total items
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_price
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

    if request.method == 'POST':
        # Construct message
        whatsapp_number = '16575358034'
        order_items = "\n".join([f"{item.product.name}: {item.quantity} x {item.product.price}" for item in cart_items])
        message = f"Order Summary:\n{order_items}\nTotal: ${total_price}"

        encoded_message = urllib.parse.quote(message)

        # WhatsApp API URL
        whatsapp_url = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={message}"

        # Optionally, clear the cart
        cart_items.delete()

        # Redirect user to WhatsApp and then show success page
        return redirect(whatsapp_url)
    
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


