from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render (request, 'store/pages/store.html', context)

def cart(request):
    context = {}
    return render (request, 'store/pages/cart.html', context)

def checkout(request):
    context = {}
    return render (request, 'store/pages/checkout.html', context)