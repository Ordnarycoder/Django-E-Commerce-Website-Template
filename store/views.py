from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Favorite, CartItem, Category
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm
import json



def product_list(request):
    # Get filter parameters from the request
    query = request.GET.get('search', '')  # Search query
    category_id = request.GET.get('category')  # Category filter
    min_price = request.GET.get('min_price')  # Minimum price
    max_price = request.GET.get('max_price')  # Maximum price

    # Fetch all products initially
    products = Product.objects.all()

    # Apply filters
    if query:  # Filter by search query
        products = products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )
    if category_id:  # Filter by category
        products = products.filter(category_id=category_id)
    if min_price:  # Filter by minimum price
        products = products.filter(price__gte=min_price)
    if max_price:  # Filter by maximum price
        products = products.filter(price__lte=max_price)

    # Get favorites for the current user
    favorites = (
        request.user.favorites.values_list('product_id', flat=True)
        if request.user.is_authenticated
        else []
    )

    # Fetch categories for the filter dropdown
    categories = Category.objects.all()

    context = {
        'products': products,
        'active_page': 'product_list',
        'search_query': query,
        'favorites': favorites,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'product_list.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def redirect_to_products(request):
    return redirect('product_list')


def redirect_to_index(request):
    products = Product.objects.all()[:3]
    return render(request, 'store/index.html', {'products': products})


@login_required
def toggle_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product)

    if favorite.exists():
        favorite.delete()
        is_favorite = False
    else:
        Favorite.objects.create(user=request.user, product=product)
        is_favorite = True

    favorite_count = Favorite.objects.filter(user=request.user).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite, 'favorite_count': favorite_count})

    return redirect('product_list')





@login_required
def favorites_view(request):
    favorite_products = Product.objects.filter(favorited__user=request.user)
    return render(request, 'favorites.html', {'favorite_products': favorite_products})


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price() for item in cart_items)
    shipping = 50 
    total = subtotal + shipping

    context = {
        'cart': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'cart.html', context)



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Please check credentials again.")
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    return render(request, 'store/profile.html', {'user': user})

@login_required
def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': cart_item.quantity, 'total_price': cart_item.total_price()})
        else:
            cart_item.delete()
            return JsonResponse({'success': True, 'removed': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def remove_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size', None)
        color = request.POST.get('color', None)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = CartItem.objects.filter(user=request.user).count()

        return JsonResponse({'success': True, 'message': 'Product added to cart', 'cart_count': cart_count})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def get_cart_count(request):
    cart_count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({'cart_count': cart_count})