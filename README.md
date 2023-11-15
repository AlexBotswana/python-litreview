# python-litreview
Projet 9 OCR Formation Python

Réalisation d'une application web avec Django pour permettre à une communauté d'utilisateurs de consulter ou de solliciter des critiques de livres/articles.

L'application contient un module d'inscription et de connexion.

Les utilisateurs connectés peuvent :

Demander des critiques de livres et d'articles (créer des tickets)
Créer des critiques de livres et d'articles
Suivre d'autres utilisateurs (en s'abonnant à eux)
Accéder à un flux (feed) contenant les tickets et avis de tous les utilisateurs qu'ils suivent
Accéder à leurs propres tickets et critiques (posts)
Modifier ou supprimer les tickets

Récupération du code source de l'application:
Cloner le projet à l'aide de votre terminal en tapant la commande :
```
   git clone https://github.com/AlexBotswana/python-litreview.git
```
Créer un environnement virtuel à l'aide de votre terminal, se positionner dans le répertoire python-litreview et taper la commande suivante:
```
   python -m venv litreview-venv
```
puis l'activer : 
```
   ./litreview-venv/Scripts/activate
```
Installation des requirements.txt (se positionner dans le répertoire du projet):
```
   pip install -r requirements.txt
```

Démarrage 
Dans le répertoire du projet python-litreview\litreview, taper les commandes suivantes:
```
   python manage.py migrate
   python manage.py runserver
```
L'application web est disponible en local à l'adresse: 
```
   http://localhost:8000/login/
```
