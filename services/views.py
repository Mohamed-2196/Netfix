from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from users.models import Company, Customer, User
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

# List all services
def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})

# Display a single service
def index(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})

# Create a new service (only for companies)
# views.py
# services/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateNewService
from .models import Service

@login_required
def create(request):
    if not request.user.is_company:
        return redirect('home')  # Only companies can create services

    company = request.user.company
    choices = Service.FIELD_CHOICES

    # Restrict choices if the company is not "All in One"
    if company.field != 'All in One':
        choices = [(company.field, company.field)]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        form.company = company  # Pass the company instance to the form
        if form.is_valid():
            service = Service(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field'],
                company=company,
            )
            service.save()
            return redirect('/services')  # Redirect to /services after successful creation
    else:
        form = CreateNewService(choices=choices)
        form.company = company  # Pass the company instance to the form

    return render(request, 'services/create.html', {'form': form})

# Display services by field
def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})

# Request a service (only for customers)

@login_required
def request_service(request, id):
    service = get_object_or_404(Service, id=id)
    if not request.user.is_customer:
        return redirect('home')  # Only customers can request services

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            # Create a new Request object manually
            request_obj = ServiceRequest(
                customer=request.user.customer,
                service=service,
                address=form.cleaned_data['address'],
                service_time=form.cleaned_data['service_time']
            )
            request_obj.save()  # Save the object to the database
            return redirect('customer_profile', username=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'form': form, 'service': service})

# Display company profile
def company_profile(request, username):
    company = get_object_or_404(Company, user__username=username)
    services = Service.objects.filter(company=company).order_by("-date_created")  # Use 'date_created' instead of 'date'
    return render(request, 'services/company_profile.html', {
        'company': company,
        'services': services,
    })

# Display customer profile
def customer_profile(request, username):
    customer = get_object_or_404(Customer, user__username=username)
    requests = ServiceRequest.objects.filter(customer=customer)
    return render(request, 'services/customer_profile.html', {
        'customer': customer,
        'requests': requests,
    })