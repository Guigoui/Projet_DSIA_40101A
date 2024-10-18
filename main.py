import pandas as pd

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

print(effectifs_2016['CODGEO'][50:100])
#print(effectifs_2016)