# ProjetFin_B3_IA-DATA
Le projet de fin d'année de Bachelor 3 IA &amp; DATA à Paris Ynov Campus

Ce projet est un projet scolaire pour un Bachelor 3 IA & DATA à Paris Ynov Campus. Il a pour objectif d'analyser des données sur la League Des Champions ainsi que le club du Real de Madrid. Nous avons été extraire des données à l'aide de plusieurs méthode : utilisation de l'API de TheSportsDB, Scraping de données sur footmercato.com et utilisation de fichiers csv. Les données scrapées sont extraites à l'aide de BeautifulSoup et Selenium, puis stockées dans une base de données MongoDB. Nous avons utiliser les endpoints fournis par TheSportDB pour l'utilisation de leur API. L'analyse et la visualisation des données est possible à l'aide de Streamlit, qui permet de créer une interface web interactive en local.

## Installation des dépendances

Assurez-vous d'avoir Python 3.x installé. Clonez ensuite le dépôt et installez les dépendances requises en exécutant les commandes suivantes dans votre terminal :

```bash
git clone https://github.com/raphacarr/Projet_B3_IA-DATA
python requirements.py
```

Assurez vous également d'avoir mongoDB qui est activé sur votre machine et modifiez la ligne suivante en fonction de votre mongo (vérifiez surtout la version) : 
```
url = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
```

## Structure du projet

Le projet est constitué de cinq fichiers principaux :

1. `DataTeam.py` :  Ce fichier contient les méthodes python permettant d'utiliser l'API de TheSportsDB à propos des données des équipes.
2. `DataPlayer.py` : Ce fichier contient les méthodes python permettant d'utiliser l'API de TheSportsDB à propos des données des joueurs.
3. `StatsJoueursScraping.py`: Ce fichier contient le code pour extraire les données des joueurs à l'aide de BeautifulSoup et Selenium, puis les stocker dans une base de données MongoDB.
6. `app.py` : Ce fichier contient le code pour créer l'interface web interactive à l'aide de Streamlit. Il permet d'afficher les données extraites et de générer des graphiques pour analyser les différentes données.
7. `config.py` : Ce fichier contient les informations de configuration pour se connecter à la base de données MongoDB.

## Utilisation
Avant tout, pour lancer le scraper, exécutez la commande suivante dans votre terminal:
```
python .\StatsJoueursScraping.py
```
Ensuite,
Pour lancer l'application Streamlit, exécutez la commande suivante dans votre terminal :

```bash
streamlit run app.py
```
Une fois l'application lancée, ouvrez votre navigateur et accédez à l'URL indiquée

## Fonctionnalités

L'interface web permet de naviguer entre 3 onglets ( Accueil, Analyses et Machine learning ), chacun représentant une partie importante du projet :
- L'onglet ##Accueil contient des informations sur le Real Madrid ainsi que sur la ligue des champions, cette partie ne comporte pas de diagramme
- L'onglet ##Analyses contient tout les diagrammes montrant les stats du Réal et qui répondent à notre problèmatique ( "Pourquoi le Réal était destiné à gagner cette ligue des champions" )
- Tandis que l'onglet ##Machine ##Learning contient deux diagrammes, l'un portant sur les chances de gagner à domicile et à l'extérieur et l'autre qui permet de faire un pronostics simple entre deux équipes ayant passé les phases de poule de la ligue des champions saison 2021-2022

    
## Licence

Ce projet est sous licence MIT. Pour plus d'informations, veuillez consulter le fichier LICENSE.

# Auteur 
Raphaël CARRILHO @raphacarr & Noah Suhard @Scr7be
