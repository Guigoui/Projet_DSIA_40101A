import pandas as pd
import re
import unicodedata


#stockage des chemins des csv dans des strings

effectifs_2016_chemin  = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\Effectifs_police_municipale_au_31_decembre_2016.csv"
effectifs_2017_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\effectifs-police-municipale-2017.csv"
effectifs_2018_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\effectifs-police-municipale-2018.csv"

data_delits_chemin = "C:\\Users\\Guillaume\\Downloads\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv"

CODGEO_communes_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\v_commune_2024.csv"




#création de dataframes pour chaque csv en précisant la délimitation des colonnes par les ','
effectifs_2016 = pd.DataFrame(pd.read_csv(effectifs_2016_chemin,delimiter=','))
effectifs_2017 = pd.DataFrame(pd.read_csv(effectifs_2017_chemin,delimiter=','))
effectifs_2018 = pd.DataFrame(pd.read_csv(effectifs_2018_chemin,delimiter=','))
#décommenter pour rendre les données filtrées
#data_delits = pd.DataFrame(pd.read_csv(data_delits_chemin,delimiter=';')) #temps d'exécution trop long
CODGEO_com = pd.DataFrame(pd.read_csv(CODGEO_communes_chemin,delimiter=','))




#effectifs_2016.columns[0] = colonne numéro département
#effectifs_2016.columns[1] correspond à la colonne qui contient le nom des villes (2eme colonne), on renomme par Nom Ville, inplace = True 
#permet de modifier directement le dataframe sans créer de nouvelle copie

#pour 2018 : num departement colonne 1 (pas entre parentheses) et nom ville colonne 4


effectifs_2016.rename(columns={effectifs_2016.columns[0]: 'Dep'}, inplace=True)
effectifs_2017.rename(columns={effectifs_2017.columns[0] : 'Dep'}, inplace=True)
effectifs_2018.rename(columns={effectifs_2018.columns[0]: 'Dep'}, inplace=True)

effectifs_2016.rename(columns={effectifs_2016.columns[1]: 'Nom Ville'}, inplace=True)
effectifs_2017.rename(columns={effectifs_2017.columns[1] : 'Nom Ville'}, inplace=True)
effectifs_2018.rename(columns={effectifs_2018.columns[3]: 'Nom Ville'}, inplace=True)



#ligne qui nous intéresse dans CODGEO_com = "NCC", il contient les noms des villes en majuscule et 'COM' qui contient les codgeo
#ligne qui nous intéresse dans effectifs_2016 = "Nom Ville", il contient les noms des villes en majuscule
#il faut maintenant ajouter une colonne dans effectifs_2016 qui donne le codgeo de la commune sur la ligne
#pour cela on peut creer un dictionnaire à l'aide CODGEO_com qui contient les noms de villes en tant que clé et le codgeo en valeur

#il faut que les noms des villes coincident donc tout mettre en majuscule et supprimer la partie entre () de la colonne Nom Ville
#ne pas oublier de supprimer caractères spéciaux comme * par exemple et toutes les "anomalies"

effectifs_2016['Nom Ville'] = effectifs_2016['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
effectifs_2017['Nom Ville'] = effectifs_2017['Nom Ville'].str.encode('utf-8').str.decode('utf-8')
effectifs_2018['Nom Ville'] = effectifs_2018['Nom Ville'].str.encode('utf-8').str.decode('utf-8')


def transformer_ville_effectifs(ville) : 
#for ville in effectifs_2016['Nom Ville'] : 
    if ville is not None : 
        #supprimer texte apres la premiere parenthese
        ville = re.sub(r'\(.*', '', str(ville)) 

        #met tout le texte en majuscule
        ville = str(ville).upper()        

        #remplace les - en espace " "
        ville = str(ville).replace("-", " ")  

        #remplace les - en espace " "
        ville = str(ville).replace("–", " ")       

        # Supprimer les apostrophes typographiques ’
        #ville = str(ville).replace("’", " ")  

         # Supprimer toutes les variations d'apostrophes
        ville = re.sub(r"[’‘']", " ", ville)
        
        #remplace les ST en SAINT
        ville = str(ville).replace("ST ", "SAINT ") 

        #remplace les ST en SAINT
        ville = str(ville).replace("/", " SUR ")

        #remplace les ST en SAINT
        ville = str(ville).replace(" *", "")

        #remplace les "L " en ""
        #ville = str(ville).replace("L ", "") 

        # Supprimer "L " en début de chaîne
        ville = re.sub(r'^L\s+', '', str(ville))
        
        # Supprimer LE ou LA ou LES en début de nom de ville
        ville = re.sub(r'^(LE|LA|LES)\s+', '', ville)
        
        # Supprimer les accents
        ville = ''.join(c for c in unicodedata.normalize('NFD', ville) if unicodedata.category(c) != 'Mn')

    

    #retire les espaces inutiles
    return ville.strip()                                    
        #print(ville)



effectifs_2016['Nom Ville'] = effectifs_2016['Nom Ville'].apply(transformer_ville_effectifs)
effectifs_2017['Nom Ville'] = effectifs_2017['Nom Ville'].apply(transformer_ville_effectifs)
effectifs_2018['Nom Ville'] = effectifs_2018['Nom Ville'].apply(transformer_ville_effectifs)




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

def extraire_nombres(texte):
    # Utilise une expression régulière pour détecter toutes les séquences de chiffres
    nombres = re.findall(r'\d+', texte)
    # Joindre les nombres en une seule chaîne, ou renvoyer None s'il n'y a pas de nombre
    return ''.join(nombres) if nombres else None



#il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
effectifs_2016['Dep'] = effectifs_2016['Dep'].astype(str)
effectifs_2017['Dep'] = effectifs_2017['Dep'].astype(str)
effectifs_2018['Dep'] = effectifs_2018['Dep'].astype(str)





# Parcourir chaque ligne de 1ère colonne (qui contient les noms de départements)
#for ligne in effectifs_2016['Dep']:



#création de variable globale departement_actuel pour le début de la fonction : 1er département ligne 17 donc avant ca il n'y a rien
departement_actuel = ""

def ecrire_departements(ligne) : 
    #accès à la variable globale
    global departement_actuel
    # Extraire le numéro de département, s'il y en a un
    nouveau_departement = extraire_nombres(ligne)
    if nouveau_departement:
        departement_actuel = nouveau_departement  # Mettre à jour la variable
        #print(f"Nouveau département détecté : {departement_actuel}")
    #else:
        #print(f"Ligne sans changement de département : {ligne}")
    return departement_actuel



#ok donc COMD signifie que la commune a fusionné avec une autre(même numéro codgeo) et numéro codgeo de la commune avec laquelle c'est fusionné est dans la colonne comparent
#il faut donc récupérer le 1er numéro dans comparent car il correspond au département et remplir la colonne dep avec ce numéro

#CODGEO_com['COMPARENT'] = CODGEO_com['COMPARENT'].astype(int)




#convertir les colonnes DEP et COMPARENT en string (attention comparent devient des nombres flottants et DEP devient 01 au lieu de 1)
CODGEO_com['DEP'] = CODGEO_com['DEP'].astype(str)
CODGEO_com['COMPARENT'] = CODGEO_com['COMPARENT'].astype(str)




#récupère 1er chiffre de comparent
def transform_dep (texte) : 
    #texte = str(texte)
    #vérifier si premier element est un chiffre
    if texte[0].isdigit():
        #si 4 nombre = 4 chiffres alors département de type unité 01,02,03 etc
        #print(texte)
        if len(texte) == 6 :
            return "0" + texte[0]
        #sinon département = dizaine
        else : 
            return texte[0:2]
    




#mettre le numéro du département dans la colonne DEP
for index, row in CODGEO_com.iterrows():

    if row['COMPARENT'] != "nan": 
        CODGEO_com.at[index, 'DEP'] = transform_dep(row['COMPARENT'])  # Mettre à jour le DataFrame directement        
        #print(row['DEP'])

#attention un peu long a exécuter




#Dans la colonne CODGEO['COM'], il y a des zéros inutiles en début de nombre lorsque les numéros sont des taille 4 (4 chiffres) ex : 01051 au lieu de 1051
#Donc on va changer ca 
#retourne une string sans le zero d'indice 0 s'il y en a un
def suppr_zero (texte) : 
    if texte[0] == "0" : 
        #retourne texte sans le zero d'indice 0
        return texte[1::]
    else :
        return texte

CODGEO_com['COM'] = CODGEO_com['COM'].apply(suppr_zero)

#code testé fonctionnel 



#exception pour 2018, les départements sont de la forme 1,2,3.. et non 01,02,03.. donc changer ca

def add_zero (texte) : 
    if len(texte) == 1 : 
        texte = "0" + texte
    return texte



effectifs_2016['Numero Departement'] = effectifs_2016['Dep'].apply(ecrire_departements)
effectifs_2017['Numero Departement'] = effectifs_2017['Dep'].apply(ecrire_departements)
effectifs_2018['Numero Departement'] = effectifs_2018['Dep'].apply(ecrire_departements)

effectifs_2018['Numero Departement'] = effectifs_2018['Numero Departement'].apply(add_zero)


#print(effectifs_2016['Numero Departement'][150:200])
#print(effectifs_2016['Nom Ville'][150:200])
effectifs_2016['Numero Departement x Nom Ville'] = effectifs_2016['Numero Departement'] + effectifs_2016['Nom Ville']
effectifs_2017['Numero Departement x Nom Ville'] = effectifs_2017['Numero Departement'] + effectifs_2017['Nom Ville']
effectifs_2018['Numero Departement x Nom Ville'] = effectifs_2018['Numero Departement'] + effectifs_2018['Nom Ville']
#print(effectifs_2018['Numero Departement x Nom Ville'][0:50])
#ca marche
#effectifs_2018.to_csv("C:\\Users\\Guillaume\\Downloads\\effectifs_2018,1.csv", index=False)



#maintenant faire de meme pour codgeo_com
CODGEO_com['Numero Departement x Nom Ville'] = CODGEO_com['DEP'] + CODGEO_com['NCC']
#print(CODGEO_com['Numero Departement x Nom Ville'][0:50])

#CODGEO_com.to_csv("C:\\Users\\Guillaume\\Downloads\\CODGEO_com.csv", index=False) #tres bien





#creer dictionnaire avec clés = l'identifiant des villes (nom+num_dep) et valeurs = numero codgeo
dictionnaire_codgeo = CODGEO_com.set_index('Numero Departement x Nom Ville')['COM'].to_dict()
#print(dictionnaire_codgeo)

#attribution des codgeo dans une nouvelle colonne CODGEO : utilisation de la méthode map qui associe les cles du dico le contenu de effectifs_2016['Numero Departement x Nom Ville'] (si les 2 matchent alors prendre codgeo assodcié à la clé correspondante)
effectifs_2016['CODGEO'] = effectifs_2016['Numero Departement x Nom Ville'].map(dictionnaire_codgeo)
effectifs_2017['CODGEO'] = effectifs_2017['Numero Departement x Nom Ville'].map(dictionnaire_codgeo)
effectifs_2018['CODGEO'] = effectifs_2018['Numero Departement x Nom Ville'].map(dictionnaire_codgeo)

#print(effectifs_2016['CODGEO'][0:50])
#print(CODGEO_com['COM'][50:100])

#recherche de doublons
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



#print(effectifs_2016['Nom Ville'][215:232])
#print(effectifs_2016[100:150])

#effectifs_2016.to_csv("C:\\Users\\Guillaume\\Downloads\\effectifs_2016_test_codgeo.csv", index=False)

#reste plus qu'a faire l'intervalle entre le CODGEO du dataframe avec les délits et celui avec les efffectifs
#ainsi garder seulement les communes pour lesquelles toutes les données sont dispo (nombres et types de délits et effectifs policiers)

#colonne avec les CODGEO dans le csv avec tous les délits : CODGEO_2024


#décommenter pour rendre les données filtrées
'''
#print(data_delits.columns)
data_delits['CODGEO_2024'] = data_delits['CODGEO_2024'].astype(str)


# Comparer les colonnes DEP et COMPARENT, et ne garder que les lignes où les valeurs sont identiques
df_intersection_2016 = data_delits[
    (data_delits['CODGEO_2024'].isin(effectifs_2016['CODGEO'])) &
    (data_delits['annee'] == 16)
]
print(df_intersection_2016)

df_intersection_2017 = data_delits[
    (data_delits['CODGEO_2024'].isin(effectifs_2017['CODGEO'])) &
    (data_delits['annee'] == 17)
]
print(df_intersection_2017)

df_intersection_2018 = data_delits[
    (data_delits['CODGEO_2024'].isin(effectifs_2018['CODGEO'])) &
    (data_delits['annee'] == 18)
]
print(df_intersection_2018)
#df_intersection_2018.to_csv("C:\\Users\\Guillaume\\Downloads\\df_intersection_2018,1.csv", index=False)
'''
