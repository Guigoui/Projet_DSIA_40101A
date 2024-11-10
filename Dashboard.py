import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Charger les données 
effectifs_total = pd.read_csv('data\\cleaned\\effectifs_total.csv', delimiter=',')
effectifs_par_dept_annee = pd.read_csv('data\\cleaned\\effectifs_par_dept_annee.csv', delimiter=',')
delits_total = pd.read_csv('data\\cleaned\\delits_total.csv', delimiter=',')
delits_par_dept_annee = pd.read_csv('data\\cleaned\\delits_par_dept_annee.csv', delimiter=',')
delits_par_commune_annee = pd.read_csv('data\\cleaned\\delits_par_commune_annee.csv', delimiter=',')
delits_par_commune_annee_sorted = pd.read_csv('data\\cleaned\\delits_par_commune_annee_sorted.csv', delimiter=',')

# cas spécial pour les département à 1 chiffre, les écrire sous forme 01 au lieu de 1 (fait tjrs ca à l'ouverture du csv surement problème de type problème à régler si assez de temps)
# sinon tous les département ne sont pas affichés (données dep ne correspondant pas avec celles de la carte de france)
effectifs_par_dept_annee['Numero Departement'] = effectifs_par_dept_annee['Numero Departement'].apply(lambda x: str(x).zfill(2))
delits_par_dept_annee['departement'] = delits_par_dept_annee['departement'].apply(lambda x: str(x).zfill(2))



# Initialiser l'application Dash
app = Dash(__name__)

# Layout de l'application Dash avec des onglets pour séparer les différentes visualisations
app.layout = html.Div(children=[
    # Titre principal du tableau de bord
    html.H1("Tableau de Bord des Effectifs de Police et des actes de délinquance recensés (2016-2018)", style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Création des onglets pour passer d'une section à l'autre
    dcc.Tabs(id="tabs", value='tab-intro', children=[
        dcc.Tab(label='Introduction', value='tab-intro'), # onglet Introduction
        dcc.Tab(label='Carte de France', value='tab-map'), # onglet Carte de France
        dcc.Tab(label='Évolution des Effectifs', value='tab-evolution'),  # onglet Évolution des Effectifs
        dcc.Tab(label='Délits par Intervalle de Population', value='tab-delits-intervalle') # onglet Délits par Population
    ]),

    # Contenu qui changera en fonction de l'onglet sélectionné
    html.Div(id='tabs-content')
])

# Callback pour afficher le contenu en fonction de l'onglet sélectionné
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    # onglet "Introduction"
    if tab == 'tab-intro':
        return html.Div([
            html.H2("Bienvenue sur le tableau de bord"),
            html.P("Ce tableau de bord présente les effectifs de police par département en France de 2016 à 2018.")
        ])
    
    # onglet "Carte de France"
    elif tab == 'tab-map':
        # Carte de France des effectifs de police
        fig_effectifs = px.choropleth(
            # données des effectifs de police par département
            effectifs_par_dept_annee, 
            # URL du fichier GeoJSON de la carte de France
            geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
            # colonne contenant les codes des départements
            locations="Numero Departement",
            # clé geojson
            featureidkey="properties.code",
            # données de la colonne somme_ligne définissant la couleur en fonction des effectifs
            color="somme_ligne",
            # colonne à afficher au survol du curseur de la souris
            hover_name="Numero Departement",
            # animation carte selon les années
            animation_frame="Année",
            # titre carte
            title="Effectifs de Police par Département (2016-2018)",
            # échelle de couleur (ici verte pour les effectifs)
            color_continuous_scale="Greens",
            # intervalle de couleurs
            range_color=[0, 1500],
            # changer le nom de l'échelle par Effectifs de police
            labels={"somme_ligne": "Effectifs de police"}  


        )
        # ajuste la carte pour afficher seulement la France métropolitaine 
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
            labels={"somme_ligne": "délits"}  

        )
        fig_delits.update_geos(fitbounds="locations", visible=False)
        
        # affichage côte à côte des deux cartes
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
                 # id pour le menu déroulant (dropdwon) de sélection des départements
                id='departement-dropdown', 
                options=[
                    {'label': f'Département {i}', 'value': str(i).zfill(2)} for i in range(1, 96)
                ],
                # département sélectionné par défaut 
                value='93', 
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(id='evolution-graph')
        ])


    elif tab == 'tab-delits-intervalle':  # Onglet pour l'histogramme des délits par population
        return html.Div([
            html.H2("Histogramme des Délits en Fonction de la Population des Communes"),
            dcc.Dropdown(
                id='annee-delits-dropdown',
                options=[
                    {'label': '2016', 'value': 16},
                    {'label': '2017', 'value': 17},
                    {'label': '2018', 'value': 18}
                ],
                value=16,  # Valeur par défaut
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(id='delits-intervalle-graph')
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


# Callback pour afficher l'histogramme des délits en fonction de la population des communes
@app.callback(
    Output('delits-intervalle-graph', 'figure'),
    Input('annee-delits-dropdown', 'value')
)
def update_delits_graph(annee):
    delits_filtered = delits_par_commune_annee_sorted[delits_par_commune_annee_sorted['annee'] == annee]
    delits_filtered_sorted = delits_filtered.sort_values(by='POP', ascending=True)
    fig = px.histogram(
        delits_filtered_sorted,
        x='POP',
        y='somme_ligne',
        histfunc='sum',
        labels={'POP': 'Population des Communes', 'somme_ligne': 'Nombre de Délits'},
        title=f"Histogramme des Délits en Fonction de la Population des Communes (Année {annee})",
        # nombre de barres dans l'histogramme
        nbins=1000
    )
    return fig

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)


