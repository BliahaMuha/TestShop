from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Product, Cart, CartProduct, Profile

session = Session()

def product_list(request):
    """ Отображение списка продуктов.
    :param request: запрос от клиента
    :type request: HttpRequest
    :return: отрендеренный шаблон со списком продуктов
    :rtype: HttpResponse """

    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def cart_detail(request):
    """
    Возвращает страницу с информацией о товарах в корзине.
    Принимает запрос пользователя "request" и возвращает страницу "cart_detail.html"
    с контекстом "context", содержащим список товаров в корзине "cart_items".
    """
    cart_items = CartProduct.objects.all()
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart_detail.html', context)


def add_to_cart(request, product_id):
    """ Функция добавления товара в корзину.
    Аргументы:
    request -- объект запроса
    product_id -- идентификатор товара

    Возвращает:
    перенаправление на страницу корзины

    Если пользователь авторизован, то товар добавляется в корзину этого пользователя.
    Если пользователь не авторизован, товар добавляется в сессию корзины.
    Если в запросе указан идентификатор корзины, то товар добавляется в эту корзину.
    Если корзины не существует, создается новая корзина.
    Если товар уже есть в корзине, то увеличивается его количество на 1.
    """
    cart_id = request.GET.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        user = request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
    product = Product.objects.get(id=product_id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    """ Функция для удаления товара из корзины.
    Аргументы:
    - request: объект запроса
    - product_id: идентификатор товара

    Возвращает:
    - перенаправление на страницу корзины
    """
    cart_id = request.GET.get('cart_id')
    print(cart_id)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        user = request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
    if cart:
        product = Product.objects.get(id=product_id)
        cart_product = CartProduct.objects.get(cart=cart, product=product)
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        else:
            cart_product.delete()
    return redirect('cart_detail')


def clear_cart(request):
    """
    Функция для очистки корзины пользователя.
    :param request: запрос HTTP
    :type request: HttpRequest
    :return: перенаправление на страницу с деталями корзины пользователя
    :rtype: HttpResponse
    """
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    if cart:
        cart.cartproduct_set.all().delete()
    return redirect('cart_detail')


def checkout(request):
    """ Функция для оформления заказа и очистки корзины пользователя.
    :param request: запрос HTTP
    :type request: HttpRequest
    :return: перенаправление на страницу успеха оформления заказа
    :rtype: HttpResponse """

    cart_id = request.session.get('cart_id')
    cart = CartProduct.objects.filter(cart_id=cart_id).first()
    if not cart:
        return redirect('product_list')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.create(user_id=cart_id)
            profile.name = form.data['name']
            profile.phone = form.data['phone']
            profile.address = form.data['address']
            profile.save()
            cart_items = CartProduct.objects.filter(cart_id=cart_id)
            for item in cart_items:
                item.delete()
            return redirect('checkout_success')
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})


def checkout_success(request):
    """
    Функция перенаправления на страницу
     с уведомлением об успешном заказе
    :param request:
    :return:
    """
    return render(request, 'checkout_success.html')
