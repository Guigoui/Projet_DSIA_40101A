import pandas as pd
import os


#stockage des chemins des csv dans des strings

<<<<<<< HEAD

effectifs_2016_chemin = "Effectifs_police_municipale_au_31_decembre_2016.csv"
effectifs_2017_chemin = "effectifs-police-municipale-2017.csv"
effectifs_2018_chemin = "effectifs-police-municipale-2018.csv"
data_delits_chemin = "C:\\Users\\romai\\OneDrive\\Documents\\Esiee\E4\\donnee-reg-data.gouv-2023-geographie2024-produit-le2024-07-05.csv"
CODGEO_communes_chemin = "v_commune_2024.csv"


# effectifs_2016_chemin  = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\Effectifs_police_municipale_au_31_decembre_2016.csv"
# effectifs_2017_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\effectifs-police-municipale-2017.csv"
# effectifs_2018_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\effectifs-police-municipale-2018.csv"
# data_delits_chemin = "C:\\Users\\Guillaume\\Downloads\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv"
# CODGEO_communes_chemin = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\v_commune_2024.csv"
=======
effectifs_2016_chemin  = "data\\raw\\Effectifs_police_municipale_au_31_decembre_2016.csv"
effectifs_2017_chemin = "data\\raw\\effectifs-police-municipale-2017.csv"
effectifs_2018_chemin = "data\\raw\\effectifs-police-municipale-2018.csv"
data_delits_chemin = "C:\\Users\\Guillaume\\Downloads\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv\\donnee-data.gouv-2023-geographie2024-produit-le2024-07-05 (1).csv"
CODGEO_communes_chemin = "data\\raw\\v_commune_2024.csv"
>>>>>>> a9bf19a47c3d498617be6bc858f69da328ea089e




#création de dataframes pour chaque csv en précisant la délimitation des colonnes par les ','
df_effectifs_2016 = pd.DataFrame(pd.read_csv(effectifs_2016_chemin,delimiter=','))
df_effectifs_2017 = pd.DataFrame(pd.read_csv(effectifs_2017_chemin,delimiter=','))
df_effectifs_2018 = pd.DataFrame(pd.read_csv(effectifs_2018_chemin,delimiter=','))
#décommenter pour rendre les données filtrées
df_data_delits = pd.DataFrame(pd.read_csv(data_delits_chemin,delimiter=';')) #temps d'exécution très long
df_CODGEO_com = pd.DataFrame(pd.read_csv(CODGEO_communes_chemin,delimiter=','))

liste_df_effectifs = [df_effectifs_2016,df_effectifs_2017,df_effectifs_2018]
# print(df_data_delits.columns)
# print(df_data_delits)

# print(df_data_delits.dtypes)
# print(df_data_delits.memory_usage(deep=True))


# dataframes_list = []

# df_names = []  # Liste pour stocker les noms des DataFrames
# for col in df_data_delits.columns:
#     df_single_col = df_data_delits[[col]]  # Crée un DataFrame avec une seule colonne
#     dataframes_list.append(df_single_col)  # Stocker le DataFrame dans la liste
#     df_names.append(col)  # Ajouter le nom de la colonne à df_names

# df_classe = dataframes_list[df_data_delits.columns.get_loc('classe')]

# # print(df_classe.memory_usage(deep=True))


# # df_classe['classe'] = df_classe['classe'].astype('int32')

# # print(df_classe.memory_usage(deep=True))

# # df_classe.to_csv("C:\\Users\\Guillaume\\Downloads\\classev4.csv", index=False)


# mid_index = len(df_classe) // 2  # Trouver l'index du milieu

# # Créer les deux DataFrames
# df_classe_part1 = df_classe.iloc[:mid_index]  # Première moitié
# df_classe_part2 = df_classe.iloc[mid_index:]   # Deuxième moitié

# # Renommer les colonnes
# df_classe_part1 = df_classe_part1.rename(columns={'classe': 'classe_part1'})
# df_classe_part2 = df_classe_part2.rename(columns={'classe': 'classe_part2'})

# # Obtenir l'index de 'classe'
# index_classe = df_data_delits.columns.get_loc('classe')  

# # Supprimer l'ancien df_classe
# dataframes_list.pop(index_classe)

# dataframes_list.insert(index_classe, df_classe_part1)  # Remplacer par la première partie
# dataframes_list.insert(index_classe + 1, df_classe_part2)  # Ajouter la deuxième partie


# # Afficher la liste mise à jour pour vérifier
# # for i, df in enumerate(dataframes_list):
# #     print(f"DataFrame {i} :")
# #     print(df)

# #c'est bon ca marche

# #maintenant créer un csv pour chaque df

# output_directory = "data\\raw\\data_delits_decompose\\"

# for i, df in enumerate(dataframes_list):
#     # Récupérer le nom de la seule colonne dans chaque DataFrame
#     column_name = df.columns[0]  # Chaque DataFrame dans dataframes_list contient une seule colonne
#     filename = f"{column_name}.csv"  # Utiliser ce nom pour créer le fichier
#     df.to_csv(output_directory + filename, index=False)  # Enregistrer en CSV







# chemin du dossier contenant les fichiers CSV
csv_directory = "data\\raw\\data_delits_decompose\\"

# Liste pour stocker tous les df chargés
loaded_dataframes = []

# Parcourir tous les fichiers du dossier et charger les CSV
for index, filename in enumerate(os.listdir(csv_directory)):
    if filename.endswith(".csv"):  # Filtrer uniquement les fichiers CSV
        filepath = os.path.join(csv_directory, filename)
        # Créer un nom de variable basé sur le nom du fichier (sans extension)
        df_name = f"df_{os.path.splitext(filename)[0]}"  # Ex: df_nomducsv
        globals()[df_name] = pd.read_csv(filepath)  # Charger le DataFrame
        if df_name == "df_classe_part1" : 
            globals()[df_name] = globals()[df_name].rename(columns={'classe_part1':'classe'})
            index_classe_part1 = index  # Enregistrer l'index de df_classe_part1

        if df_name == "df_classe_part2" :
            globals()[df_name] = globals()[df_name].rename(columns={'classe_part2':'classe'})
            index_classe_part2 = index  # Enregistrer l'index de df_classe_part2
        loaded_dataframes.append(globals()[df_name])

# print(loaded_dataframes)

# print(loaded_dataframes[index_classe_part1])

#ignore_index = True permet de numéroter les lignes de 0 a 3917759 au lieu de 0 à la moitié
df_classe = pd.concat([loaded_dataframes[index_classe_part1],loaded_dataframes[index_classe_part2]],ignore_index=True)

# print(df_classe)

del loaded_dataframes[index_classe_part1]
# étant donné que le df_classe_part1 vient d'être supprimé, le df_classe_part2 vient de prendre sa place à l'index index_classe_part1
del loaded_dataframes[index_classe_part1]
loaded_dataframes.insert(index_classe_part1,df_classe)

# print(loaded_dataframes)


columns_name = []
for df in loaded_dataframes : 
    columns_name.append(df.columns[0])

# print(columns_name)


df_data_delits = pd.concat(loaded_dataframes, axis = 1, ignore_index=True)

df_data_delits.columns = columns_name
# print(df_data_delits)

# ok ca marche les 2 correspondent il y a juste les colonnes qui ne sont pas aux memes endroits LETS GOOOO ENFIIIN APRES 4HEURES



