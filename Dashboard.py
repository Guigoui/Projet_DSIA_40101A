import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Charger les données pour les années 2016, 2017, 2018 et total
effectifs_2016 = pd.read_csv('data\\cleaned\\effectifs_2016.csv', delimiter=',')
effectifs_2017 = pd.read_csv('data\\cleaned\\effectifs_2017.csv', delimiter=',')
effectifs_2018 = pd.read_csv('data\\cleaned\\effectifs_2018.csv', delimiter=',')
effectifs_total = pd.read_csv('data\\cleaned\\effectifs_total.csv', delimiter=',')
effectifs_par_dept_annee = pd.read_csv('data\\cleaned\\effectifs_par_dept_annee.csv', delimiter=',')


delits_2016 = pd.read_csv('data\\cleaned\\delits_2016.csv', delimiter=',')
delits_2017 = pd.read_csv('data\\cleaned\\delits_2017.csv', delimiter=',')
delits_2018 = pd.read_csv('data\\cleaned\\delits_2018.csv', delimiter=',')
delits_total = pd.read_csv('data\\cleaned\\delits_total.csv', delimiter=',')
delits_par_dept_annee = pd.read_csv('data\\cleaned\\delits_par_dept_annee.csv', delimiter=',')


# cas spécial pour les département à 1 chiffre, les écrire sous forme 01 au lieu de 1 (fait tjrs ca à l'ouverture du csv surement problème de type problème à régler si assez de temps)
effectifs_par_dept_annee['Numero Departement'] = effectifs_par_dept_annee['Numero Departement'].apply(lambda x: str(x).zfill(2))
delits_par_dept_annee['departement'] = delits_par_dept_annee['departement'].apply(lambda x: str(x).zfill(2))
print('test')
print(effectifs_par_dept_annee["Numero Departement"].unique())




# Initialiser l'application Dash
app = Dash(__name__)

# Layout de l'application avec des onglets et sélection de l'année
app.layout = html.Div(children=[
    html.H1("Tableau de Bord des Effectifs de Police et des actes de délinquance recensés (2016-2018)", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.Tabs(id="tabs", value='tab-intro', children=[
        dcc.Tab(label='Introduction', value='tab-intro'),
        dcc.Tab(label='Carte de France', value='tab-map'),
        dcc.Tab(label='Évolution des Effectifs', value='tab-evolution'),  
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
