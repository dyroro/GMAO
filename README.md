
<body>
  <h1>Structure du projet</h1>
  <ul>
    <li>monprojet/ # Racine du projet (dossier principal)
      <ul>
        <li>manage.py # Fichier de gestion principal du projet</li>
        <li>monprojet/ # Dossier du projet (configuration globale)
          <ul>
            <li>__init__.py # Fichier vide qui indique que ce dossier est un package Python</li>
            <li>settings.py # Configuration générale du projet</li>
            <li>urls.py # Routes (URLs) principales du projet</li>
            <li>asgi.py # Configuration ASGI pour le déploiement moderne</li>
            <li>wsgi.py # Configuration WSGI pour le déploiement web</li>
          </ul>
        </li>
        <li>monapp/ # Dossier de l'application (logique métier)
          <ul>
            <li>static/
              <ul>
                <li>monapp/
                  <ul>
                    <li>style.css</li>
                  </ul>
                </li>
              </ul>
            </li>
            <li>migrations/ # Dossier des migrations de base de données</li>
            <li>templates/ # Dossier des templates HTML</li>
            <li>__init__.py # Package Python pour l'application</li>
            <li>admin.py # Configuration de l'interface d'administration</li>
            <li>apps.py # Configuration de l'application</li>
            <li>models.py # Définition des modèles de données</li>
            <li>tests.py # Tests unitaires</li>
            <li>views.py # Logique de traitement des requêtes</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</body>


