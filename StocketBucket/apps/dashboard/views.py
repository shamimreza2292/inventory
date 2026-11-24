from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login:login')
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login:login')
def orders(request):
    context = {
        'page_title': 'Orders',
    }
    return render(request, 'dashboard/orders.html', context)


@login_required(login_url='login:login')
def customers(request):
    context = {
        'page_title': 'Customers',
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='login:login')
def reports(request):
    context = {
        'page_title': 'Reports',
    }
    return render(request, 'dashboard/reports.html', context)
