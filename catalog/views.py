# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Product, UserProfile
from .forms import UserUpdateForm, UserProfileForm
from cart.models import Cart, Order


def store_home(request):
    # Fetch up to 4 products for the featured section
    products = Product.objects.all()[:4]
    return render(request, 'catalog/index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully. Welcome, {user.username}!")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def shop_home(request):
    products = Product.objects.all()
    
    # Category Filter (mapping check boxes to name search keywords)
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        query = Q()
        if 'watches' in selected_categories:
            query |= Q(name__icontains='watch') | Q(name__icontains='timepiece')
        if 'shoes' in selected_categories:
            query |= Q(name__icontains='shoes') | Q(name__icontains='footwear')
        if 'accessories' in selected_categories:
            query |= Q(name__icontains='accessory') | Q(name__icontains='wallet')
        if 'clothes' in selected_categories:
            query |= Q(name__icontains='clothing') | Q(name__icontains='t-shirt') | Q(name__icontains='collection')
        products = products.filter(query)

    # Price Filter
    price_range = request.GET.get('price_range')
    if price_range:
        try:
            products = products.filter(price__lte=float(price_range))
        except ValueError:
            pass
            
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')

    context = {
        'products': products,
        'selected_categories': selected_categories,
        'price_range': price_range or '350',  # default max price slider value
        'sort_by': sort_by or '',
    }
    return render(request, 'catalog/shop.html', context)

def categories_view(request):
    return render(request, 'catalog/categories.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # In a real system, we'd email or save this message, for now let's show success
        messages.success(request, f"Thank you, {name}! We have received your message and will get back to you soon.")
        return redirect('contact_view')
        
    return render(request, 'catalog/contact.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=profile)
        
    # Get active cart and items
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        
    # Get order history
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cart_items': cart_items,
        'orders': orders,
        'active_tab': request.GET.get('tab', 'profile')
    }
    return render(request, 'catalog/profile.html', context)