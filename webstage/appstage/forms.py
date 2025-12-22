from django import forms
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import Offre
from .models import Candidature



class OffreForm(ModelForm):
    class Meta:
        model = Offre
        fields = [
            'entrepriseOffre', 
            'nomContactOffre', 
            'prenomContactOffre', 
            'emailContactOffre', 
            'titreOffre', 
            'detailsOffre',
            'imageOffre'
        ]
        labels = {
            'entrepriseOffre': 'Entreprise',
            'nomContactOffre': 'Nom du contact',
            'prenomContactOffre': 'Prénom du contact',
            'emailContactOffre': 'Email du contact',
            'titreOffre': "Titre de l'offre",
            'detailsOffre': "Détails de l'offre",
        }
        widgets = {
            'entrepriseOffre': TextInput(attrs={'class': 'form-control'}),
            'nomContactOffre': TextInput(attrs={'class': 'form-control'}),
            'prenomContactOffre': TextInput(attrs={'class': 'form-control'}),
            'emailContactOffre': EmailInput(attrs={'class': 'form-control'}),
            'titreOffre': TextInput(attrs={'class': 'form-control'}),
            'detailsOffre': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imageOffre': forms.FileInput(attrs={'class': 'form-control'}),

        }
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['message', 'cv', 'lettre']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explique pourquoi tu es intéressé(e) par ce stage...',
            }),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'lettre': forms.FileInput(attrs={'class': 'form-control'}),
        }