from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import MyUser, Product, Purchase


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ["username", ]


class AppendForm(ModelForm):
    class Meta:
        model = Product
        exclude = []


class BuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ["quantity"]

    def clean(self):
        cleaned_data = super().clean()
        need_count = cleaned_data.get("quantity")
        if not need_count > 0:
            self.add_error("quantity", f"count must be more than {need_count}")
