#import de toutes lew variables et fonctions des fichiers ci-dessous
from get_data import *
from common_functions import *

import pandas as pd
import re
import unicodedata

#Voici les étapes à suivre pour rendre les données utilisables dans le dashboard : 

#1ere étape : renommer les colonnes des différents df pour plus de clarté
#2eme étape : normaliser les noms des villes dans CODGEO_com et df_effectifs (-> devenir identiques)
#3eme étape : normaliser les numéros département dans df_CODGEO_com
#4eme étape : normaliser les numéros département dans df_effectifs
#5eme étape : créer un identifiant de type 60GOUVIEUX dans df_effectifs
#6eme étape : créer un identifiant de type 60GOUVIEUX dans df_CODGEO_com
#7eme étape : créer dictionnaire avec clés = identifiants villes et valeurs = cogdeo
#8eme étape : attribuer un codgeo à chaque ville de df_effectifs à l'aide du dictionnaire et de l'identifiant clé des communes
#9eme étape : faire l'intervalle des villes disponibles dans df_data_delits et df_effectifs à l'aide du codgeo et de l'année
#10eme étape : concaténer les différents df obtenus avec les différentes années en 1 seul df pour les délits et les effectifs



#1ere étape : renommer les colonnes des différents df pour plus de clarté 

#effectifs_2016.columns[0] = colonne numéro département
#effectifs_2016.columns[1] correspond à la colonne qui contient le nom des villes (2eme colonne), on renomme par Nom Ville
#inplace = True permet de modifier directement le dataframe sans créer de nouvelle copie

#pour 2018 : num departement colonne 1 (pas entre parentheses) et nom ville = colonne 4

#pas d'automatisation avec un for car formats de données différentes selon les années 
df_effectifs_2016.rename(columns={df_effectifs_2016.columns[0]: 'Dep'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[0] : 'Dep'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[0]: 'Dep'}, inplace=True)

df_effectifs_2016.rename(columns={df_effectifs_2016.columns[1]: 'Nom Ville'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[1] : 'Nom Ville'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[3]: 'Nom Ville'}, inplace=True)




#2eme étape : normaliser les noms des villes dans CODGEO_com et df_effectifs (-> devenir identiques)

#ligne qui nous intéresse dans df_CODGEO_com = "NCC", il contient les noms des villes en majuscule et 'COM' qui contient les codgeo
#ligne qui nous intéresse dans effectifs_2016 = "Nom Ville", il contient les noms des villes (différents formats de noms : majuscule, minuscule, caractères spéciaux etc)
#il faut maintenant ajouter une colonne dans effectifs_2016 qui attribue le codgeo de la commune sur une ligne (dans les df_effectifs, il n'y a pas les coedgeo donc il faut les rajouter nous-même)
#pour cela on peut creer un dictionnaire à l'aide CODGEO_com qui contient les un identifiant pour chaque ville en tant que clé et le codgeo en valeur  
#ensuite faire matcher cet identifiant (clé) avec un identifiant dans un df_effetifs (si identifiants identiques alors c'est la même ville donc attribuer codgeo correspondant)

#il faut que les noms des villes coincident donc tout mettre en majuscule et supprimer la partie entre () de la colonne Nom Ville
#ne pas oublier de supprimer caractères spéciaux comme * par exemple et toutes les "anomalies"
#attention conserver le DE car souvent utilisé dans codgeo et voir tous les caractères spéciaux qui trainent
#on normalise les noms de villes à l'aide de transformer_ville_effectifs (voir common_functions.py)



for df in liste_df_effectifs : 
    #problème d'encodage des caractères spéciaux à la lecture du df
    df['Nom Ville'] = df['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
    df['Nom Ville'] = df['Nom Ville'].apply(transformer_ville_effectifs)
    #il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
    df['Dep'] = df['Dep'].astype(str)



#voir ligne 3043 2 villes dans 1 case
#touquet paris plage écrit touquet dans effectifs_2016
#a voir si / ecrit avec des espaces ou non

#On remarque qu'il y a des doublons au niveau du nom des villes, il faut donc créer un identifiant unique pour chaque ville
#on fait cela en concaténant le non de ville avec le numéro du département qui est disponible dans les df_effectifs et le df_CODGEO_com 
#on aura un identifiant de la forme 60GOUVIEUX
#faire cela dans les df_effectifs et dans le df_CODGEO_com
#concernant les différences liées à l'orthographe, je peux pas faire grand chose, il y aura des villes avec des données non utilisables mais 
#cela reste très minoritaire donc on va se contenter de ce que l'on a déjà



'''
#vérification de doublons dans les colonnes ci-dessous, il n'y en a pas donc il n'y aura pas de 'clé : valeur' identiques dans le dico

CODGEO_NCC_COM = pd.DataFrame(CODGEO_com["NCC"],["COM"])
doublons = CODGEO_NCC_COM.duplicated()
print(doublons) #retourne false donc pas de doublons

'''




#3eme étape : normaliser les numéros département dans df_CODGEO_com

#convertir les colonnes DEP et COMPARENT en string (attention comparent devient des nombres flottants et DEP devient 01 au lieu de 1)
df_CODGEO_com['DEP'] = df_CODGEO_com['DEP'].astype(str)
df_CODGEO_com['COMPARENT'] = df_CODGEO_com['COMPARENT'].astype(str)


#certains CODGEO tels que 1015 sont écrits 01015 donc supp_zero permet de transformer 01015 en 1015
#indispensable car codgeo écrit 1015 dans df_data_delits
df_CODGEO_com['COM'] = df_CODGEO_com['COM'].apply(suppr_zero)


#il y a certaines villes qui ont fusionné -> problème au niveau codgeo
#certaines villes peuvent ainsi avoir le même codgeo ou non donc 'COMPARENT' spécifie le codgeo avec laquelle la ville a fusionné
#donc si une ville a un codgeo = 1097 et que le comparent est 1453 sur la même ligne, alors la ville de codgeo 1097 a fusionné avec celle de codgeo 1453 mais le codgeo reste différent
#dans certains cas, le codgeo sera identiques pour plusieurs villes avec des noms différents
#dans les lignes où la colonne 'COMPARENT' contient un numéro, il n'y a pas de données dans la colonne 'DEP' 
#un codgeo contient le numéro du département en début de chaine de caractère, on se sert donc du codgeo de comparent pour attribuer un numéro de département à la commune
#on aurait pu vérifier les lignes pour lesquelles 'DEP' is None et prendre le codgeo de la colonne 'COM' (qui contient le codgeo de la commune) mais on a préféré prendre le codgeo de 'COMPARENT' au cas où il y aurait des différences au niveau du département entre les différentes communes
#dans les 2 cas le code est très similaire et celui-ci est fonctionnel donc on le garde tel quel
#mettre le numéro du département dans la colonne DEP de df_CODGEO_com
for index, row in df_CODGEO_com.iterrows():
    if row['COMPARENT'] != "nan": 
        #Mettre à jour le df directement sinon modifications pas prise en compte    
        df_CODGEO_com.at[index, 'DEP'] = transform_dep(row['COMPARENT'])  
        #print(row[''])




#4eme étape : normaliser les numéros département dans df_effectifs

#on souhaite attribuer un numéro de département sur chaque ligne pour chaque commune
for df in liste_df_effectifs : 
    df['Numero Departement'] = df['Dep'].apply(ecrire_departements)

#exception pour 2018, les départements sont de la forme 1,2,3.. et non 01,02,03.. donc changer ca
df_effectifs_2018['Numero Departement'] = df_effectifs_2018['Numero Departement'].apply(add_zero)




#5eme étape : créer un identifiant de type 60GOUVIEUX dans df_effectifs

#création d'une nouvelle colonne contenant l'identifiant unique en faisant la concaténation du numéro département et du nom de commune 
for df in liste_df_effectifs : 
    df['Numero Departement x Nom Ville'] = df['Numero Departement'] + df['Nom Ville']




#6eme étape : créer un identifiant de type 60GOUVIEUX dans df_CODGEO_com

#maintenant faire de meme pour codgeo_com
df_CODGEO_com['Numero Departement x Nom Ville'] = df_CODGEO_com['DEP'] + df_CODGEO_com['NCC']




#7eme étape : créer dictionnaire avec clés = identifiants villes et valeurs = cogdeo

#creer dictionnaire avec clés = l'identifiant des villes (nom+num_dep) et valeurs = numero codgeo
dictionnaire_codgeo = df_CODGEO_com.set_index('Numero Departement x Nom Ville')['COM'].to_dict()




#8eme étape : attribuer un codgeo à chaque ville de df_effectifs à l'aide du dictionnaire et de l'identifiant clé des communes

for df in liste_df_effectifs : 
    df['CODGEO'] = df['Numero Departement x Nom Ville'].map(dictionnaire_codgeo)

#recherche de doublons
#pas de doublons trouvés
'''
doublons = effectifs_2016[effectifs_2016['Nom Ville'].duplicated(keep=False)]

for ville in doublons['Nom Ville'] : 
    if ville != "NAN" :
        print(ville)
'''
'''
doublons_codgeo = CODGEO_com[CODGEO_com['NCC'].duplicated(keep=False)]

for ville in doublons_codgeo['NCC'][0:100] : 
    if ville != "NAN" :
        print(ville)
'''


#9eme étape : faire l'intervalle des villes disponibles dans df_data_delits et df_effectifs à l'aide du codgeo et de l'année

#reste plus qu'a faire l'intervalle entre le CODGEO du dataframe avec les délits et celui avec les efffectifs
#ainsi garder seulement les communes pour lesquelles toutes les données sont dispo (nombres et types de délits et effectifs policiers)

#colonne avec les CODGEO dans le csv avec tous les délits : CODGEO_2024


#décommenter pour rendre les données filtrées

#print(data_delits.columns)
df_data_delits['CODGEO_2024'] = df_data_delits['CODGEO_2024'].astype(str)


# Comparer les colonnes DEP et COMPARENT, et ne garder que les lignes où les valeurs des codgeos sont identiques
df_intersection_delits_2016 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2016['CODGEO'])) &
    (df_data_delits['annee'] == 16)
]
# print(df_intersection_delits_2016)

df_intersection_delits_2017 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2017['CODGEO'])) &
    (df_data_delits['annee'] == 17)
]
# print(df_intersection_delits_2017)

df_intersection_delits_2018 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2018['CODGEO'])) &
    (df_data_delits['annee'] == 18)
]
# print(df_intersection_delits_2018)
#df_intersection_2018.to_csv("C:\\Users\\Guillaume\\Downloads\\df_intersection_2018,1.csv", index=False)

df_intersection_delits_2016.to_csv("data\\cleaned\\delits_2016.csv", index=False)
df_intersection_delits_2017.to_csv("data\\cleaned\\delits_2017.csv", index=False)
df_intersection_delits_2018.to_csv("data\\cleaned\\delits_2018.csv", index=False)

df_intersection_effectifs_2016 = df_effectifs_2016[df_effectifs_2016['CODGEO'].isin(df_data_delits['CODGEO_2024'])]
print("voici ce que je veux")
print(df_intersection_effectifs_2016)
print(df_effectifs_2016)
#dupliquer pour les 2 autres années et créer effectifs_total
df_intersection_effectifs_2017 = df_effectifs_2017[df_effectifs_2017['CODGEO'].isin(df_data_delits['CODGEO_2024'])]
df_intersection_effectifs_2018 = df_effectifs_2018[df_effectifs_2016['CODGEO'].isin(df_data_delits['CODGEO_2024'])]

# mettre en csv les données nettoyés dans cleaned
df_intersection_effectifs_2016.to_csv("data\\cleaned\\effectifs_2016.csv", index=False)
df_intersection_effectifs_2017.to_csv("data\\cleaned\\effectifs_2017.csv", index=False)
df_intersection_effectifs_2018.to_csv("data\\cleaned\\effectifs_2018.csv", index=False)



# #10eme étape : concaténer les différents df obtenus avec les différentes années en 1 seul df pour les délits et les effectifs

# # Concaténation des DataFrames le long des lignes (axis=0)
delits_total = pd.concat([df_intersection_delits_2016, df_intersection_delits_2017, df_intersection_delits_2018], axis=0, ignore_index=True)
# #effectifs_total.to_csv("C:\\Users\\Guillaume\\Downloads\\effectif_total2.csv", index=False)
effectifs_total = pd.concat([df_intersection_effectifs_2016,df_intersection_effectifs_2017,df_intersection_effectifs_2018])
print(effectifs_total)


