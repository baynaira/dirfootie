from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_items = CartItem.objects.filter(cart=cart).count()
            return {'cart_item_count': total_items}
    return {'cart_item_count': 0}
