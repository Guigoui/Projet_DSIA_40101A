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
#data_delits = pd.DataFrame(pd.read_csv(data_delits_chemin,delimiter=','))
CODGEO_com = pd.DataFrame(pd.read_csv(CODGEO_communes_chemin,delimiter=','))


colonnes_effectifs_2016 = [ name for name in effectifs_2016.columns ] #contient le nom des colonnes de effectifs_2016
#colonne qui contient les noms des villes : Source\xa0: Ministère de l’intérieur (DLPAJ), on renomme par Nom Ville, inplace = True 
#permet de modifier directement le dataframe sans créer de nouvelle copie
effectifs_2016.rename(columns={'Source\xa0: Ministère de l’intérieur (DLPAJ)': 'Nom Ville'}, inplace=True)


#print(effectifs_2016['Source\xa0: Ministère de l’intérieur (DLPAJ)'])

#ligne qui nous intéresse dans CODGEO_com = "NCC", il contient les noms des villes en majuscule et 'COM' qui contient les codgeo
#ligne qui nous intéresse dans effectifs_2016 = "Nom Ville", il contient les noms des villes en majuscule
#il faut maintenant ajouter une colonne dans effectifs_2016 qui donne le codgeo de la commune sur la ligne
#pour cela on peut creer un dictionnaire à l'aide CODGEO_com qui contient les noms de villes en tant que clé et le codgeo en valeur

#il faut que les noms des villes coincident donc tout mettre en majuscule et supprimer la partie entre () de la colonne Nom Ville
#ne pas oublier de supprimer caractères spéciaux comme * par exemple

effectifs_2016['Nom Ville'] = effectifs_2016['Nom Ville'].str.encode('utf-8').str.decode('utf-8')


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
        if match.group(1)[0] == "0" : #supprime le 0 dans 01 et renvoie seulement 1 pour correspondre avec les départements dans codgeo
            return match.group(1)[1]
        else : 
            return match.group(1)
    return None

#il faut que la colonne avec les numéros de départements soit une string sinon pourra pas gérer les NULL
effectifs_2016['Unnamed: 0'] = effectifs_2016['Unnamed: 0'].astype(str)

# Parcourir chaque ligne de 1ère colonne (qui contient les noms de départements)
#for ligne in effectifs_2016['Unnamed: 0']:

#création de variable globale departement_actuel pour le début de la fonction : 1er département ligne 17 donc avant ca il n'y a rien
departement_actuel = ""

def ecrire_departements(ligne) : 
    #accès à la variable globale
    global departement_actuel
    # Extraire le numéro de département, s'il y en a un
    nouveau_departement = extraire_numero_departement(ligne)
    if nouveau_departement:
        departement_actuel = nouveau_departement  # Mettre à jour la variable
        #print(f"Nouveau département détecté : {departement_actuel}")
    #else:
        #print(f"Ligne sans changement de département : {ligne}")
    return departement_actuel



#code testé fonctionnel 

effectifs_2016['Numero Departement'] = effectifs_2016['Unnamed: 0'].apply(ecrire_departements)
#print(effectifs_2016['Numero Departement'][150:200])
#print(effectifs_2016['Nom Ville'][150:200])
effectifs_2016['Numero Departement x Nom Ville'] = effectifs_2016['Numero Departement'] + effectifs_2016['Nom Ville']
#print(effectifs_2016[50:100])
#ca marche

#maintenant faire de meme pour codgeo_com

CODGEO_com['Numero Departement x Nom Ville'] = CODGEO_com['DEP'] + CODGEO_com['NCC']
print(CODGEO_com['Numero Departement x Nom Ville'][10000:10050])



dictionnaire_codgeo = CODGEO_com.set_index('NCC')['COM'].to_dict()
#print(dictionnaire_codgeo)

#attribution des codgeo dans une nouvelle colonne CODGEO : utilisation de la méthode map qui associe les cles du dico aux valeurs de Nom Ville
effectifs_2016['CODGEO'] = effectifs_2016['Nom Ville'].map(dictionnaire_codgeo)

#recherche de doublons
'''
doublons = effectifs_2016[effectifs_2016['Nom Ville'].duplicated(keep=False)]

for ville in doublons['Nom Ville'] : 
    if ville != "NAN" :
        print(ville)


doublons_codgeo = CODGEO_com[CODGEO_com['NCC'].duplicated(keep=False)]

for ville in doublons_codgeo['NCC'] : 
    if ville != "NAN" :
        print(ville)
'''



#print(effectifs_2016['Nom Ville'][215:232])
#print(effectifs_2016[100:150])

#effectifs_2016.to_csv("C:\\Users\\Guillaume\\Downloads\\effectifs_2016_test_codgeo8.csv", index=False)