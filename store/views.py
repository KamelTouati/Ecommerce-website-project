import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    context = {'products': products, 'cartItems': cartItems}
    return render (request, 'store/pages/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render (request, 'store/pages/cart.html', context)

@csrf_exempt
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render (request, 'store/pages/checkout.html', context)

def updateItem(request): 
    # print(request.body)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # print('productId:', productId)
    # print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id = productId) 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0 : 
        orderItem.delete()
    return JsonResponse('Item was added', safe= False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print('data:', request.body)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse('payment complete', safe= False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None: 
            print (user)
            login(request, user)
            return redirect('/')
        else: 
            messages.info(request, 'Credentials Invalid')
            print('Credentials Invalid')
            return redirect('login')
    else:
        return render (request, 'store/pages/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if password == confirmpassword:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Already Exists')
                print("Email Already Exists")
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username Already Exists')
                print("username Already Exists")
                return redirect('register')
            else: 
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                print("save new user")
                return redirect('login')
        else: 
            messages.info(request, 'Password Not The Same')
            print("password not the same")
            return redirect('register')
    else:
        return render(request, 'store/pages/register.html')    

def logout_view(request):
    logout(request)
    return redirect('/')