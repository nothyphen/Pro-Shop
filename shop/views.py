from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.http import JsonResponse
import json
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.urls import reverse

# Create your views here.
def index(request):
    category = Category.objects.all()
    banner = Banner.objects.all()
    context = {
        'categories' : category,
        'banners' : banner,
    }
    return render(request, 'index.html', context=context)

def checkout_item(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else :
        items = []
        order = {
            'get_cart_total':0,
            'shipping' : False
        }
        cartItem = ''
    context = {
            'items' : items,
            'order' : order,
            'cartItems' : cartItem,
        }
    print(order.get_cart_total)
    return render(request, 'checkout.html', context=context)

def detail_product(request, slug):
    product = product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total':0,
            'cartItems' : cartItem,
        }
    context = {
        'product' : product,
        'items' : items,
        'order' : order,
        'cartItems' : cartItem,
    }
    return render(request, 'detail.html', context=context)

def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        
    else:
        items = []
        order = {
            'get_cart_total':0,
        }
        cartItem = order['get_cart_items']

    product = Product.objects.all()
    context = {
        'products' : product,
        'cartItems' : cartItem,
    }
    return render(request, "shop.html", context=context)

def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total':0,
            'cartItems' : cartItem,
        }
    context = {
        'items' : items,
        'order' : order,
        'cartItems' : cartItem,
    }
    return render(request, "contact.html")

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        
    else:
        items = []
        order = {
            'get_cart_total':0,
            'cartItems' : cartItem,
        }
    context = {
            'items' : items,
            'order' : order,
            'cartItems' : cartItem,
        }
    return render(request, 'cart.html', context=context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(action)
    print(productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == "removeAll":
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

def processOrder(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        street = request.POST['address']
        zipcode = request.POST['zipcode']
        shipping, created = ShippingAddress.objects.get_or_create(customer=customer, order=order, address=address, city=city, state=state, street=street, zipcode=zipcode)
    return redirect('/payment/')

def paymentinfo(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else :
        items = []
        order = {
            'get_cart_total':0,
            'shipping' : False
        }
        cartItem = ''
    context = {
            'items' : items,
            'order' : order,
            'cartItems' : cartItem,
        }
    print(order.get_cart_total)
    return render(request, 'payment.html', context=context)

def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    normal = str(int(order.get_cart_total))+'0'
    amount = int(normal)
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = ''  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('/callback/'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e
    
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        order.save()


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")