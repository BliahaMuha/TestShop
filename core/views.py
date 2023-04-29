from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .forms import OrderForm
from .models import Product, Cart, CartProduct, Profile

session = Session()


class ProductListView(ListView):
    """ Отображение списка продуктов. """
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


def cart_detail(request):
    """
    Возвращает страницу с информацией о товарах в корзине.
    Принимает запрос пользователя "request" и возвращает страницу "cart_detail.html"
    с контекстом "context", содержащим список товаров в корзине "cart_items".
    """

    cart = request.session.get('cart', {})
    products = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        products.append({'product': product, 'quantity': quantity})

    context = {'cart': products}


    print('CONTEXT', context)

    return render(request, 'cart_detail.html', context)


class CartDetailView(View):
    """ Отображение списка товаров в корзине. """
    model = CartProduct
    template_name = 'cart_detail.html'
    context_object_name = 'cart_items'

    def get_queryset(self, request):
        user = request.user

        """ Отображаем только товары в корзине текущего пользователя. """
        if user.is_authenticated:
            return CartProduct.objects.filter(user=user)
        else:
            user = request.session.value()
            print('USER', user)
            cart_id = request.session.get('cart_id')
            print(cart_id)
            return CartProduct.objects.get('cart_id')


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
    if 'cart' not in request.session:
        request.session['cart'] = {}  # создаем пустую корзину

    cart = request.session['cart']
    cart_id = request.session.get('cart_id')
    if cart_id:
        carts = Cart.objects.get(id=cart_id)
    else:
        carts = Cart.objects.create()
        request.session['cart_id'] = cart.id



    if product_id in cart:
        product_id = cart[product_id]
        print('CART1', cart)
        cart[product_id] += 1  # увеличиваем количество товара

    else:
        cart[product_id] = 1  # добавляем новый товар
        product = Product.objects.get(id=product_id)
        print('CART', cart, product.name)

    request.session.modified = True  # сохраняем изменения в сессии
    product = Product.objects.get(id=product_id)
    cart_product, created = CartProduct.objects.get_or_create(cart=carts, product=product)
    print(cart_product, created)
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session['cart']
    del cart[str(product_id)]

    request.session.modified = True
    product = Product.objects.get(id=product_id)
    cart_product = CartProduct.objects.filter(cart=request.session['cart_id'], product=product)
    cart_product.delete()

    return redirect('cart_detail')


class ClearCartView(View):
    """
    Класс-вьюха для очистки корзины пользователя.
    """
    def get(self, request):
        request.session['cart'] = {}
        request.session.modified = True
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
