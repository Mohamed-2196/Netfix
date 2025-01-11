from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    print("LoginUserView called")  # Debug statement
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug statement
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"Email: {email}, Password: {password}")  # Debug statement
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    print("User authenticated successfully")  # Debug statement
                    login(request, user)
                    return redirect('/')
                else:
                    print("Authentication failed: Incorrect password")  # Debug statement
                    form.add_error(None, "Invalid email or password.")  # Add a non-field error
            except User.DoesNotExist:
                print("Authentication failed: User does not exist")  # Debug statement
                form.add_error(None, "Invalid email or password.")  # Add a non-field error
        else:
            print("Form is invalid")  # Debug statement
            print(form.errors)  # Print form errors
    else:
        form = UserLoginForm()

    print("Rendering login template")  # Debug statement
    return render(request, 'users/login.html', {'form': form})
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the home page after logout