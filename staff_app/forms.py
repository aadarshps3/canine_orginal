from django import forms

from customer_app.models import *
from staff_app.models import Report


class StaffUpdateBoardingForm(forms.ModelForm):
    class Meta:
        model = Boarding
        fields = ['status']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['customer','description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = User.objects.filter(role=3)
    