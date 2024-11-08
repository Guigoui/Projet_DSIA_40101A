import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Charger les données pour les années 2016, 2017, 2018 et total
effectifs_2016 = pd.read_csv('data\\cleaned\\effectifs_2016.csv', delimiter=',')
effectifs_2017 = pd.read_csv('data\\cleaned\\effectifs_2017.csv', delimiter=',')
effectifs_2018 = pd.read_csv('data\\cleaned\\effectifs_2018.csv', delimiter=',')
effectifs_total = pd.read_csv('data\\cleaned\\effectifs_total.csv', delimiter=',')

delits_2016 = pd.read_csv('data\\cleaned\\delits_2016.csv', delimiter=',')
delits_2017 = pd.read_csv('data\\cleaned\\delits_2017.csv', delimiter=',')
delits_2018 = pd.read_csv('data\\cleaned\\delits_2018.csv', delimiter=',')
delits_total = pd.read_csv('data\\cleaned\\delits_total.csv', delimiter=',')

#on ne prends pas en compte la ligne 1350

# converti ces colonnes en ignorant les erreurs (de object à float)
effectifs_total["Nombre d ASVP"] = pd.to_numeric(effectifs_total["Nombre d ASVP"], errors="coerce")
effectifs_total["Nombre d habitants"] = pd.to_numeric(effectifs_total["Nombre d habitants"], errors="coerce")




# Remplir les valeurs manquantes avec 0
effectifs_2016 = effectifs_2016.fillna(0)
effectifs_2017 = effectifs_2017.fillna(0)
effectifs_2018 = effectifs_2018.fillna(0)
effectifs_total = effectifs_total.fillna(0)

effectifs_total_cols = effectifs_total[['Nombre de policiers municipaux', 'Nombre d ASVP',
       'Nombre de gardes-champêtres', 'Nombre d agents cynophiles',
       'Nombre de chiens de patrouille de police municipale','Nombre de maîtres chiens de police municipale']]

# converti tous les types des colonnes en int64
effectifs_total_cols = effectifs_total_cols.astype({col: 'int64' for col in effectifs_total_cols.select_dtypes(include='float64').columns})


# print(effectifs_total_cols.dtypes)
# Préparer les données par département et par année
effectifs_par_dept_annee = effectifs_total.groupby(["Numero Departement", "Année"]).agg({
    col: "sum" for col in effectifs_total_cols.columns
}).reset_index()

# print(effectifs_par_dept_annee.columns)
#faire la somme sur la ligne : 
effectifs_par_dept_annee['somme_ligne'] = effectifs_par_dept_annee.drop(['Numero Departement', 'Année'], axis=1).sum(axis=1)


# print(effectifs_par_dept_annee)
# effectifs_par_dept_annee.to_csv("data\\cleaned\\effectifs_par_dept_annee.csv", index=False)


# Convertir les numéros de département en chaînes pour correspondre au format de Plotly
effectifs_par_dept_annee["Numero Departement"] = effectifs_par_dept_annee["Numero Departement"].astype(str).str.zfill(2)
# print(effectifs_par_dept_annee)


# Vérifier les doublons dans les colonnes 'CODGEO_2024' et 'classe'
# print(f"Nombre de doublons dans les colonnes 'CODGEO_2024' et 'classe' : {delits_total[['CODGEO_2024', 'classe']].duplicated().sum()}")
# print(delits_2016)


# Réorganiser le tableau avec CODGEO_2024, POP et année comme index et les délits en colonnes
delits_pivot_2016 = delits_2016.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')
delits_pivot_2017 = delits_2017.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')
delits_pivot_2018 = delits_2018.pivot_table(index=['departement','CODGEO_2024','POP','annee'], columns='classe', values='faits', aggfunc='first')


#créer des colonnes avec les index
delits_pivot_2016 = delits_pivot_2016.reset_index()
delits_pivot_2017 = delits_pivot_2017.reset_index()
delits_pivot_2018 = delits_pivot_2018.reset_index()

# Remplir les valeurs manquantes avec 0
delits_pivot_2016 = delits_pivot_2016.fillna(0)
delits_pivot_2017 = delits_pivot_2017.fillna(0)
delits_pivot_2018 = delits_pivot_2018.fillna(0)




# print(delits_pivot_2016)
# print(delits_pivot_2017)
# print(delits_pivot_2018)
#conversion des types (pas forcément nécessaire)
delits_pivot_2016 = delits_pivot_2016.astype({col: 'int64' for col in delits_pivot_2016.select_dtypes(include='float64').columns})
delits_pivot_2017 = delits_pivot_2017.astype({col: 'int64' for col in delits_pivot_2017.select_dtypes(include='float64').columns})
delits_pivot_2018 = delits_pivot_2018.astype({col: 'int64' for col in delits_pivot_2018.select_dtypes(include='float64').columns})


delits_pivot_total = pd.concat([delits_pivot_2016,delits_pivot_2017,delits_pivot_2018],ignore_index=True)
# print(delits_pivot_total.columns)

delits_pivot_total_cols = delits_pivot_total[['Autres coups et blessures volontaires','Cambriolages de logement',
       'Coups et blessures volontaires',
       'Coups et blessures volontaires intrafamiliaux',
       'Destructions et dégradations volontaires', 'Trafic de stupéfiants',
       'Usage de stupéfiants', 'Violences sexuelles', 'Vols avec armes',
       'Vols d\'accessoires sur véhicules', 'Vols dans les véhicules',
       'Vols de véhicules', 'Vols sans violence contre des personnes',
       'Vols violents sans arme']]

# print(delits_pivot_total_cols.columns)
delits_par_dept_annee = delits_pivot_total.groupby(["departement", "annee"]).agg({
    col: "sum" for col in delits_pivot_total_cols.columns
}).reset_index()

# faire la somme sur la ligne pour déterminer l'ensemble des délits
delits_par_dept_annee['somme_ligne'] = delits_par_dept_annee.drop(['departement', 'annee'], axis=1).sum(axis=1)
print(delits_par_dept_annee)
# delits_par_dept_annee.to_csv("data\\cleaned\\delits_par_dept_annee.csv", index=False)



# Convertir les numéros de département en chaînes pour correspondre au format de Plotly
delits_par_dept_annee["departement"] = delits_par_dept_annee["departement"].astype(str).str.zfill(2)

# print(delits_pivot_2016.dtypes)
# print(delits_pivot_2017.dtypes)
# print(delits_pivot_2018.dtypes)
# print(delits_pivot_total)
# print(delits_par_dept_annee)












# Initialiser l'application Dash
app = Dash(__name__)

# Layout de l'application avec des onglets et sélection de l'année
app.layout = html.Div(children=[
    html.H1("Tableau de Bord des Effectifs de Police et des actes de délinquance recensés (2016-2018)", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.Tabs(id="tabs", value='tab-intro', children=[
        dcc.Tab(label='Introduction', value='tab-intro'),
        dcc.Tab(label='Carte de France', value='tab-map'),
        dcc.Tab(label='Évolution des Effectifs', value='tab-evolution'),  # Nouveau tab
    ]),
    html.Div(id='tabs-content')
])

# Callback pour le contenu des onglets
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-intro':
        return html.Div([
            html.H2("Bienvenue sur le tableau de bord"),
            html.P("Ce tableau de bord présente les effectifs de police par département en France de 2016 à 2018.")
        ])
    elif tab == 'tab-map':
        # Carte de France des effectifs de police
        fig_effectifs = px.choropleth(
            effectifs_par_dept_annee,
            # chargement carte
            geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
            locations="Numero Departement",
            featureidkey="properties.code",
            # prendre des données de la colonne somme_ligne
            color="somme_ligne",
            hover_name="Numero Departement",
            animation_frame="Année",
            title="Effectifs de Police par Département (2016-2018)",
            color_continuous_scale="Greens",
            range_color=[0, 1500],
            # changer le nom de l'échelle par Effectifs de police
            labels={"somme_ligne": "Effectifs de police"}  # Changer le nom de l'échelle ici


        )
        fig_effectifs.update_geos(fitbounds="locations", visible=False)
        
        # Carte de France des délits
        fig_delits = px.choropleth(
            delits_par_dept_annee,
            geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
            locations="departement",
            featureidkey="properties.code",
            color="somme_ligne",
            hover_name="departement",
            animation_frame="annee",
            title="Délits par Département (2016-2018)",
            color_continuous_scale="Reds",
            range_color=[0, 150000],
            labels={"somme_ligne": "délits"}  # Changer le nom de l'échelle ici

        )
        fig_delits.update_geos(fitbounds="locations", visible=False)
        
        return html.Div(style={'display': 'flex', 'justifyContent': 'space-around'}, children=[
            html.Div([
                html.H3("Effectifs de Police par Département"),
                dcc.Graph(figure=fig_effectifs)
            ], style={'width': '45%'}),
            html.Div([
                html.H3("Délits par Département"),
                dcc.Graph(figure=fig_delits)
            ], style={'width': '45%'})
        ])
    
    elif tab == 'tab-evolution':
        # Graphique pour l'évolution des effectifs dans un département
        return html.Div([
            html.H2("Évolution des Effectifs de Police dans un Département"),
            dcc.Dropdown(
                id='departement-dropdown',
                options=[
                    {'label': f'Département {i}', 'value': str(i).zfill(2)} for i in range(1, 96)
                ],
                value='93',  # Valeur par défaut (Paris)
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(id='evolution-graph')
        ])

# Callback pour mettre à jour le graphique en fonction du département sélectionné
@app.callback(
    Output('evolution-graph', 'figure'),
    Input('departement-dropdown', 'value')
)
def update_graph(departement):
    # Filtrer les données pour le département sélectionné
    dept_data = effectifs_par_dept_annee[effectifs_par_dept_annee["Numero Departement"] == departement]
    
    # Créer le graphique
    fig = px.bar(
    dept_data,
    x="Année",
    y="somme_ligne",
    title=f"Évolution des Effectifs de Police dans le {departement}",
     # Pour colorier les barres en fonction de l'année
    labels={"somme_ligne": "Nombre d'effectifs de police", "Année": "Année"},
    barmode="group"  # Affiche les barres côte à côte pour chaque année si besoin
)
    fig.update_layout(xaxis_title="Année", yaxis_title="Nombre d'effectifs de police")
    return fig

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
