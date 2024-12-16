from .models import Checker
from django import forms

class CheckerForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))





    class Meta:
        model = Checker
        fields = ['img']
