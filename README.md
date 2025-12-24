# 🚀 AppStage — Plateforme Moderne de Gestion des Stages

AppStage est une plateforme web full-stack conçue pour centraliser, fluidifier et professionnaliser la gestion des offres de stage. Elle connecte efficacement entreprises, étudiants et responsables pédagogiques, tout en offrant une interface moderne, responsive et élégante grâce à un design system premium basé sur l'Indigo/Violet.

## ✨ Fonctionnalités Clés

### 🎓 Étudiants

- **Recherche avancée** : filtrage par poste, entreprise, compétences, localisation, mots-clés
- **Candidature simplifiée** : dépôt de CV, lettre de motivation et message personnalisé
- **Suivi en temps réel** : tableau de bord personnel avec statut des candidatures
- **Espace utilisateur complet** : gestion du profil, mot de passe, informations personnelles

### 🏢 Entreprises

- **Dépôt d'offres sans compte** : formulaire public sécurisé pour soumettre une offre
- **Gestion visuelle** : ajout d'images pour illustrer les offres
- **Processus simplifié** : interface claire pour publier rapidement une opportunité

### 🛡️ Administration (Staff & Superuser)

- **Modération des offres** : validation, refus, archivage, clôture
- **Dashboard analytique** : graphiques interactifs (Chart.js) pour visualiser :
  - répartition des statuts d'offres
  - volume des candidatures
  - activité globale de la plateforme
- **Gestion des accès** : contrôle complet via le backoffice Django
- **Vue consolidée** : accès rapide aux offres, candidatures et utilisateurs

## 🎨 Design & Expérience Utilisateur

AppStage intègre un design system premium basé sur une palette Indigo/Violet moderne :

- Navbar glassmorphism (blur + transparence)
- Cards élégantes avec ombres douces
- Formulaires modernes et accessibles
- Animations légères (fade-in)
- Typographie Inter pour une lisibilité optimale
- Responsive complet (mobile, tablette, desktop)

**Le résultat** : une interface professionnelle, cohérente, agréable à utiliser.

## 🛠️ Stack Technique

### Backend

- Python 3.13
- Django 5.2
- Django ORM
- Gestion des médias (CV, images d'offres)

### Frontend

- HTML5 / CSS3
- Bootstrap 5
- Design System custom (Indigo/Violet + Glassmorphism)
- Animations CSS
- Chart.js (statistiques)

### Base de données

- SQLite (développement)
- Compatible PostgreSQL / MySQL en production

### Outils & DevOps

- Git & GitHub
- Environnement virtuel Python
- Architecture Django modulaire

## ⚙️ Installation & Configuration

### 1. Cloner le projet

```bash
git clone https://github.com/votre-repo/webstage-django.git
cd webstage-django
```

### 2. Créer l'environnement virtuel

```bash
python -m venv env
source env/bin/activate      # Linux / Mac
env\Scripts\activate         # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

**Accès** : 👉 http://127.0.0.1:8000/

## 📂 Structure du Projet

```
webstage/
│── appstage/          # Offres, candidatures, pages publiques, dashboard
│── appcompte/         # Authentification, profils, mot de passe oublié
│── appadmin/          # Dashboard admin personnalisé
│── media/             # CV, images d'offres
│── static/            # CSS, JS, images
│── templates/         # Templates HTML
│── manage.py
│── requirements.txt
└── README.md
```

## 🔐 Sécurité & Permissions

- **Étudiants** : accès aux offres validées + candidatures personnelles
- **Entreprises** : dépôt d'offres sans compte
- **Staff** : validation des offres + gestion avancée
- **Superuser** : contrôle total (backoffice Django)

## 🧪 Tests

Lancer les tests unitaires :

```bash
python manage.py test
```

## 👥 Auteurs

Développé avec passion par :

- **Mohamed JADID** — Développeur Full-Stack
- **Chadi AMESTOUN** — Développeur & Architecte Logiciel

## 📄 Licence

Ce projet est sous licence MIT.  
Consultez le fichier `LICENSE` pour plus d'informations.

## ⭐ Support & Contributions

Les contributions sont les bienvenues !

Pour contribuer :

1. Fork du projet
2. Création d'une branche (`feature/ma-feature`)
3. Commit (`git commit -m "Ajout de ma feature"`)
4. Push
5. Pull Request