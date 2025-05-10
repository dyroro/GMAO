monprojet/           # Racine du projet (dossier principal)
├── manage.py        # Fichier de gestion principal du projet
├── monprojet/       # Dossier du projet (configuration globale)
│   ├── __init__.py  # Fichier vide qui indique que ce dossier est un package Python
│   ├── settings.py  # Configuration générale du projet
│   ├── urls.py      # Routes (URLs) principales du projet
│   ├── asgi.py      # Configuration ASGI pour le déploiement moderne
│   └── wsgi.py      # Configuration WSGI pour le déploiement web
└── monapp/          # Dossier de l'application (logique métier)
    ├── static/
        ├── monapp/
            ├── style.css
    ├── migrations/  # Dossier des migrations de base de données
    ├── templates/   # Dossier des templates HTML
    ├── __init__.py  # Package Python pour l'application
    ├── admin.py     # Configuration de l'interface d'administration
    ├── apps.py      # Configuration de l'application
    ├── models.py    # Définition des modèles de données
    ├── tests.py     # Tests unitaires
    └── views.py     # Logique de traitement des requêtes
