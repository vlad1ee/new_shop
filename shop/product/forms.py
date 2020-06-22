from django import forms 
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['message']
        widgets = {
            'message':forms.Textarea(attrs={'class':'form-control'})
        }