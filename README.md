# PDF Compressor

Application Flask simple permettant de compresser des fichiers PDF directement depuis une interface web basée sur Bootstrap. Cette solution est adaptée à un hébergement mutualisé O2switch (Passenger WSGI) et s'appuie sur l'outil Ghostscript pour réaliser la compression.

## Prérequis

- Python 3.10 ou plus récent
- Ghostscript (`gs`) installé sur le serveur
- Accès SSH ou gestionnaire d'applications Python d'O2switch

Sur O2switch, vous pouvez installer Ghostscript via `yum` depuis le cPanel (Terminal SSH) :

```bash
yum install ghostscript -y
```

## Installation

1. Clonez le dépôt sur votre machine ou directement sur le serveur :

   ```bash
   git clone <votre-url>
   cd pdfcompress
   ```

2. Créez un environnement virtuel et installez les dépendances :

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Exportez une clé secrète :

   ```bash
   export SECRET_KEY="une-cle-secrete-a-changer"
   ```

4. Lancez l'application en local :

   ```bash
   flask --app app run --debug
   ```

   Le site est accessible sur http://127.0.0.1:5000.

## Déploiement sur O2switch

1. Connectez-vous au cPanel puis ouvrez la section « Application Python ».
2. Créez un environnement Python (version 3.10 recommandée) et installez les dépendances depuis `requirements.txt`.
3. Uploadez les fichiers du projet dans le dossier de l'application.
4. Configurez le fichier WSGI pour pointer vers `app:app`.
5. Assurez-vous que Ghostscript est installé sur le serveur et accessible (commande `which gs`).
6. Optionnel : configurez un domaine ou sous-domaine pour pointer vers le dossier de l'application.

## Utilisation

- Rendez-vous sur la page d'accueil.
- Téléversez un fichier PDF (max 32 Mo).
- Choisissez le niveau de compression souhaité.
- Téléchargez immédiatement le PDF compressé.

## Personnalisation

- Les niveaux de compression sont définis dans `QUALITY_PRESETS` dans `app.py`.
- Vous pouvez ajuster la limite de taille via `MAX_CONTENT_LENGTH` dans `create_app()`.
- La mise en forme peut être personnalisée dans `static/css/style.css` ou en modifiant le template `templates/index.html`.

## Licence

Ce projet est distribué sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.
