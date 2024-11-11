# DSIA4101A

**Introduction :**  
Ce projet a été réalisé en binôme par Romain Yerolymos et Guillaume Curtis. Ce projet cherche à montrer une corrélation entre le nombre de policiers municipaux et le nombre de délits commis. Il cherche aussi à montrer la corrélation entre la population et le nombre d'incidents commis.

# Sommaire 

## Data sets (jeux de données)
1. Introduction
2. Information sur les datas sets utilisés
3. Analyse de nos données

## User guide
1. Prérequi
2. Exportation du projet
3. Ouverture du dashboard
4. Utilisation du dashboard

## Guide du developpeur
1. Introduction
2. Organisation du code
3. Ajouter une page 
4. Améliorations possibles
---

# Data sets

## 1 - Introduction

Nous voulions à travers ces deux jeux de données savoir s'il y avait une corrélation entre les effectifs de la police municipale et les délits commis dans les villes. 

## 2 - Information sur les datas sets utilisés

Voici les liens des données utilisées :

https://www.data.gouv.fr/fr/datasets/police-municipale-effectifs-par-commune/#/community-reuses

https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources

Les données ont été trouvées sur le site Datagouv.fr, un site qui permet aux utilisateurs de trouver tout type de données sur la vie en France.

Le premier lien est le lien pour trouver les données des effectifs de police municipale en fonction des années et le deuxième permet de faire de même mais avec tous les délits commis dans les communes françaises.

## 3 - Analyse de nos données 

L'objectif de notre analyse était de déterminer un lien entre le nombre de policiers et le nombre de délits sur 3 ans d'intervalle. 

![image](https://github.com/user-attachments/assets/bc517f13-5c29-4ff2-9d94-f84bfca2f593)

Sur les cartes, nous pouvons observer une corrélation entre les départements les plus touchés par les délits et les départements où la présence policière est la plus élevée. Notamment dans le département des Bouches-du-Rhône. De plus, si nous faisons évoluer les années, on voit que la corrélation reste la même.

![image](https://github.com/user-attachments/assets/1a64c61a-d2e0-4720-8ce7-b839b32ed6c3)

Nous pouvons vérifier cette corrélation avec ce graphique qui montre la relation entre effectifs de police et nombre de délits. On observe que plus il y a de policiers, plus il y a de délits.

![image](https://github.com/user-attachments/assets/a492a30f-2d46-44d5-ae83-6ed97666abdf)




![image](https://github.com/user-attachments/assets/c9016cd1-d7ad-4913-99a1-ea60b3708fdb)


On observe sur ces deux graphiques une relation très intéressante, en effet la majorité des effectifs de police et des délits se trouvent dans des petites et moyennes villes, ce qui montre que la taille des villes n'est pas forcément proportionnelle au nombre de délits et au nombre de policiers présents dans la commune.





# User Guide 

Cette partie est destinée à l'importation de tous les fichiers depuis GitHub et à la visualisation de notre Dashboard.

## 1 - Prérequis 

Ce projet est entièrement réalisé en Python. Une version égale ou supérieure à 3.11 est vivement conseillée.
[Installer une version de python au moins égale à 3.11](https://www.python.org/downloads/)

Il faudra aussi avoir un compte sur Git-Hub

[Page d'acceuil Github](https://github.com/)

## 2 - Exportation du projet 


### Cloner le répertoire sur sa machine :
Pour ce faire, ouvrez ‘Git Bash’ (vous pouvez le chercher depuis la barre de recherche Windows). Rentrez la commande suivante dans ‘Git Bash’ :


```
git clone https://github.com/Guigoui/Projet_DSIA_40101A.git
```


### Installer les packages nécessaires au programme :

Pour ce faire, ouvrez l’‘Invite de Commandes’ (vous pouvez la chercher depuis la barre de recherche Windows). À l’aide de la commande ‘cd’, rejoignez votre dossier qui correspond au dossier cloné de Git.

```
cd path\to\your\Projet_DSIA_40101A
```


Enfin, depuis ce dossier, rentrez la commande suivante : 

```
python -m pip install -r requirements.txt
```


## 3 - Ouvrir le Dashboard 


Après avoir suivi toutes les étapes précédentes, il vous suffit de rentrer la commande suivante :
```
*python main.py*
```

Vous obtiendrez ensuite:

![image](https://github.com/user-attachments/assets/4a72750f-7073-4ec3-b40f-f7d8777f0cbc)

cliquez sur http://127.0.0.1:8050/

Et vous voilà sur notre dashboard.


## 4 - Utilisation du Dashboard 

Notre dashboard se présente sous cette forme-là :

![image](https://github.com/user-attachments/assets/d98509c4-4466-439e-97f1-24f155da2927)



Pour naviguer, il vous suffira de choisir l'onglet que vous voulez consulter et cliquer dessus. Puis dans la petite barre de recherche, choisissez ce que vous voulez observer. Et vous voilà prêt à utiliser notre dashboard.



# Guide du developpeur 

## Introduction 

Ce guide du développeur est conçu pour faciliter l'ajout de nouvelles fonctionnalités et de son amélioration.

## Organisation du code 

Notre code est structuré en plusieur fichiers :

**data** : contient toutes les données , repartie entre cleaned et brute (raw)

**src** : contient les scripts pour netoyer les données brutes.

**main.py** : permet de lancer et visualiser le dashbaord .



## Ajouter une page  

Il vous suffit d'aller dans main.py et de rajouter le dcc.tab que vous voulez .

![image](https://github.com/user-attachments/assets/d1abecc1-ed66-4914-9955-eef14d998f63)


Puis rajouter une condition d'apparition avec un elif 

![image](https://github.com/user-attachments/assets/df585033-ee68-485d-8a77-c98321f3e0c4)


## Amélioration possible 

- Ajouter plus d'années pour une étude plus détaillée de l'évolution des délits.
- Ajouter d'autres graphiques pour observer une tendance précise sur chaque département.
- Améliorer l'interface graphique.


# Copyright 

-Je déclare sur l’honneur que le code fourni a été produit par nous même.

  










