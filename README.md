# DSIA4101A

**Introduction :**  
Ce projet a étét réaliser en binome par Romain Yerolymos et Guillaume Curtis. 
Ce projet cherche à monter une corélation entre le nombre de policier municipaux et le nombre de délits commits. Il cherche aussi à montrer la corrélation entre la population et le nombre d'incidents commits.

# Sommaire 

## Data sets (jeux de données)
1. [ Introduction](#1--- Introduction)
2. [Information sur les datas sets utilisés](#2---Information sur les datas sets utilisés)

## User guide
1. [Prérequis d'installation](#1---Prérequis-dinstallation)
2. [Lancer l'application](#2---Lancer-lapplication)
3. [Présentation du Dashboard](#3---Présentation-du-dashboard)

## Guide du developpeur
1. [Introduction](#1---Introduction)
2. [Organisation du code ](#2---Organisation du code )
3. [Ajouter une page](#3---Ajouter-une-page)
4. [Suggestions d'améliorations futures](#4---Suggestions-daméliorations-futures)
---

# Data sets

## 1 - Introduction

Nous voulions à travers ces deux jeux de données savoir si il y avait une corrélation entre les effectifis de la police municipales et les délits commits dans les villes. 

## 2 - Information sur les datas sets utilisés

Voici les liens des données utilisées :

https://www.data.gouv.fr/fr/datasets/police-municipale-effectifs-par-commune/#/community-reuses

https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources

Les données ont été trouvés sur le site Datagouv.fr
C'est un site qui permet au utilisateurs de trouver tout type de données sur la vie en france.

Le premier lien est le lien pour trouver les données des effectifs de police municipaux en fonction des années et le deuxième permet de faire pareils mais avec tous les delits commits dans les communes françaises.

# User Guide 

Cette partie est destinée à l'importation de tous les fihier depuis Git-hub et à la visualisation de notre Dashboard.

## 1 - Prérequis 

Ce projet est entièrement réaliser en python une version égale ou superieur à  .... est vivement conséillé.
[Installer une version de python au moins égale à 3.11](https://www.python.org/downloads/)

Il faudra aussi avoir un compte sur Git-Hub

[Page d'acceuil Github](https://github.com/)

## 2 - Exportation du projet 


### Cloner le répertoire sur sa machine :
Pour ce faire, ouvrez le ‘Git Bash’ (vous pouvez le chercher depuis la barre
de recherche windows). Rentrez la commande suivante dans ‘Git Bash’ :
git clone https://git.esiee.fr/carangeh/carangeot_sali-orliange_pythonds_e4



### Installer les packages nécessaires au programme :

Pour ce faire, ouvrez l' ’Invite de Commandes’ (vous pouvez la chercher
depuis la barre de recherche windows). À l’aide de la commande ‘cd’ rejoignez
votre dossier ‘CARANGEOT_SALI-ORLIANGE_PYTHONDS_E4’ qui correspond au dossier
cloné de Git.

Enfin, depuis ce dossier, rentrez la commande suivante : 
python -m pip install -r requirements.txt

## 3 - Ouvrir le Dashboard 


Après avoir suivie tous les étapes précedentes il vous suffit de rentrer la commande suivante  :

```
*python Dashboard.py*
```

Vous obtiendrez ensuite:

![image](https://github.com/user-attachments/assets/4a72750f-7073-4ec3-b40f-f7d8777f0cbc)

cliquez sur http://127.0.0.1:8050/

et vous voilà sur notre dashboard.

## 4 - Utilisation du Dashboard 





# Guide du developpeur 

## Introduction 

Ce guide du developpeur est concue pour faciliter l'ajout de nouvelles fonctionnalités et de son amélioration.

## Organisation du code 

Notre code est structuré en plusieur fichiers :









