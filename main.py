import pandas as pd

#conversion des fichiers ods en csv

chemin  = "C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\Effectifs_police_municipale_au_31_decembre_2016.ods"

data = pd.read_excel(chemin, engine = 'odf')
data.to_csv("C:\\Users\\Guillaume\\Desktop\\Projet DSIA 40101A\\Effectifs_police_municipale_au_31_decembre_2016.csv", index = False)
