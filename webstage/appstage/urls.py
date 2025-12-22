from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    # Consultation
    path('offres/', views.offres, name='offres_disponibles'),
    path('offres/<int:offre_id>/', views.offre, name='detail_offre'),
    path('offres/en-attente/', views.offres_en_attente, name='offres_en_attente'),


    # Dépôt offres
    path('offres/deposer/', views.formulaireCreationOffre, name='deposer_offre'),
    path('offres/creer/', views.CreerOffre, name='creer_offre'),

    # Candidature
    path('offres/<int:offre_id>/candidater/', views.candidaterOffre, name='candidater_offre'),
    # liste des candidatures de l'etudiant
    path('mes-candidatures/', views.candidaturesEtudiant, name='candidaturesEtudiant'),


    # Validation responsable/admin
    path('offres/<int:offre_id>/valider/', views.validerOffre, name='valider_offre'),
    path('offres/<int:offre_id>/refuser/', views.refuserOffre, name='refuser_offre'),
    
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),

]
