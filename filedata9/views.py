from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only

# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)      
            messages.success(request,'Account was created for'  +  username)
            return redirect('login')
    context={'form':form}
    return render(request,'filedata9/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, "Usename or Password is incorrect")
    context={}
    return render(request,'filedata9/login.html',context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders= Orders.objects.all()
    customers=Customer.objects.all()
    total_orders= orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status="Delivered").count()
    pending= orders.filter(status="Pending").count()
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'filedata9/dashboard.html',context)

def userPage(request):
    context={}
    return render ( request, 'filedata9/userpage.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    uproducts=Products.objects.all()
    return render(request,'filedata9/products.html', {'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customers = Customer.objects.get(id=pk_test)

    orders = customers.orders_set.all()
    order_count = orders.count()
    myFilter=OrderFilter(request.GET, queryset=orders)
    orders=myFilter.qs
    context= {'customers':customers, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request,'filedata9/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Orders , fields=('product','status'),extra=10)
    custom= Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset= Orders.objects.none(), instance=custom)
    #form = OrderForm(initial={'customer':custom})
    if request.method =='POST':
        #form=OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=custom)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context  ={'formset': formset}
    return render(request,'filedata9/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'filedata9/delete.html',context)
