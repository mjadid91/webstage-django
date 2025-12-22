from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Offre (models.Model):
    IDOffre = models.AutoField(primary_key=True)
    entrepriseOffre = models.CharField(max_length=200)
    nomContactOffre = models.CharField(max_length=100)
    prenomContactOffre = models.CharField(max_length=100, blank=True, null=True)
    emailContactOffre = models.EmailField(max_length=254)
    dateDepotOffre = models.DateTimeField(auto_now_add=True)
    titreOffre = models.CharField(max_length=200)
    detailsOffre = models.TextField()

    imageOffre = models.ImageField(
        upload_to='offres_images/',
        blank=True,
        null=True
    )

    statutOffre = models.CharField(
        max_length=20,
        choices=[
            ('attente', 'En attente de validation'),
            ('validee', 'Validée'),
            ('refusee', 'Refusée'),
            ('cloturee', 'Clôturée'),
        ],
        default='attente'
    )

    def __str__(self) -> str:
        return f"{self.titreOffre} - {self.entrepriseOffre} - ({self.statutOffre})" 
    
class Candidature(models.Model):
    IDCandidature = models.AutoField(primary_key=True)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCandidature = models.DateTimeField(auto_now_add=True)

    # NOUVEAUX CHAMPS POUR UNE "VRAIE" CANDIDATURE
    message = models.TextField(blank=True, null=True)  # message de motivation
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    lettre = models.FileField(upload_to='lettres/', blank=True, null=True)

    class Meta:
        unique_together = ('offre', 'etudiant')

    def __str__(self) -> str:
        user = self.etudiant
        off = self.offre
        return f"Candidature de {user.first_name} {user.last_name} pour l'offre {off.titreOffre} le {self.dateCandidature}"
