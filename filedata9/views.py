from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
#from django.forms import inlineformset_factory
# Create your views here.

def home(request):
    orders= Orders.objects.all()
    customers=Customer.objects.all()
    total_orders= orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status="Delivered").count()
    pending= orders.filter(status="Pending").count()
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'filedata9/dashboard.html',context)

def products(request):
    products=Products.objects.all()
    return render(request,'filedata9/products.html', {'products':products})

def customer(request,pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.orders_set.all()
    order_count = orders.count()
    context= {'customers':customers, 'orders':orders, 'order_count':order_count}
    return render(request,'filedata9/customer.html',context)



def createOrder(request,pk):
    custom= Customer.objects.get(id=pk)
    form = OrderForm()
    if request.method =='POST':
        form=OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    context  ={'form': form}
    return render(request,'filedata9/order_form.html',context)

def updateOrder(request,pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method =='POST':

        #print('Printing POST', request.POST)
        form=OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'filedata9/order_form.html',context)

def deleteOrder(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'filedata9/delete.html',context)
