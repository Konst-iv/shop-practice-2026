from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import OrderCreateForm
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all() # Получаем все категории для фильтра

    # Получаем параметры поиска и фильтрации из GET-запроса
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    # Применяем фильтр по поисковому запросу (ищем по названию или описанию)
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    # Применяем фильтр по категории
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'shop/product_list.html', context)

# Добавьте эту функцию:
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) # Защита: если id не существует, вернет 404
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    total_price = sum(item.get_total_price() for item in cart.items.all())
    
    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def order_create(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            cart.items.all().delete()
            
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
        
    total_price = sum(item.get_total_price() for item in cart.items.all())
    return render(request, 'shop/order_create.html', {
        'cart': cart,
        'form': form,
        'total_price': total_price
    })

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'shop/order_list.html', {'orders': orders})