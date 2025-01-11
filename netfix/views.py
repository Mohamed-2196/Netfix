from django.shortcuts import render, get_object_or_404
from services.models import ServiceRequest

from users.models import User, Company,Customer
from services.models import Service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, username):
    customer = get_object_or_404(Customer, user__username=username)
    service_history = ServiceRequest.objects.filter(customer=customer).order_by("-date_requested")
    return render(request, 'users/profile.html', {
        'customer': customer,
        'sh': service_history,
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
