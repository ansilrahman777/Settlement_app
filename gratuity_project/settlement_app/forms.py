from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class SettlementForm(forms.Form):
    employee_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee name'})
    )
    joining_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ending_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    basic_salary = forms.FloatField(
        validators=[MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'AED'})
    )
    allowances = forms.FloatField(
        validators=[MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'AED'})
    )
    deductions = forms.FloatField(
        validators=[MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'AED'})
    )
    al_used = forms.IntegerField(
        label='Annual Leave Used',
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    absence_days = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        joining_date = cleaned_data.get('joining_date')
        ending_date = cleaned_data.get('ending_date')

        if joining_date and ending_date:
            if ending_date <= joining_date:
                raise ValidationError("Service Ending Date must be after Joining Date.")
