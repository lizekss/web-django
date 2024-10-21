from django.shortcuts import render
from django.http import HttpResponse


def order_list(request):
    return HttpResponse("This is the order list.")


def order_detail(request):
    return HttpResponse("This is the order detail.")


def cart(request):
    return render(request, 'cart.html', {'title': 'Cart'})


def checkout(request):
    return render(request, 'checkout.html', {'title': 'Check Out'})
