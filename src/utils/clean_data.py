# import de toutes lew variables et fonctions des fichiers ci-dessous
from get_data import *
from common_functions import *

import pandas as pd
import re
import unicodedata

# Voici les étapes à suivre pour rendre les données utilisables dans le dashboard : 

# 1ere étape : renommer les colonnes des différents df pour plus de clarté
# 2eme étape : normaliser les noms des villes dans CODGEO_com et df_effectifs (-> devenir identiques)
# 3eme étape : normaliser les numéros département dans df_CODGEO_com
# 4eme étape : normaliser les numéros département dans df_effectifs
# 5eme étape : créer un identifiant de type 60GOUVIEUX dans df_effectifs
# 6eme étape : créer un identifiant de type 60GOUVIEUX dans df_CODGEO_com
# 7eme étape : créer dictionnaire avec clés = identifiants villes et valeurs = cogdeo
# 8eme étape : attribuer un codgeo à chaque ville de df_effectifs à l'aide du dictionnaire et de l'identifiant clé des communes
# 9eme étape : faire l'intervalle des villes disponibles dans df_data_delits et df_effectifs à l'aide du codgeo et de l'année
# 10eme étape : concaténer les différents df obtenus avec les différentes années en 1 seul df pour les délits et les effectifs
# 11eme étape : créer différents df pour rendre les données plus pertinentes et utilisables



# 1ere étape : renommer les colonnes des différents df pour plus de clarté 

# effectifs_2016.columns[0] = colonne numéro département
# effectifs_2016.columns[1] correspond à la colonne qui contient le nom des villes (2eme colonne), on renomme par Nom Ville
# inplace = True permet de modifier directement le dataframe sans créer de nouvelle copie

# pour 2018 : num departement colonne 1 (pas entre parentheses) et nom ville = colonne 4

# pas d'automatisation avec un for car formats de données différentes selon les années 
df_effectifs_2016.rename(columns={df_effectifs_2016.columns[0]: 'Dep'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[0] : 'Dep'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[0]: 'Dep'}, inplace=True)

df_effectifs_2016.rename(columns={df_effectifs_2016.columns[1]: 'Nom Ville'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[1] : 'Nom Ville'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[3]: 'Nom Ville'}, inplace=True)




# 2eme étape : normaliser les noms des villes dans CODGEO_com et df_effectifs (-> devenir identiques)

# ligne qui nous intéresse dans df_CODGEO_com = "NCC", il contient les noms des villes en majuscule et 'COM' qui contient les codgeo
# ligne qui nous intéresse dans effectifs_2016 = "Nom Ville", il contient les noms des villes (différents formats de noms : majuscule, minuscule, caractères spéciaux etc)
# il faut maintenant ajouter une colonne dans effectifs_2016 qui attribue le codgeo de la commune sur une ligne (dans les df_effectifs, il n'y a pas les coedgeo donc il faut les rajouter nous-même)
# pour cela on peut creer un dictionnaire à l'aide CODGEO_com qui contient les un identifiant pour chaque ville en tant que clé et le codgeo en valeur  
# ensuite faire matcher cet identifiant (clé) avec un identifiant dans un df_effetifs (si identifiants identiques alors c'est la même ville donc attribuer codgeo correspondant)

# il faut que les noms des villes coincident donc tout mettre en majuscule et supprimer la partie entre () de la colonne Nom Ville
# ne pas oublier de supprimer caractères spéciaux comme * par exemple et toutes les "anomalies"
# attention conserver le DE car souvent utilisé dans codgeo et voir tous les caractères spéciaux qui trainent
# on normalise les noms de villes à l'aide de transformer_ville_effectifs (voir common_functions.py)



for df in liste_df_effectifs : 
    #problème d'encodage des caractères spéciaux à la lecture du df
    df['Nom Ville'] = df['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
    df['Nom Ville'] = df['Nom Ville'].apply(transformer_ville_effectifs)
    #il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
    df['Dep'] = df['Dep'].astype(str)



# voir ligne 3043 2 villes dans 1 case
# touquet paris plage écrit touquet dans effectifs_2016
# a voir si / ecrit avec des espaces ou non

# On remarque qu'il y a des doublons au niveau du nom des villes, il faut donc créer un identifiant unique pour chaque ville
# on fait cela en concaténant le non de ville avec le numéro du département qui est disponible dans les df_effectifs et le df_CODGEO_com 
# on aura un identifiant de la forme 60GOUVIEUX
# faire cela dans les df_effectifs et dans le df_CODGEO_com
# concernant les différences liées à l'orthographe, je peux pas faire grand chose, il y aura des villes avec des données non utilisables mais 
# cela reste très minoritaire donc on va se contenter de ce que l'on a déjà



'''
#vérification de doublons dans les colonnes ci-dessous, il n'y en a pas donc il n'y aura pas de 'clé : valeur' identiques dans le dico

CODGEO_NCC_COM = pd.DataFrame(CODGEO_com["NCC"],["COM"])
doublons = CODGEO_NCC_COM.duplicated()
print(doublons) #retourne false donc pas de doublons

'''




# 3eme étape : normaliser les numéros département dans df_CODGEO_com

# convertir les colonnes DEP et COMPARENT en string (attention comparent devient des nombres flottants et DEP devient 01 au lieu de 1)
df_CODGEO_com['DEP'] = df_CODGEO_com['DEP'].astype(str)
df_CODGEO_com['COMPARENT'] = df_CODGEO_com['COMPARENT'].astype(str)


# certains CODGEO tels que 1015 sont écrits 01015 donc supp_zero permet de transformer 01015 en 1015
# indispensable car codgeo écrit 1015 dans df_data_delits
df_CODGEO_com['COM'] = df_CODGEO_com['COM'].apply(suppr_zero)


# il y a certaines villes qui ont fusionné -> problème au niveau codgeo
# certaines villes peuvent ainsi avoir le même codgeo ou non donc 'COMPARENT' spécifie le codgeo avec laquelle la ville a fusionné
# donc si une ville a un codgeo = 1097 et que le comparent est 1453 sur la même ligne, alors la ville de codgeo 1097 a fusionné avec celle de codgeo 1453 mais le codgeo reste différent
# dans certains cas, le codgeo sera identiques pour plusieurs villes avec des noms différents
# dans les lignes où la colonne 'COMPARENT' contient un numéro, il n'y a pas de données dans la colonne 'DEP' 
# un codgeo contient le numéro du département en début de chaine de caractère, on se sert donc du codgeo de comparent pour attribuer un numéro de département à la commune
# on aurait pu vérifier les lignes pour lesquelles 'DEP' is None et prendre le codgeo de la colonne 'COM' (qui contient le codgeo de la commune) mais on a préféré prendre le codgeo de 'COMPARENT' au cas où il y aurait des différences au niveau du département entre les différentes communes
# dans les 2 cas le code est très similaire et celui-ci est fonctionnel donc on le garde tel quel
# mettre le numéro du département dans la colonne DEP de df_CODGEO_com
for index, row in df_CODGEO_com.iterrows():
    if row['COMPARENT'] != "nan": 
        #Mettre à jour le df directement sinon modifications pas prise en compte    
        df_CODGEO_com.at[index, 'DEP'] = transform_dep(row['COMPARENT'],6)  
        #print(row[''])



# 4eme étape : normaliser les numéros département dans df_effectifs

# on souhaite attribuer un numéro de département sur chaque ligne pour chaque commune
for df in liste_df_effectifs : 
    df['Numero Departement'] = df['Dep'].apply(ecrire_departements)

# exception pour 2018, les départements sont de la forme 1,2,3.. et non 01,02,03.. donc changer ca
df_effectifs_2018['Numero Departement'] = df_effectifs_2018['Numero Departement'].apply(add_zero)




# 5eme étape : créer un identifiant de type 60GOUVIEUX dans df_effectifs

# création d'une nouvelle colonne contenant l'identifiant unique en faisant la concaténation du numéro département et du nom de commune 
for df in liste_df_effectifs : 
    df['Numero Departement x Nom Ville'] = df['Numero Departement'] + df['Nom Ville']




# 6eme étape : créer un identifiant de type 60GOUVIEUX dans df_CODGEO_com

# maintenant faire de meme pour codgeo_com
df_CODGEO_com['Numero Departement x Nom Ville'] = df_CODGEO_com['DEP'] + df_CODGEO_com['NCC']




# 7eme étape : créer dictionnaire avec clés = identifiants villes et valeurs = cogdeo

#creer dictionnaire avec clés = l'identifiant des villes (nom+num_dep) et valeurs = numero codgeo
dictionnaire_codgeo = df_CODGEO_com.set_index('Numero Departement x Nom Ville')['COM'].to_dict()




# 8eme étape : attribuer un codgeo à chaque ville de df_effectifs à l'aide du dictionnaire et de l'identifiant clé des communes

for df in liste_df_effectifs : 
    df['CODGEO'] = df['Numero Departement x Nom Ville'].map(dictionnaire_codgeo)

# recherche de doublons
# pas de doublons trouvés
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


# 9eme étape : faire l'intervalle des villes disponibles dans df_data_delits et df_effectifs à l'aide du codgeo et de l'année

# reste plus qu'a faire l'intervalle entre le CODGEO du dataframe avec les délits et celui avec les efffectifs
# ainsi garder seulement les communes pour lesquelles toutes les données sont dispo (nombres et types de délits et effectifs policiers)

# colonne avec les CODGEO dans le csv avec tous les délits : CODGEO_2024


# décommenter pour rendre les données filtrées

# print(data_delits.columns)
df_data_delits['CODGEO_2024'] = df_data_delits['CODGEO_2024'].astype(str)

# créer une nouvelle colonne departement pour stocker l'information du département
# lambda texte sert à spécifier que df_data_delits['CODGEO_2024'] est le parametre "texte" de la fonction et 4 est précisé comme chiffre
df_data_delits['departement'] = df_data_delits['CODGEO_2024'].apply(lambda texte: transform_dep(texte, 4))
# print(df_data_delits)

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
# df_intersection_2018.to_csv("C:\\Users\\Guillaume\\Downloads\\df_intersection_2018,1.csv", index=False)

# Remplir les valeurs manquantes avec 0
df_intersection_delits_2016 = df_intersection_delits_2016.fillna(0)
df_intersection_delits_2017 = df_intersection_delits_2017.fillna(0)
df_intersection_delits_2018 = df_intersection_delits_2018.fillna(0)


# df_intersection_delits_2016.to_csv("data\\cleaned\\delits_2016.csv", index=False)
# df_intersection_delits_2017.to_csv("data\\cleaned\\delits_2017.csv", index=False)
# df_intersection_delits_2018.to_csv("data\\cleaned\\delits_2018.csv", index=False)


# faire la même intersection avec les effectifs
df_intersection_effectifs_2016 = df_effectifs_2016[df_effectifs_2016['CODGEO'].isin(df_data_delits['CODGEO_2024'])]
df_intersection_effectifs_2017 = df_effectifs_2017[df_effectifs_2017['CODGEO'].isin(df_data_delits['CODGEO_2024'])]
df_intersection_effectifs_2018 = df_effectifs_2018[df_effectifs_2016['CODGEO'].isin(df_data_delits['CODGEO_2024'])]



# renommer les colonnes pour plus de lisibilité : 
# print(df_intersection_effectifs_2016.columns)
# print(df_intersection_effectifs_2018.columns)
new_columns_names_effectifs_2016 = ['Dep','Nom Ville','Nombre de policiers municipaux','Nombre d ASVP','Nombre de gardes-champêtres','Nombre d agents cynophiles','Nombre de chiens de patrouille de police municipale','Numero Departement','Numero Departement x Nom Ville','CODGEO']
new_columns_names_effectifs_2017 = ['Dep','Nom Ville','Nombre d habitants','Nombre de policiers municipaux','Nombre d ASVP','Nombre de gardes-champêtres','Nombre de maîtres chiens de police municipale','Nombre de chiens de patrouille de police municipale','Numero Departement','Numero Departement x Nom Ville','CODGEO']
new_columns_names_effectifs_2018 = ['Dep','Nom Département','Inconnu','Nom Ville','Nombre d habitants','Nombre de policiers municipaux','Nombre d ASVP','Nombre de gardes-champêtres','Nombre de maîtres chiens de police municipale','Nombre de chiens de patrouille de police municipale','Numero Departement','Numero Departement x Nom Ville','CODGEO']




# print(len(df_intersection_effectifs_2016.columns))
# print(len(df_intersection_effectifs_2017.columns))
# print(len(df_intersection_effectifs_2018.columns))
df_intersection_effectifs_2016.columns = new_columns_names_effectifs_2016
df_intersection_effectifs_2017.columns = new_columns_names_effectifs_2017
df_intersection_effectifs_2018.columns = new_columns_names_effectifs_2018

# supprimer les totaux à la fin de chaque département dans intersection_effectifs_2018

df_intersection_effectifs_2018 = df_intersection_effectifs_2018[~df_intersection_effectifs_2018['Dep'].str.contains('TOTAL', case=False, na=False)]

# supprimer les données qui ne sont pas en commun pour les effectifs de police a part la population des villes qui n'est pas disponible dans le 2016

# pour 2016
# axis = 1 pour préciser que l'on supprime 1 colonne (vertical)
df_intersection_effectifs_2016 = df_intersection_effectifs_2016.drop('Nombre d agents cynophiles', axis = 1)

# pour 2017
df_intersection_effectifs_2017 = df_intersection_effectifs_2017.drop('Nombre de maîtres chiens de police municipale', axis = 1)

# pour 2018
# garder Nom département car sinon aucune précision sur celui-ci dans le df (le nom de dep est présent dans la colonne Dep des années 2016 et 2017)
df_intersection_effectifs_2018 = df_intersection_effectifs_2018.drop('Inconnu', axis = 1)
df_intersection_effectifs_2018 = df_intersection_effectifs_2018.drop('Nombre de maîtres chiens de police municipale', axis = 1)

# ajout de colonnes année pour avoir cette information après concaténation
df_intersection_effectifs_2016['Année'] = 2016
df_intersection_effectifs_2017['Année'] = 2017
df_intersection_effectifs_2018['Année'] = 2018


# Remplir les valeurs manquantes avec 0
df_intersection_effectifs_2016 = df_intersection_effectifs_2016.fillna(0)
df_intersection_effectifs_2017 = df_intersection_effectifs_2017.fillna(0)
df_intersection_effectifs_2018 = df_intersection_effectifs_2018.fillna(0)

# mettre en csv les données nettoyées dans cleaned
# df_intersection_effectifs_2016.to_csv("data\\cleaned\\effectifs_2016.csv", index=False)
# df_intersection_effectifs_2017.to_csv("data\\cleaned\\effectifs_2017.csv", index=False)
# df_intersection_effectifs_2018.to_csv("data\\cleaned\\effectifs_2018.csv", index=False)

# 10eme étape : concaténer les différents df obtenus avec les différentes années en 1 seul df pour les délits et les effectifs


# # Concaténation des DataFrames le long des lignes (axis=0)
delits_total = pd.concat([df_intersection_delits_2016, df_intersection_delits_2017, df_intersection_delits_2018], axis=0, ignore_index=True)
effectifs_total = pd.concat([df_intersection_effectifs_2016, df_intersection_effectifs_2017, df_intersection_effectifs_2018], ignore_index=True)


# 11eme étape : créer différents df pour rendre les données plus pertinentes et utilisables

# ne garder que les villes pour lesquelles on a des données sur 3 ans
effectifs_total = effectifs_total.groupby('CODGEO').filter(lambda x: len(x) != 1)

effectifs_total_cols = effectifs_total[['Nombre de policiers municipaux', 
                                        'Nombre d ASVP',
                                        'Nombre de gardes-champêtres',
                                        'Nombre de chiens de patrouille de police municipale']]


# converti ces colonnes en ignorant les erreurs (de object à float/int) sinon toutes les valeurs ne sont pas forcément prises en compte
effectifs_total[effectifs_total_cols.columns] = effectifs_total_cols.apply(pd.to_numeric, errors="coerce")
effectifs_total["Nombre d habitants"] = pd.to_numeric(effectifs_total["Nombre d habitants"], errors="coerce")
effectifs_total["CODGEO"] = pd.to_numeric(effectifs_total["CODGEO"], errors="coerce")



# Remplir les valeurs manquantes avec 0
effectifs_2016 = df_intersection_effectifs_2016.fillna(0)
effectifs_2017 = df_intersection_effectifs_2017.fillna(0)
effectifs_2018 = df_intersection_effectifs_2018.fillna(0)
effectifs_total = effectifs_total.fillna(0)



effectifs_total_cols = effectifs_total[['Nombre de policiers municipaux', 
                                        'Nombre d ASVP',
                                        'Nombre de gardes-champêtres',
                                        'Nombre de chiens de patrouille de police municipale']]


# converti tous les types des colonnes en int64
effectifs_total_cols = effectifs_total_cols.astype({col: 'int64' for col in effectifs_total_cols.select_dtypes(include='float64').columns})
effectifs_total = effectifs_total.astype({col: 'int64' for col in effectifs_total_cols.select_dtypes(include='float64').columns})


# Préparer les données par département et par année
effectifs_par_dept_annee = effectifs_total.groupby(["Numero Departement", "Année"]).agg({
    col: "sum" for col in effectifs_total_cols.columns
}).reset_index()


# faire la somme sur la ligne : 
effectifs_par_dept_annee['somme_ligne'] = effectifs_par_dept_annee.drop(['Numero Departement', 'Année'], axis=1).sum(axis=1)


# Convertir les numéros de département en chaînes pour correspondre au format de Plotly
effectifs_par_dept_annee["Numero Departement"] = effectifs_par_dept_annee["Numero Departement"].astype(str).str.zfill(2)


effectifs_total_pop = effectifs_total[effectifs_total['Année'] != 2016]

effectifs_par_commune_annee = effectifs_total_pop.groupby(["CODGEO","Année","Nombre d habitants"]).agg({
    col: "sum" for col in effectifs_total_cols.columns
}).reset_index()


print(effectifs_par_commune_annee)

effectifs_par_commune_sorted = effectifs_total_pop.sort_values(by='Nombre d habitants')

print(effectifs_par_commune_sorted)




# ne garder que les villes pour lesquelles on a des données sur 3 ans
delits_total = delits_total.groupby('CODGEO_2024').filter(lambda x: len(x) == 3)

# Réorganiser le tableau avec CODGEO_2024, POP et année comme index et les délits en colonnes
delits_pivot_2016 = df_intersection_delits_2016.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')
delits_pivot_2017 = df_intersection_delits_2017.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')
delits_pivot_2018 = df_intersection_delits_2018.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')


# créer des colonnes avec les index
delits_pivot_2016 = delits_pivot_2016.reset_index()
delits_pivot_2017 = delits_pivot_2017.reset_index()
delits_pivot_2018 = delits_pivot_2018.reset_index()


# Remplir les valeurs manquantes avec 0
delits_pivot_2016 = delits_pivot_2016.fillna(0)
delits_pivot_2017 = delits_pivot_2017.fillna(0)
delits_pivot_2018 = delits_pivot_2018.fillna(0)


# conversion des types (pas forcément nécessaire)
delits_pivot_2016 = delits_pivot_2016.astype({col: 'int64' for col in delits_pivot_2016.select_dtypes(include='float64').columns})
delits_pivot_2017 = delits_pivot_2017.astype({col: 'int64' for col in delits_pivot_2017.select_dtypes(include='float64').columns})
delits_pivot_2018 = delits_pivot_2018.astype({col: 'int64' for col in delits_pivot_2018.select_dtypes(include='float64').columns})


# concaténation des années
delits_pivot_total = pd.concat([delits_pivot_2016,delits_pivot_2017,delits_pivot_2018],ignore_index=True)

# ne garder que les villes pour lesquelles on a des données sur 3 ans
delits_pivot_total = delits_pivot_total.groupby('CODGEO_2024').filter(lambda x: len(x) == 3)

# rassembler les colonnes qui contiennent les informations pertinentes (nombre de faits et classes)
delits_pivot_total_cols = delits_pivot_total[['Autres coups et blessures volontaires','Cambriolages de logement',
       'Coups et blessures volontaires',
       'Coups et blessures volontaires intrafamiliaux',
       'Destructions et dégradations volontaires', 'Trafic de stupéfiants',
       'Usage de stupéfiants', 'Violences sexuelles', 'Vols avec armes',
       'Vols d\'accessoires sur véhicules', 'Vols dans les véhicules',
       'Vols de véhicules', 'Vols sans violence contre des personnes',
       'Vols violents sans arme']]


delits_par_dept_annee = delits_pivot_total.groupby(["departement","annee"]).agg({
    col: "sum" for col in delits_pivot_total_cols.columns
}).reset_index()

#convertir CODGEO_2024 en int sinon groupby impossible pour les codgeo a 4 chiffres
delits_pivot_total['CODGEO_2024'] = delits_pivot_total['CODGEO_2024'].astype(int)
print(delits_pivot_total['CODGEO_2024'].dtypes)

delits_par_commune_annee = delits_pivot_total.groupby(["CODGEO_2024","annee","POP"]).agg({
    col: "sum" for col in delits_pivot_total_cols.columns
}).reset_index()



# faire la somme sur la ligne pour déterminer l'ensemble des délits
delits_par_commune_annee['somme_ligne'] = delits_par_commune_annee.drop(['annee','CODGEO_2024','POP'], axis=1).sum(axis=1)
delits_par_dept_annee['somme_ligne'] = delits_par_dept_annee.drop(['departement','annee'], axis=1).sum(axis=1)

# trier les communes par ordre croissant population
delits_par_commune_annee_sorted = delits_par_commune_annee.sort_values(by='POP')

# Convertir les numéros de département en chaînes pour correspondre au format de Plotly
delits_par_dept_annee["departement"] = delits_par_dept_annee["departement"].astype(str).str.zfill(2)


# Regrouper les communes selon des intervalles de population
population_bins = [0, 1000, 2000, 5000, 10000, 20000, 30000, 40000, 50000, 70000, 100000, 200000, 500000, 1000000]
population_labels = ["0-1k","1k-2k","2k-5k","5k-10k","10k-20k", "20k-30k", "30k-40k", "40k-50k", "50k-70k","70k-100k","100k-200k","200k-500k","500k-1M"]


# Ajouter une colonne 'intervalle_population' pour les intervalles de population
delits_par_commune_annee['intervalle_population'] = pd.cut(
    delits_par_commune_annee['POP'], 
    bins=population_bins, 
    labels=population_labels, 
    right=False
)

# Dupliquer les données pour chaque année (2016, 2017, 2018)
# Crée une nouvelle colonne 'annee' et duplique les lignes pour chaque année
# delits_par_commune_annee['annee'] = delits_par_commune_annee['annee'].astype(int)

# Comptabilise le nombre de délits pour chaque intervalle de population
# on fait cela en faisant la somme de somme_ligne
# et on créer une colonne année qui renseigne l'année auquel appartient l'intervalle
delits_par_commune_annee_grouped = delits_par_commune_annee.groupby(
    ['annee', 'intervalle_population']
).agg(
    total_delits=('somme_ligne', 'sum'),  # fait la somme des délits par intervalle de population et année
    nombre_communes=('CODGEO_2024', 'size')  # compte le ombre de communes par intervalle et année
).reset_index()




# effectifs_total.to_csv("data\\cleaned\\effectifs_total.csv", index=False)
# effectifs_par_dept_annee.to_csv("data\\cleaned\\effectifs_par_dept_annee.csv", index=False)
# delits_total.to_csv("data\\cleaned\\delits_total.csv", index=False)
# delits_par_dept_annee.to_csv("data\\cleaned\\delits_par_dept_annee.csv", index=False)
# delits_par_commune_annee.to_csv("data\\cleaned\\delits_par_commune_annee.csv", index=False)
# delits_par_commune_annee_grouped.to_csv("data\\cleaned\\delits_par_commune_annee_grouped.csv", index=False)
# delits_par_commune_annee_sorted.to_csv("data\\cleaned\\delits_par_commune_annee_sorted.csv", index=False)


# print(delits_par_commune_annee)
# print(delits_par_dept_annee)
# print(effectifs_par_dept_annee)


