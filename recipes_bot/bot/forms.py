from django import forms
from .models import Recipe


class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'photo']
        labels = {
            'name': '',
            'photo': '',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опис'}),
            # 'photo': forms.ImageField()
        }
