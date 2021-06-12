from django import forms


from django.forms import ModelForm, TextInput

from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


# class TrouserForm(ModelForm):
#     class Meta:
#         model = Trouser
#         fields = ["title", "quantity"]
#         widgets = {
#             "title": TextInput(attrs={
#                 'class': 'form-control', 
#                 "placeholder": "Введите название"
#             }),
#             "quantity": TextInput(attrs={
#                 'class': 'form-control', 
#                 "placeholder": "Введите в наличии"
#             })
#         }  