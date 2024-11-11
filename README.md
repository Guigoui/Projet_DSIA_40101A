# DSIA4101A

**Introduction :**  
Ce projet a étét réaliser en binome par Romain Yerolymos et Guillaume Curtis. 
Ce projet cherche à monter une corélation entre le nombre de policier municipaux et le nombre de délits commits. Il cherche aussi à montrer la corrélation entre la population et le nombre d'incidents commits.

# Sommaire 

## Data sets (jeux de données)
1. Introduction
2. Information sur les datas sets utilisés
3. Analyse de nos données

## User guide
1. Prérequis
2. Exportation du projet
3. Ouvrir le dashboard
4. Utilisation du dashboard

## Guide du developpeur
1. Introduction
2. Organisatio du code
3. Ajouter une page 
4. Améliorations possibles
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

## 3 - Analyse de nos données 

L'objetif de notre analyse était de determiné un lien entre nombre de policiers et nomre de délits sur 3 ans d'intervalle. 

![image](https://github.com/user-attachments/assets/bc517f13-5c29-4ff2-9d94-f84bfca2f593)

Sur les cartes nous pouvons observer une coorélations entre les departement les plus touchés par les délits et les département où la présence policière est la plus élevé.
Notament dans le depatement des bouches du rhone. 
De plus si nous faisons évoluer les années on voit que la corélation reste la même.

![image](https://github.com/user-attachments/assets/1a64c61a-d2e0-4720-8ce7-b839b32ed6c3)

Nous pouvons verifier cette corélations avec ce graphique qui montre la relation entre effectifs de police et nombre de délits.
On observe que plus il y a de policier plus il y a de délits. 

![image](https://github.com/user-attachments/assets/a492a30f-2d46-44d5-ae83-6ed97666abdf)




![image](https://github.com/user-attachments/assets/c9016cd1-d7ad-4913-99a1-ea60b3708fdb)


On observe sur ces deux graphqiues une relation trés intéressante , en effet la mqjorité des effectifs de polices et des délits se passent dans des petites et moyennes villes ce qui montre que la taille des villes n'est pas forcément proportionnelles au nombre de délits et au nombres de policier présents dans la commune.





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
git clone https://



### Installer les packages nécessaires au programme :

Pour ce faire, ouvrez l' ’Invite de Commandes’ (vous pouvez la chercher
depuis la barre de recherche windows). À l’aide de la commande ‘cd’ rejoignez
votre dossier ‘’ qui correspond au dossier
cloné de Git.

Enfin, depuis ce dossier, rentrez la commande suivante : 
python -m pip install -r requirements.txt

## 3 - Ouvrir le Dashboard 


Après avoir suivie tous les étapes précedentes il vous suffit de rentrer la commande suivante  :

```
*python main.py*
```

Vous obtiendrez ensuite:

![image](https://github.com/user-attachments/assets/4a72750f-7073-4ec3-b40f-f7d8777f0cbc)

cliquez sur http://127.0.0.1:8050/

et vous voilà sur notre dashboard.


## 4 - Utilisation du Dashboard 


![image](https://github.com/user-attachments/assets/d98509c4-4466-439e-97f1-24f155da2927)

Notre dashoard se présente sous cette forme là. 

Pour navigeur il vous suffira de choisir l'onglet que vous voulez consulter et cliquer dessus .
Puis dans la petite barre de recherche choissisez ce que vous voulez observer.
Et vous voilà prêt à utiliser notre dashboard.



# Guide du developpeur 

## Introduction 

Ce guide du developpeur est concue pour faciliter l'ajout de nouvelles fonctionnalités et de son amélioration.

## Organisation du code 

Notre code est structuré en plusieur fichiers :

**data** : contient toutes les données , repartie entre cleaned et brute (raw)

**src** : contient les scripts pour netoyer les données brutes.

**main.py** : permet de lancer et visualiser le dashbaord .



## Ajouter une page  

Il vous suffit d'aller dans main.py et de rajouter le dcc.tab que vous voulez .

![image](https://github.com/user-attachments/assets/d1abecc1-ed66-4914-9955-eef14d998f63)


Puis rajouter un ça conditiont d'apparitions avec un elif 

![image](https://github.com/user-attachments/assets/df585033-ee68-485d-8a77-c98321f3e0c4)


## Amélioration possible 

- Ajouter plus d'années pour une études plus détaller de l'évolution des délits.
- Ajout d'autre graphique pour observer une tendance précise sur chaque dépatements.
- Améliorer l'interface graphique

  










