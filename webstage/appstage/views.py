from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appstage.models import Offre, Candidature
from .forms import OffreForm,CandidatureForm
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime
import json
from django.db.models import Count



# Page principale
def main(request):
    return render(
        request, 
        'appstage/main.html'
        )


# Liste des offres
def offres(request):
    user = request.user

    # Base queryset selon rôle
    if not user.is_authenticated:
        # Non connecté → ne voit que les offres validées
        qs = Offre.objects.filter(statutOffre='validee')

    elif user.is_superuser:
        # Admin → toutes les offres
        qs = Offre.objects.all()

    elif user.is_staff:
        # Responsable → toutes les offres (pour recherche + filtre)
        qs = Offre.objects.all()

    else:
        # Étudiant → ne voit que les offres validées
        qs = Offre.objects.filter(statutOffre='validee')

    # Recherche texte
    q = request.GET.get('q')
    if q:
        qs = qs.filter(
            Q(titreOffre__icontains=q) |
            Q(entrepriseOffre__icontains=q)
        )

    # Filtre statut (staff/admin seulement)
    statut = request.GET.get('statut')
    if statut and (user.is_staff or user.is_superuser):
        qs = qs.filter(statutOffre=statut)

    # Ajout du nombre de candidatures sur chaque offre
    offres_list = qs.annotate(nb_candidatures=Count('candidature'))

    return render(request, 'appstage/offres.html', {
        'offres': offres_list,
        'q': q or "",
        'statut': statut or "",
    })

@login_required
def offres_en_attente(request):
    # Réservé au responsable (staff) et éventuellement admin si tu veux
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, 'appstage/forbidden.html', {
            'message': "Accès réservé au responsable."
        })

    offres_list = (
        Offre.objects
        .filter(statutOffre='attente')
        .annotate(nb_candidatures=Count('candidature'))
    )

    return render(request, 'appstage/offres_en_attente.html', {
        'offres': offres_list
    })



# Détail d'une offre
def offre(request, offre_id):
    try:
        uneOffre = Offre.objects.get(IDOffre=offre_id)
    except Offre.DoesNotExist:
        return render(
            request, 
            'appstage/forbidden.html', 
            {'message': "Offre introuvable."}
        )

    # Non connecté -> peut seulement voir les validées
    if not request.user.is_authenticated and uneOffre.statutOffre != 'validee':
        return render(
            request, 
            'appstage/forbidden.html', 
            {'message': "Offre non disponible."}
        )

    return render(
        request, 
        'appstage/offre.html', 
        {'offre': uneOffre}
    )

# Formulaire création offre (accessible par tous)
def formulaireCreationOffre(request):
    if request.user.is_authenticated:  # ← SEULS visiteurs doivent y accéder
        return render(request, 'appstage/forbidden.html', {
            'message': "Seules les entreprises externes peuvent déposer une offre."
        })

    form = OffreForm()
    return render(request, 'appstage/formulaireCreationOffre.html', {'form': form})


# Création offre (accessible à tous)
def CreerOffre(request):

    # Seules les entreprises NON CONNECTÉES peuvent déposer une offre
    if request.user.is_authenticated:
        return render(request, 'appstage/forbidden.html', {
            'message': "Seules les entreprises externes peuvent déposer une offre."
        })

    form = OffreForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        offre = form.save()
        return render(
            request,
            'appstage/traitementFormulaireCreationOffre.html',
            {'titre': offre.titreOffre}
        )

    return render(
        request,
        'appstage/formulaireCreationOffre.html',
        {'form': form}
    )



# Candidature étudiante
@login_required
def candidaterOffre(request, offre_id):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, "appstage/forbidden.html",
                      {"message": "Seuls les étudiants peuvent candidater."})

    try:
        offre = Offre.objects.get(IDOffre=offre_id)
    except Offre.DoesNotExist:
        return render(request, "appstage/forbidden.html",
                      {"message": "Offre introuvable."})

    # Vérifications
    if offre.statutOffre != 'validee':
        return render(request, "appstage/offre.html",
                      {"offre": offre, "message": "Offre non disponible."})

    if Candidature.objects.filter(offre=offre, etudiant=request.user).exists():
        return render(request, "appstage/offre.html",
                      {"offre": offre, "message": "Déjà candidaté."})

    if Candidature.objects.filter(offre=offre).count() >= 5:
        return render(request, "appstage/offre.html",
                      {"offre": offre, "message": "Candidatures max atteintes."})

    # Formulaire
    if request.method == "POST":
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            cand = form.save(commit=False)
            cand.offre = offre
            cand.etudiant = request.user
            cand.save()

            # Clôture automatique
            if Candidature.objects.filter(offre=offre).count() >= 5:
                offre.statutOffre = "cloturee"
                offre.save()

            return render(request, "appstage/traitementCandidatureOffre.html",
                          {"offre": offre, "candidature": cand})
    else:
        form = CandidatureForm()

    return render(request, "appstage/formulaireCandidature.html",
                  {"form": form, "offre": offre})



def validerOffre(request, offre_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return render(
            request, 
            'appstage/forbidden.html', 
            {
                'message': "Accès refusé."
            }
        )

    try:
        offre = Offre.objects.get(IDOffre=offre_id)
    except Offre.DoesNotExist:
        return render(
            request, 
            'appstage/forbidden.html', 
            {
                'message': "Offre introuvable."
            }
        )

    # Changer le statut de l'offre en base
    offre.statutOffre = 'validee'
    offre.save()

    # Libellé lisible pour le template
    statut_libelle = "Validée"

    return render(request, 'appstage/validation_success.html', {
        'offre': offre,
        'action': statut_libelle
    })


# Refus responsable/admin
def refuserOffre(request, offre_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return render(
            request, 
            'appstage/forbidden.html', 
            {
                'message': "Accès refusé."
            }
        )

    try:
        offre = Offre.objects.get(IDOffre=offre_id)
    except Offre.DoesNotExist:
        return render(
            request, 
            'appstage/forbidden.html', 
            {
                'message': "Offre introuvable."
            }
        )

    offre.statutOffre = 'refusee'
    offre.save()

    # Libellé lisible
    statut_libelle = "Refusée"

    return render(
        request, 
        'appstage/validation_success.html', {
        'offre': offre,
        'action': statut_libelle
    })

# Mes candidatures (étudiant)
def candidaturesEtudiant(request):
    if not request.user.is_authenticated:
        return redirect('login')  # redirige vers login si non connecté

    # Récupérer toutes les candidatures de l'étudiant
    candidatures = Candidature.objects.filter(etudiant=request.user).order_by('-dateCandidature')
    
    return render(
        request, 
        'appstage/candidaturesEtudiant.html', 
        {'candidatures': candidatures}
    )

@login_required
def dashboard_admin(request):

    if not request.user.is_superuser:
        return render(request, 'appstage/forbidden.html', {
            'message': "Accès réservé au personnel."
        })

    # INDICATEURS
    total_offres = Offre.objects.count()
    offres_validees = Offre.objects.filter(statutOffre='validee').count()
    offres_attente = Offre.objects.filter(statutOffre='attente').count()
    total_candidatures = Candidature.objects.count()

    # STATUTS
    stats_statut = list(
        Offre.objects.values('statutOffre').annotate(total=Count('IDOffre'))
    )

    # 12 derniers mois
    last_year = datetime.date.today() - datetime.timedelta(days=365)

    # CANDIDATURES PAR MOIS
    stats_candidatures_mois = list(
        Candidature.objects.filter(dateCandidature__gte=last_year)
        .annotate(month=TruncMonth('dateCandidature'))
        .values('month')
        .annotate(total=Count('IDCandidature'))
        .order_by('month')
    )

    # OFFRES PAR MOIS
    stats_offres_mois = list(
        Offre.objects.filter(dateDepotOffre__gte=last_year)
        .annotate(month=TruncMonth('dateDepotOffre'))
        .values('month')
        .annotate(total=Count('IDOffre'))
        .order_by('month')
    )

    return render(request, 'appstage/dashboard_admin.html', {
        'total_offres': total_offres,
        'offres_validees': offres_validees,
        'offres_attente': offres_attente,
        'total_candidatures': total_candidatures,

        'stats_statut': json.dumps(stats_statut),
        'stats_candidatures_mois': json.dumps(stats_candidatures_mois, default=str),
        'stats_offres_mois': json.dumps(stats_offres_mois, default=str),
    })