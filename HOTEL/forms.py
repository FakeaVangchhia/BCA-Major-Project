from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        send_mail(
            f"New message from {name} ({email})",
            message,
            email,
            ['fakeavangchhia@gmail.com'],
            fail_silently=False,
        )
