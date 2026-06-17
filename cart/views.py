from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from catalog.models import Product, UserProfile
from .models import Cart, CartItem, Order, OrderItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    # Calculate item subtotals and overall cart total
    cart_total = 0
    for item in items:
        item.subtotal = item.product.price * item.quantity
        cart_total += item.subtotal
        
    context = {
        'cart': cart,
        'items': items,
        'cart_total': cart_total,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock at all
    if product.stock_quantity <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('home')
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        # If product already in cart, check if incrementing quantity exceeds stock limits
        if cart_item.quantity + 1 > product.stock_quantity:
            messages.warning(request, f"Cannot add more of {product.name}. Only {product.stock_quantity} available in stock.")
            return redirect('cart_detail')
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.success(request, f"Added {product.name} to your cart.")
        
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect('cart_detail')

@login_required
def checkout(request):
    if request.method != 'POST':
        return redirect('cart_detail')
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    if not items.exists():
        messages.error(request, "Your shopping cart is empty.")
        return redirect('cart_detail')
        
    # Get checkout parameters from the POST form
    delivery_type = request.POST.get('delivery_type', 'Delivery')
    shipping_address = request.POST.get('shipping_address', '')
    shipping_city = request.POST.get('shipping_city', '')
    shipping_country = request.POST.get('shipping_country', '')
    shipping_phone = request.POST.get('shipping_phone', '')
    payment_method = request.POST.get('payment_method', 'COD')
    save_to_profile = request.POST.get('save_to_profile', 'false')
        
    # Start atomic database transaction to prevent race conditions during purchase
    try:
        with transaction.atomic():
            cart_total = 0
            order_items_to_create = []
            products_to_update = []
            
            # Step 1: Validate stock and calculate totals
            for item in items:
                # Refresh product from DB within the transaction for lock protection
                product = Product.objects.select_for_update().get(id=item.product.id)
                
                if product.stock_quantity < item.quantity:
                    messages.error(
                        request, 
                        f"Insufficient stock for '{product.name}'. "
                        f"Available: {product.stock_quantity}, in your cart: {item.quantity}."
                    )
                    return redirect('cart_detail')
                    
                item_subtotal = product.price * item.quantity
                cart_total += item_subtotal
                
                # Deduct stock
                product.stock_quantity -= item.quantity
                products_to_update.append(product)
                
                # Keep order item data
                order_items_to_create.append({
                    'product': product,
                    'price': product.price,
                    'quantity': item.quantity
                })
            
            # Step 2: Create the Order
            order = Order.objects.create(
                user=request.user, 
                total_price=cart_total, 
                status='Pending',
                delivery_type=delivery_type,
                shipping_address=shipping_address if delivery_type == 'Delivery' else 'Store Pickup',
                shipping_city=shipping_city if delivery_type == 'Delivery' else 'Accra',
                shipping_country=shipping_country if delivery_type == 'Delivery' else 'Ghana',
                shipping_phone=shipping_phone,
                payment_method=payment_method
            )
            
            # Step 3: Create OrderItems
            for oi in order_items_to_create:
                OrderItem.objects.create(
                    order=order,
                    product=oi['product'],
                    price=oi['price'],
                    quantity=oi['quantity']
                )
                
            # Step 4: Save all updated products
            for product in products_to_update:
                product.save()
                
            # Step 5: Save to user profile if checked
            if save_to_profile == 'true' or save_to_profile == 'on':
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if delivery_type == 'Delivery':
                    profile.address = shipping_address
                    profile.city = shipping_city
                    profile.country = shipping_country
                profile.phone_number = shipping_phone
                profile.payment_method = payment_method
                profile.save()
                
            # Step 6: Clear items in the Cart
            items.delete()
            
            messages.success(request, "Order placed successfully!")
            return redirect('order_success', order_id=order.id)
            
    except Exception as e:
        messages.error(request, f"An error occurred while processing your checkout: {str(e)}")
        return redirect('cart_detail')

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'items': order.items.all()
    }
    return render(request, 'cart/order_success.html', context)
