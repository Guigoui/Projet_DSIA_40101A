import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Charger les données 
effectifs_total = pd.read_csv('data\\cleaned\\effectifs_total.csv', delimiter=',')
effectifs_par_dept_annee = pd.read_csv('data\\cleaned\\effectifs_par_dept_annee.csv', delimiter=',')
effectifs_par_commune_annee_sorted = pd.read_csv('data\\cleaned\\effectifs_par_commune_annee_sorted.csv', delimiter=',')
delits_total = pd.read_csv('data\\cleaned\\delits_total.csv', delimiter=',')
delits_par_dept_annee = pd.read_csv('data\\cleaned\\delits_par_dept_annee.csv', delimiter=',')
delits_par_commune_annee = pd.read_csv('data\\cleaned\\delits_par_commune_annee.csv', delimiter=',')
delits_par_commune_annee_sorted = pd.read_csv('data\\cleaned\\delits_par_commune_annee_sorted.csv', delimiter=',')
merged_data = pd.read_csv('data\\cleaned\\merged_data.csv', delimiter=',')


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
        dcc.Tab(label='Délits par Intervalle de Population', value='tab-delits-intervalle'), # onglet Délits par Population
        dcc.Tab(label='Effectifs vs Délits', value='tab-effectifs-vs-delits')  # onglet pour le nuage de points 

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
             html.P("Explorez ce dashboard réalisé par Romain Yerolymos et Guillaume Curtis. Ce tableau de bord interactif vous permet de visualiser les données et de comprendre les tendances régionales au fil des années."),
             html.Br(),
             html.P("La première page affiche les données sur des cartes."),
             html.Br(),
             html.P("La deuxième page affiche l'evolution des effectifs de police en fonction du département."),
             html.Br(),
             html.P("La troisième page affiche les données des délits et des effectifs de police en fonction des intervalles population. Chaque commune est assignée à un intervalle de population et la somme des délits ou effectifs de ces communes permettent de mettre en évidence la distribution de délits et d'effectifs en fonction de l'intervalle de population."),
             html.Br(),
             html.P("La quatrième page affiche les délits en fonction du nombre de policier.")
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
                {'label': '2017', 'value': 2017},
                {'label': '2018', 'value': 2018}
            ],
                value=2016,  # Valeur par défaut
                style={'width': '50%', 'margin': 'auto'}
             ),
             # 2 histogramme pour les délits et effectifs
            dcc.Graph(id='delits-intervalle-graph'),
            dcc.Graph(id='effectifs-intervalle-graph') 
        ])
    elif tab == 'tab-effectifs-vs-delits':
        # Onglet pour afficher le graphique Effectifs vs Délits
        return html.Div([
            html.H2("Relation entre les Effectifs de Police et les Délits par Département"),
            dcc.Dropdown(
                id='annee-effectifs-vs-delits-dropdown',
                options=[
                    {'label': '2017', 'value': 2017},
                    {'label': '2018', 'value': 2018}
                ],
                value=2017,  # Valeur par défaut
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(id='effectifs-vs-delits-graph')
        ])
    
    

# Callback pour mettre à jour le graphique en fonction du département sélectionné
@app.callback(
    Output('evolution-graph', 'figure'),
    Input('departement-dropdown', 'value')
)
def update_graph(departement):
    # filtrer les données pour le département sélectionné
    dept_data = effectifs_par_dept_annee[effectifs_par_dept_annee["Numero Departement"] == departement]
    
    # créer le graphique
    fig = px.bar(
    dept_data,
    x="Année",
    y="somme_ligne",
    title=f"Évolution des Effectifs de Police dans le {departement}",
     # pour colorier les barres en fonction de l'année
    labels={"somme_ligne": "Nombre d'effectifs de police", "Année": "Année"},
    barmode="group"  # affiche les barres côte à côte pour chaque année si besoin
)
    fig.update_layout(xaxis_title="Année", yaxis_title="Nombre d'effectifs de police")
    return fig


# Callback pour afficher l'histogramme des délits en fonction de la population des communes
@app.callback(
    [Output('delits-intervalle-graph', 'figure'),
    Output('effectifs-intervalle-graph', 'figure')],
    Input('annee-delits-dropdown', 'value')
)
def update_delits_graph(annee):
    delits_filtered = delits_par_commune_annee_sorted[delits_par_commune_annee_sorted['annee'] == annee]
    delits_filtered_sorted = delits_filtered.sort_values(by='POP', ascending=True)

    # créer l'histogramme pour les délits
    fig_delits = px.histogram(
        delits_filtered_sorted,
        x='POP',
        y='somme_ligne',
        histfunc='sum',
        labels={'POP': 'Population des Communes', 'somme_ligne': 'Nombre de Délits'},
        title=f"Histogramme des Délits en Fonction de la Population des Communes (Année {annee})",
        # nombre de barres dans l'histogramme
        nbins=1000
    )

    # Filtrer les données des effectifs pour l'année sélectionnée
    effectifs_filtered = effectifs_par_commune_annee_sorted[effectifs_par_commune_annee_sorted['Année'] == annee]
    effectifs_filtered_sorted = effectifs_filtered.sort_values(by='Nombre d habitants', ascending=True)


    # créer l'histogramme pour les effectifs
    fig_effectifs = px.histogram(
        effectifs_filtered_sorted,
        x='Nombre d habitants',
        y='somme_ligne',
        histfunc='sum',
        labels={'Nombre d habitant': 'Population des Communes', 'somme_ligne': 'Nombre d\'Effectifs'},
        title=f"Histogramme des Effectifs en Fonction de la Population des Communes (Année {annee})",
        nbins=1000
    )

    return fig_delits, fig_effectifs


# Callback pour afficher le graphique Effectifs vs Délits
@app.callback(
    Output('effectifs-vs-delits-graph', 'figure'),
    Input('annee-effectifs-vs-delits-dropdown', 'value')
)
def update_effectifs_vs_delits_graph(annee):
    # filtrer les données pour l'année sélectionnée et le nomnbre d'habitants
    filtered_data = merged_data[merged_data['Année'] == annee]
    # il faut normaliser la taille donc x100 et faire le rapport avec la taille max (pour l'échelle)
    filtered_data['taille_cercle'] = filtered_data['Nombre d habitants'] / filtered_data['Nombre d habitants'].max() * 100  


    # Créer le nuage de points
    fig = px.scatter(
        filtered_data,
        x='somme_ligne_effectifs',  # effectifs de police
        y='somme_ligne_delits',     # nombre de délits
        size='taille_cercle',       # taille des cercles en fonction de la population
        color='CODGEO',  #  ville
        hover_name='CODGEO',  # Afficher le code géographique au survol du curseur de la souris
        labels={'somme_ligne_effectifs': 'Effectifs de Police', 'somme_ligne_delits': 'Délits'},
        title=f"Relation entre les Effectifs de Police et les Délits (Année {annee})",
        size_max=50,  # taille max des cercles

    )
    return fig

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)


