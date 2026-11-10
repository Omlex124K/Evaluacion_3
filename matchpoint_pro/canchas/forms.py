
from django import forms
from .models import Cancha

# El resto del archivo (class CanchaForm...) se queda exactamente igual.

class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['codigo', 'nombre', 'disciplina', 'superficie', 'tarifa_bloque', 'estado', 'imagen', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PD-01'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cancha Central'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'superficie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pasto Sintético'}),
            'tarifa_bloque': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 15000'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Validación clean_ personalizada exigida por rúbrica para duplicados
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if Cancha.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este código único ya está registrado en el complejo.")
        return codigo

    # Validación clean_ personalizada exigida por rúbrica para valores negativos
    def clean_tarifa_bloque(self):
        tarifa = self.cleaned_data.get('tarifa_bloque')
        if tarifa is not None and tarifa < 0:
            raise forms.ValidationError("La tarifa por bloque no puede ser un valor negativo.")
        return tarifa
