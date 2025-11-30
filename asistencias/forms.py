from django import forms
from .models import CierreDiario

class CierreDiarioForm(forms.ModelForm):
    class Meta:
        model = CierreDiario
        fields = ['fecha', 'observaciones_cierre']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones_cierre': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
