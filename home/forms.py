from django import forms

class ContactusForm(forms.Form):
        sender = forms.EmailField(widget=forms.TextInput(attrs={'type':'email','placeholder':'Please enter your email.','class': 'form-control'}))
	subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Please enter your subject.','class': 'form-control'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'rows':6,
		'placeholder':'Please enter your message.','class': 'form-control'}))

