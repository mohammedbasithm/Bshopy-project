from django import forms
from Store.models import ProductImage
 
class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)