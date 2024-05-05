import datetime

from django import forms
from django.core.validators import RegexValidator
from customer_app.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age', 'temperament', 'health_status','photo']



class BoardingForm(forms.ModelForm):
    class Meta:
        model = Boarding
        fields = ['start_date', 'end_date', 'room_preference', 'special_requirements']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['description']

class AddBill(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=User.objects.filter(role='3'))

    class Meta:
        model = Bill
        exclude = ['status', 'paid_on']


class PayBillForm(forms.ModelForm):
    card_no = forms.CharField(validators=[RegexValidator(regex='^.{16}$', message='Please Enter a Valid Card No')])
    card_cvv = forms.CharField(widget=forms.PasswordInput,
                               validators=[RegexValidator(regex='^.{3}$', message='Please Enter a Valid CVV')])
    expiry_date = forms.DateField(widget=DateInput(attrs={'id': 'example-month-input'}))

    class Meta:
        model = CreditCard
        fields = ['card_no', 'card_cvv', 'expiry_date']

class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['name', 'breed', 'age', 'description', 'image']

class Adopt_Pet(forms.ModelForm):
    To_which_date=forms.DateField(widget=DateInput)
    class Meta:
        model = Adopt
        fields = ('Dogs','To_which_date')

        def clean_date_joining(self):
            date = self.cleaned_data['To_which_date']

            if date < datetime.date.today():
                raise forms.ValidationError("Invalid Date")
            return date
