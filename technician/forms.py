from django import forms
from accounts.forms import UserForm
from technician.models import Technician

class TechnicianForm(forms.ModelForm):
  class Meta:
    model = Technician
    fields = ['technician_license', 'technician_description', 'service_description', 'service_type', 'service_charge', 'service_image' ]

  