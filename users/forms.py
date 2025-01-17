from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Company, Customer
from django.contrib.auth import authenticate

# Define User model
User = get_user_model()

# DateInput widget for date fields
class DateInput(forms.DateInput):
    input_type = 'date'

# Email validation function
def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(value + " is already taken.")

# Customer SignUp Form
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'form-control'  # Optional: Add a CSS class
        }),
        label="Email",
        help_text="Enter a valid email address."
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control'  # Optional: Add a CSS class
        }),
        label="Username",
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'  # Optional: Add a CSS class
        }),
        label="Password",
        help_text="Your password must contain at least 8 characters and cannot be entirely numeric."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control'  # Optional: Add a CSS class
        }),
        label="Password Confirmation",
        help_text="Enter the same password as before, for verification."
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'  # Optional: Add a CSS class
        }),
        label="Date of Birth",
        help_text="Enter your date of birth."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True  # Set the user as a customer
        if commit:
            user.save()
            # Create a Customer profile for the user
            Customer.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user

# Company SignUp Form
class CompanySignUpForm(UserCreationForm):
    # Add additional fields for the company
    field = forms.ChoiceField(
        choices=Company.FIELD_CHOICES,
        label="Field of Work",
        help_text="Select your field of work from the dropdown."
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        help_text="Enter a valid email address."
    )
    username = forms.CharField(
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        help_text="Choose a unique username."
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        help_text="Your password must contain at least 8 characters and cannot be entirely numeric."
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        help_text="Enter the same password as before, for verification."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'field')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True  # Set the user as a company
        if commit:
            user.save()
            # Create a Company profile for the user
            Company.objects.create(
                user=user,
                field=self.cleaned_data['field']
            )
        return user

# User Login Form
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')

    print(f"Email: {email}, Password: {password}")  # Debug statement

    if email and password:
        # Authenticate the user using email and password
        user = authenticate(email=email, password=password)
        if user is None:
            print("Authentication failed: Invalid email or password.")  # Debug statement
            self.add_error(None, "Invalid email or password.")  # Add a non-field error
        else:
            print("User authenticated successfully")  # Debug statement
            cleaned_data['user'] = user
    else:
        print("Email or password is missing")  # Debug statement
        self.add_error(None, "Email and password are required.")  # Add a non-field error

    return cleaned_data