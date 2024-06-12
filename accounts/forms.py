from django import forms
from .models import User, UserProfile
from django.forms.widgets import PasswordInput
from django.utils.safestring import mark_safe

class PasswordInputWithToggle(PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        input_attrs = attrs.copy()
        input_attrs['class'] = 'form-control'
        rendered_input = super().render(name, value, input_attrs, renderer)
        toggle_button = """
        <div class="input-group-append">
            <button class="btn btn-outline-secondary toggle-password" type="button">
                <i class="fa fa-eye"></i>
            </button>
        </div>
        """
        return mark_safe(f'<div class="input-group">{rendered_input}{toggle_button}</div>')


    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',)
        }
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', '../fixit_main/static/js/custom.js')

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=PasswordInputWithToggle())
  confirm_password = forms.CharField(widget=PasswordInputWithToggle())
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'phone_number', 'password',]

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password does not match"
      )
    if not any(char.isalnum() for char in password):
        raise forms.ValidationError("Password must contain at least one alphanumeric character.")
    if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters long.")

    # Check if the password contains at least one alphanumeric character

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Start typing...',
        'required': 'required',
        'class': 'form-control px-2', 
    }))
    latitude = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    longitude = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude',]
        widgets = {
            'country': forms.HiddenInput(attrs={'class': 'form-control'}),
            'state': forms.HiddenInput(attrs={'class': 'form-control'}),
            'city': forms.HiddenInput(attrs={'class': 'form-control'}),
            'pin_code': forms.HiddenInput(attrs={'class': 'form-control'}),
        }