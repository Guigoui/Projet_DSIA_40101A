#import de toutes lew variables et fonctions des fichiers ci-dessous
from get_data import *
from common_functions import *

import pandas as pd
import re
import unicodedata




#effectifs_2016.columns[0] = colonne numéro département
#effectifs_2016.columns[1] correspond à la colonne qui contient le nom des villes (2eme colonne), on renomme par Nom Ville, inplace = True 
#permet de modifier directement le dataframe sans créer de nouvelle copie

#pour 2018 : num departement colonne 1 (pas entre parentheses) et nom ville colonne 4

#pas d'automatisation avec un for car formats de données différentes selon les années 
df_effectifs_2016.rename(columns={df_effectifs_2016.columns[0]: 'Dep'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[0] : 'Dep'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[0]: 'Dep'}, inplace=True)

df_effectifs_2016.rename(columns={df_effectifs_2016.columns[1]: 'Nom Ville'}, inplace=True)
df_effectifs_2017.rename(columns={df_effectifs_2017.columns[1] : 'Nom Ville'}, inplace=True)
df_effectifs_2018.rename(columns={df_effectifs_2018.columns[3]: 'Nom Ville'}, inplace=True)



#ligne qui nous intéresse dans CODGEO_com = "NCC", il contient les noms des villes en majuscule et 'COM' qui contient les codgeo
#ligne qui nous intéresse dans effectifs_2016 = "Nom Ville", il contient les noms des villes en majuscule
#il faut maintenant ajouter une colonne dans effectifs_2016 qui donne le codgeo de la commune sur la ligne
#pour cela on peut creer un dictionnaire à l'aide CODGEO_com qui contient les noms de villes en tant que clé et le codgeo en valeur

#il faut que les noms des villes coincident donc tout mettre en majuscule et supprimer la partie entre () de la colonne Nom Ville
#ne pas oublier de supprimer caractères spéciaux comme * par exemple et toutes les "anomalies"


'''
à supprimer si le for fonctionne
df_effectifs_2016['Nom Ville'] = df_effectifs_2016['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
df_effectifs_2017['Nom Ville'] = df_effectifs_2017['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
df_effectifs_2018['Nom Ville'] = df_effectifs_2018['Nom Ville'].str.encode('utf-8').str.decode('utf-8')

effectifs_2016['Nom Ville'] = effectifs_2016['Nom Ville'].apply(transformer_ville_effectifs)
effectifs_2017['Nom Ville'] = effectifs_2017['Nom Ville'].apply(transformer_ville_effectifs)
effectifs_2018['Nom Ville'] = effectifs_2018['Nom Ville'].apply(transformer_ville_effectifs)

#il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
effectifs_2016['Dep'] = effectifs_2016['Dep'].astype(str)
effectifs_2017['Dep'] = effectifs_2017['Dep'].astype(str)
effectifs_2018['Dep'] = effectifs_2018['Dep'].astype(str)
'''


for df in liste_df_effectifs : 
    df['Nom Ville'] = df['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
    df['Nom Ville'] = df['Nom Ville'].apply(transformer_ville_effectifs)
    #il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
    df['Dep'] = df['Dep'].astype(str)



#attention conserver le DE car souvent utilisé dans codgeo et voir tous les caractères spéciaux qui trainent
#voir ligne 3043 2 villes dans 1 case
#touquet paris plage écrit touquet dans effectifs_2016
#a voir si / ecrit avec des espaces ou non
#lorsqu'il y a des doublons, regarder le département dans effectifs, et comparer les valeurs codgeo, ne prendre que celle qui commence par le numéro du département
#prochaine étape récupérer le v_commune pour 2016 et comparer, si c'est toujours la même chose alors s'arreter la 
#concernant les différences liées à l'orthographe, je peux pas faire grand chose


#création d'un dictionnaire qui stocke la colonne NCC en tant que clé et la colonne COM en tant que valeur

'''
CODGEO_NCC_COM = pd.DataFrame(CODGEO_com["NCC"],["COM"])
doublons = CODGEO_NCC_COM.duplicated()
print(doublons) #retourne false donc pas de doublons

'''





#1ere étape : trouver le nom du département pour la ville dans effectifs et créer une nouvelle colonne de ce type 60GOUVIEUX


'''
# Fonction pour extraire les numéros de département
def extraire_numero_departement(texte):
    # Utilise une expression régulière pour détecter les numéros de département entre parenthèses
    match = re.search(r'\((\d{2})\)', texte)
    #si match NULL (aucun numéro de département trouvé) alors ne rien renvoyer
    if match:
        #group(0) renvoie tout le motif trouvé, même avec les parenthèses or group(1) renvoie 1er sous groupe donc sans parentheses
        #group indispensable car match contient des informations concernant le motif, pas le motif en lui-même
        return match.group(1)
    return None
'''


    
#convertir les colonnes DEP et COMPARENT en string (attention comparent devient des nombres flottants et DEP devient 01 au lieu de 1)
df_CODGEO_com['DEP'] = df_CODGEO_com['DEP'].astype(str)
df_CODGEO_com['COMPARENT'] = df_CODGEO_com['COMPARENT'].astype(str)

df_CODGEO_com['COM'] = df_CODGEO_com['COM'].apply(suppr_zero)



#mettre le numéro du département dans la colonne DEP de df_CODGEO_com
for index, row in df_CODGEO_com.iterrows():
    if row['COMPARENT'] != "nan": 
        df_CODGEO_com.at[index, 'DEP'] = transform_dep(row['COMPARENT'])  # Mettre à jour le DataFrame directement        
        #print(row['DEP'])



for df in liste_df_effectifs : 
    df['Numero Departement'] = df['Dep'].apply(ecrire_departements)

df_effectifs_2018['Numero Departement'] = df_effectifs_2018['Numero Departement'].apply(add_zero)

for df in liste_df_effectifs : 
    df['Numero Departement x Nom Ville'] = df['Numero Departement'] + df['Nom Ville']

#maintenant faire de meme pour codgeo_com
df_CODGEO_com['Numero Departement x Nom Ville'] = df_CODGEO_com['DEP'] + df_CODGEO_com['NCC']

#creer dictionnaire avec clés = l'identifiant des villes (nom+num_dep) et valeurs = numero codgeo
dictionnaire_codgeo = df_CODGEO_com.set_index('Numero Departement x Nom Ville')['COM'].to_dict()

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


#reste plus qu'a faire l'intervalle entre le CODGEO du dataframe avec les délits et celui avec les efffectifs
#ainsi garder seulement les communes pour lesquelles toutes les données sont dispo (nombres et types de délits et effectifs policiers)

#colonne avec les CODGEO dans le csv avec tous les délits : CODGEO_2024


#décommenter pour rendre les données filtrées

#print(data_delits.columns)
df_data_delits['CODGEO_2024'] = df_data_delits['CODGEO_2024'].astype(str)


# Comparer les colonnes DEP et COMPARENT, et ne garder que les lignes où les valeurs sont identiques
df_intersection_2016 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2016['CODGEO'])) &
    (df_data_delits['annee'] == 16)
]
print(df_intersection_2016)

df_intersection_2017 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2017['CODGEO'])) &
    (df_data_delits['annee'] == 17)
]
print(df_intersection_2017)

df_intersection_2018 = df_data_delits[
    (df_data_delits['CODGEO_2024'].isin(df_effectifs_2018['CODGEO'])) &
    (df_data_delits['annee'] == 18)
]
print(df_intersection_2018)
#df_intersection_2018.to_csv("C:\\Users\\Guillaume\\Downloads\\df_intersection_2018,1.csv", index=False)




