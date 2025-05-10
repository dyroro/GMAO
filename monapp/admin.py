from django.contrib import admin

# Register your models here.
# admin.py
from django import forms

from .models import Historique_de_pannes


class HistoriqueAdminForm(forms.ModelForm):
    class Meta:
        model = Historique_de_pannes
        fields = '__all__'
        widgets = {
            'annee_panne': forms.NumberInput(attrs={'min': 2000, 'max': 2100})
        }

@admin.register(Historique_de_pannes)
class HistoriqueAdmin(admin.ModelAdmin):
    form = HistoriqueAdminForm
    list_filter = ('annee_panne', 'equipment')