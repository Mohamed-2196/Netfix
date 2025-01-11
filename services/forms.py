from django import forms
from django.core.exceptions import ValidationError
from .models import Service, ServiceRequest
from users.models import Company

class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00
    )
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # Add choices to the field dropdown
        if choices:
            self.fields['field'].choices = choices
        # Add placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    def clean(self):
        cleaned_data = super().clean()
        field = cleaned_data.get('field')
        company = self.company  # Pass the company instance when initializing the form

        # Ensure the service field matches the company's field of work
        if company.field != 'All in One' and company.field != field:
            raise ValidationError(f"This company can only provide {company.field} services.")

        return cleaned_data


class RequestServiceForm(forms.Form):
    address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'})
    )
    service_time = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter service time (in hours)'})
    )

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        # Add placeholders to form fields
        self.fields['address'].widget.attrs['autocomplete'] = 'off'