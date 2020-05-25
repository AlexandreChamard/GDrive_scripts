
# Application GDrive

application créer par Alexandre Chamard-bois qui permet de scanner un dossier GDrive pour le parcourir en local.

## 1. Quickstart
https://developers.google.com/drive/api/v3/quickstart/python  

## 2. Installation des dépendances python:

/!\ utiliser pip3 pour python3.  
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  

## 3. Créer un 'credentials':

1. se connecter sur Google Cloud Platform (nécéssite un compte google)  
2. aller dans la console (bouton en haut à droite de la page si connecté)  
3. créer un projet si pas encore de projet (en haut à gauche de la console)  
4. aller dans le module 'API & Services' (rechercher dans la barre en haut)  
5. aller dans l'onglet credentials  
6. cliquer sur 'create credentials' (OAuth client ID)  
7. selectionner 'other', donner un nom puis cliquer sur 'create'  
8. cliquer sur 'ok' pour fermer la fenètre  
9. télécharger l'OAuth (bouton à droite sur la ligne de l'OAuth)  
10. déplacer le fichier .json télécharger à la racine des scripts  
11. renommé le fichier '*.json' en 'credentials.json'  
12. vous pouvez maintenant lancer utiliser les scripts  

## 4. Utiliser les scripts

0. vous devez avoir un fichier 'credentials.json' à la racine des scripts (voir la partie 3)  
1. scanGDriveFolder.py: demande au lancement l'id d'un dossier GDrive (fin de l'url après le dernier '/')  
2. en cas de succès, le fichier result.txt est généré et contient l'arborescence du dossier choisi  
3. checkResult.py: parcourt l'arborescence dans le fichier result.txt (taper 'help' pour afficher la liste des commandes)  

## 5. Autre

si vous avez des questions/remarques:  
alexandre.chamard-bois@epitech.eu  

si le réseau ne fonctionne pas: reset de l'IPv6  
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1  
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1  
