from .models import Favorite, CartItem

def favorite_count_processor(request):
    if request.user.is_authenticated:
        favorite_count = Favorite.objects.filter(user=request.user).count()
    else:
        favorite_count = 0
    return {'favorite_count': favorite_count}

def cart_count_processor(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
