from itertools import product
from multiprocessing import context
from django.shortcuts import render
from .models import *
import json
import requests
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)



def search(request):
    context = {}
    return render(request, 'store/search.html', context)

@csrf_exempt    
def searchresult(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        result = requests.get(
            'https://api.kinopoisk.dev/movie',
            params={
                'field': 'id',
                'search': f'{form.id}',
                'token': 'ZQQ8GMN-TN54SGK-NB3MKEC-ZKB8V06',
            }
        )

        movies = result.json()
    
        if movies:
            context = {
                'id': movies['id'],
                'name': movies['name'],
                'description': movies['description'],
                'poster': movies['poster']['previewUrl'],
                'raw': movies,
            }

        else:
            context = {"movies": 'error'}

        if form.is_valid():
            return render(request, 'store/searchresult.html', context)

    else:
        form = SearchForm()

        context = {"movies": 'error'}
        return render(request, 'store/searchresult.html', context)