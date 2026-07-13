from django.shortcuts import render, get_object_or_404, render
from .models import Product, Category

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