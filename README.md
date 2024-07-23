# Script de Scraping

## Contexte du projet

Ce projet vise à développer un outil de scraping web pour extraire des données spécifiques à partir de pages web. En offrant deux méthodes de scraping — BeautifulSoup pour les pages statiques et Selenium pour les pages dynamiques — le script permet une extraction flexible et efficace des informations. Les données collectées sont ensuite stockées dans une base de données MongoDB pour un accès et une gestion ultérieurs. Ce projet est conçu pour simplifier la collecte automatisée de données à partir de diverses sources web, facilitant ainsi l'analyse et la recherche.

## Architecture du projet

Le projet est structuré autour de quatre fichiers principaux, chacun ayant un rôle spécifique dans le processus de scraping et de gestion des données :

- scrap_beautifulsoup.py : Ce fichier contient les fonctions nécessaires pour scraper des pages web statiques en utilisant la bibliothèque BeautifulSoup. Il est conçu pour extraire des données structurées à partir de HTML statique.

- scrap_selenium.py : Ce fichier gère le scraping des pages web dynamiques à l'aide de Selenium. Il est utilisé pour interagir avec des pages qui nécessitent des actions JavaScript ou une navigation complexe.

- bdd.py : Ce fichier est responsable de la création et de la gestion de la base de données MongoDB. Il contient les fonctions nécessaires pour se connecter à la base de données, créer des collections et effectuer des opérations de stockage des données.

- main.py : Le fichier de lancement du projet. Il orchestre l'exécution en demandant à l'utilisateur de choisir la méthode de scraping, en récupérant les pages spécifiées, et en stockant les résultats dans la base de données à l'aide des fonctions définies dans les autres fichiers.

Cette architecture permet une séparation claire des responsabilités, facilitant ainsi la maintenance et l'extension du projet.

## Prérequis

Avant de lancer le script, assurez-vous que vous avez les éléments suivants installés :

- Python 3.x
- Les bibliothèques Python suivantes :
  - `concurrent.futures`
  - `beautifulsoup4`
  - `selenium`
  - `pymongo`
- Un navigateur compatible avec Selenium (comme Chrome ou Firefox)
- MongoDB en fonctionnement

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_DOSSIER>
   ```

2. Installez les dépendances nécessaires :

   ```bash
   pip install beautifulsoup4 selenium pymongo
   ```

3. Configurez MongoDB pour qu'il soit accessible par le script.

## Utilisation

1. Lancer le Script

Exécutez le script avec Python :

   ```bash
   python nom_du_script.py
   ```

2. Choisir la Méthode de Scraping

Lorsque le script démarre, il vous demandera de choisir la méthode de scraping :

- 1 pour BeautifulSoup
- 2 pour Selenium

Entrez le numéro correspondant et appuyez sur Entrée.

3. Spécifier le Nombre de Pages

Ensuite, entrez le nombre de pages que vous souhaitez scraper et appuyez sur Entrée.

4. Traitement et Résultats

Le script :

- Utilisera des threads pour scraper les pages choisies.
- Rassemblera les données extraites.
- Supprimera les anciennes questions dans la base de données MongoDB.
- Insérera les nouvelles questions dans la base de données.

À la fin, le script affichera le nombre de questions insérées.