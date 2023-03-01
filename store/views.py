from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render (request, 'store/pages/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        # print(request.user.customer)
        customer = request.user.customer
        order, created =  Order.objects.get_or_create(customer=customer, complete=False)
        # print(order)
        # print(created)
        items = order.orderitem_set.all()
        # print(items)
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items': items, 'order': order}
    return render (request, 'store/pages/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =  Order.objects.get_or_create(customer=customer, complete=False)
        # print(order)
        # print(created)
        items = order.orderitem_set.all()
        # print(items)
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items': items, 'order': order}
    return render (request, 'store/pages/checkout.html', context)

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