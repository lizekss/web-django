from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def product_list(request):
   return HttpResponse("This is the product list.")

def product_detail(request):
   return HttpResponse("This is the product detail.")