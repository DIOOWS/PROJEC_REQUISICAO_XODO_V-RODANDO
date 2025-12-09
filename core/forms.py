from django import forms
from .models import Product, Requisition

class ProductAdminForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label="Imagem (upload)")

    class Meta:
        model = Product
        fields = "__all__"


class RequisitionAdminForm(forms.ModelForm):
    icon_file = forms.FileField(required=False, label="Ícone (upload)")

    class Meta:
        model = Requisition
        fields = "__all__"
