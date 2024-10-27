import pandas as pd
import re
import unicodedata




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


#pour extraire les numéros de départements dans la 1ere colonne
def extraire_nombres(texte):
    # Utilise une expression régulière pour détecter toutes les séquences de chiffres
    nombres = re.findall(r'\d+', texte)
    # Joindre les nombres en une seule chaîne, ou renvoyer None s'il n'y a pas de nombre
    return ''.join(nombres) if nombres else None



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
        


#Dans la colonne CODGEO['COM'], il y a des zéros inutiles en début de nombre lorsque les numéros sont des taille 4 (4 chiffres) ex : 01051 au lieu de 1051
#Donc on va changer ca 
#retourne une string sans le zero d'indice 0 s'il y en a un
def suppr_zero (texte) : 
    if texte[0] == "0" : 
        #retourne texte sans le zero d'indice 0
        return texte[1::]
    else :
        return texte
    

#exception pour 2018, les départements sont de la forme 1,2,3.. et non 01,02,03.. donc changer ca

def add_zero (texte) : 
    if len(texte) == 1 : 
        texte = "0" + texte
    return texte