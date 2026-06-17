from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Return total sum of quantities of all items in the cart
            count = sum(item.quantity for item in cart.items.all())
            return {'cart_count': count}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}
