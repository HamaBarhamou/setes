from django import forms
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Votre nom"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Votre email"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Objet"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Message",
                    "rows": 6,
                }
            ),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Votre email"}),
        }
