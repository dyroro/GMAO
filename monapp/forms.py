# forms.py
from django import forms
from .models import Equipment
from django import forms
from .models import Personnel

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'date_maint': forms.DateInput(attrs={'type': 'date'}),
        }



class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'exemple@domaine.com'}),
        }
from django import forms
from .models import Equipment

class EquipmentSelectForm(forms.Form):
    equipement = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label="Choisissez un équipement",
        required=True
    )

from django import forms
from .models import HistoriquePlanning

class HistoriquePlanningForm(forms.ModelForm):
    class Meta:
        model = HistoriquePlanning
        fields = ['type', 'duree']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'duree': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }
from django import forms
from .models import BonTravail

# forms.py
from django import forms
from .models import BonTravail

class BonTravailForm(forms.ModelForm):
    class Meta:
        model = BonTravail
        fields = '__all__'
        widgets = {
            'numero':     forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numéro'}),
            'date':       forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'demandeur':  forms.TextInput(attrs={'class':'form-control', 'placeholder':'Demandeur'}),
            'lieu':       forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lieu'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'style':'height:100px;'}),
            'technicien': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Technicien'}),
            'duree':      forms.TextInput(attrs={'class':'form-control', 'placeholder':'Durée'}),
        }

# forms.py
from django import forms
from .models import Historique_de_pannes
# forms.py
from django import forms


class PanneForm(forms.ModelForm):
    class Meta:
            model = Historique_de_pannes
            fields = ['panne','ttr','criticite','equipment']
            widgets = {
                'equipment': forms.Select(attrs={'id': 'equipment-field'}),
            }

    # Ajout d’un champ d’année automatique
    def save(self, commit=True):
        instance = super().save(commit=False)
        from datetime import datetime
        instance.annee_panne = datetime.now().year
        if commit:
            instance.save()
        return instance


