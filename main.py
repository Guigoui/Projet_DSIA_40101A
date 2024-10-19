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

        #remplace les ST en SAINT
        ville = str(ville).replace("ST", "SAINT")          

        #remplace les - en espace " "
        ville = str(ville).replace("-", " ")  

        #remplace les - en espace " "
        ville = str(ville).replace("–", " ")       

    
        # Supprimer les apostrophes typographiques
        ville = str(ville).replace("’", " ")  

        # Supprimer LE ou LA en début de nom de ville
        ville = re.sub(r'^(LE|LA)\s+', '', ville)

        # Supprimer les accents
        ville = ''.join(c for c in unicodedata.normalize('NFD', ville) if unicodedata.category(c) != 'Mn')

        

    #retire les espaces inutiles
    return ville.strip()                                    
        #print(ville)

effectifs_2016['Nom Ville'] = effectifs_2016['Nom Ville'].apply(transformer_ville_effectifs)

print(effectifs_2016['Nom Ville'][139:142])

#supprimer les ' et remplacer par un espace attention conserver de DE car souvent utilisé dans codgeo et voir ligne 93 le - pas supprimé
#prochaine étape récupérer le v_commune pour 2016 et comparer, si c'est toujours la même chose alors s'arreter la 
#concernant les différences liées à l'orthographe, je peux pas faire grand chose


#création d'un dictionnaire qui stocke la colonne NCC en tant que clé et la colonne COM en tant que valeur

'''
CODGEO_NCC_COM = pd.DataFrame(CODGEO_com["NCC"],["COM"])
doublons = CODGEO_NCC_COM.duplicated()
print(doublons) #retourne false donc pas de doublons
'''

dictionnaire_codgeo = CODGEO_com.set_index('NCC')['COM'].to_dict()
#print(dictionnaire_codgeo)

#attribution des codgeo dans une nouvelle colonne CODGEO : utilisation de la méthode map qui associe les cles du dico aux valeurs de Source\xa0: Ministère de l’intérieur (DLPAJ)
effectifs_2016['CODGEO'] = effectifs_2016['Nom Ville'].map(dictionnaire_codgeo)

print(effectifs_2016['Nom Ville'][85:120])
#print(effectifs_2016[100:150])

#effectifs_2016.to_csv("C:\\Users\\Guillaume\\Downloads\\effectifs_2016_test_codgeo4.csv", index=False)