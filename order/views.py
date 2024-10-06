from django.shortcuts import render
from django.http import HttpResponse


def order_list(request):
    return HttpResponse("This is the order list.")


def order_detail(request):
    return HttpResponse("This is the order detail.")
