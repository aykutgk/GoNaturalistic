from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from users.models import User_Account


class UserLoginForm(ModelForm):
    class Meta:
        model = User
	fields = '__all__'

class UserAccountForm(ModelForm):
	user_full_name = forms.RegexField(
		label=("Full Name"), max_length=50, regex=r"^[a-zA-Z]*\s[a-zA-Z]*$",
		widget=forms.TextInput(attrs={'type': 'text','placeholder':'Enter your first and last name.','class': 'form-control'}),
        	help_text=("Allison Ramsey"),
        	error_messages={
            		'invalid':("Invalid User Full Name")})

	user_phone = forms.RegexField(
                label=("Phone Number"), max_length=10, regex=r"^[0-9]{10}$",
                widget=forms.TextInput(attrs={'type': 'text','placeholder':'Enter your phone.','class': 'form-control'}),
                help_text=("5129548942"),
                error_messages={
                        'invalid':("Invalid Phone Number")})
	user_zipcode = forms.RegexField(
                label=("Zip Code"), max_length=5, regex=r"^\d{5}$",
                widget=forms.TextInput(attrs={'type': 'text','placeholder':'Enter your zip code.','class': 'form-control'}),
                help_text=("78759"),
                error_messages={
                        'invalid':("Invalid Zip Code")})

	class Meta:
                model = User_Account
		fields = ('user','user_full_name','user_phone','user_address','user_city','user_state','user_country','user_zipcode')
        	widgets = {
			'user': forms.TextInput(attrs={'type': 'hidden'}),
                	'user_address': forms.TextInput(attrs={'type': 'text','placeholder':'Enter your address.','class': 'form-control'}),
                        'user_city': forms.TextInput(attrs={'type': 'text','placeholder':'Enter your city.','class': 'form-control'}),
                        'user_state': forms.Select(attrs={'class': 'form-control input-sm'}),
                        'user_country': forms.Select(attrs={'class': 'form-control input-sm'}),
        	}

