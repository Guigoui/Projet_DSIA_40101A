import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Charger les données pour les années 2016, 2017, et 2018
effectifs_2016 = pd.read_csv('C:\\Users\\romai\OneDrive\\Documents\\Esiee\\E4\\Projet_DSIA_40101A\\data\\cleaned\\effectifs_2016.csv', encoding='ISO-8859-1', delimiter=';')
effectifs_2017 = pd.read_csv('C:\\Users\\romai\OneDrive\\Documents\\Esiee\\E4\\Projet_DSIA_40101A\\data\\cleaned\\effectifs_2017.csv', encoding='ISO-8859-1', delimiter=';')
effectifs_2018 = pd.read_csv('C:\\Users\\romai\OneDrive\\Documents\\Esiee\\E4\\Projet_DSIA_40101A\\data\\cleaned\\effectifs_2018.csv', encoding='ISO-8859-1', delimiter=';')

#on ne prends pas en compte la ligne 1350
#effectifs_2018 = pd.read_csv('C:\\Users\\romai\\OneDrive\\Documents\\Esiee\\E4\\Projet_DSIA_40101A\\data\\cleaned\\effectifs_2018.csv', encoding='ISO-8859-1', delimiter=';', skiprows=[1350])

# # Ajouter une colonne 'Année' à chaque DataFrame
effectifs_2016['Année'] = 2016
effectifs_2017['Année'] = 2017
effectifs_2018['Année'] = 2018

effectifs = pd.concat([effectifs_2016, effectifs_2017, effectifs_2018])

# Préparer les données par département et par année
effectifs_par_dept_annee = effectifs.groupby(["Numero Departement", "Année"]).agg({
    "Nombre de policiers municipaux": "sum"
}).reset_index()

# Convertir les numéros de département en chaînes pour correspondre au format de Plotly
effectifs_par_dept_annee["Numero Departement"] = effectifs_par_dept_annee["Numero Departement"].astype(str).str.zfill(2)

# Initialiser l'application Dash
app = Dash(__name__)

# Layout de l'application avec des onglets et sélection de l'année
app.layout = html.Div(children=[
    html.H1("Tableau de Bord des Effectifs de Police par Année", style={'textAlign': 'center', 'marginBottom': '20px'}),
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
            html.P("Ce tableau de bord présente les effectifs de police municipaux par département en France de 2016 à 2018.")
        ])
    elif tab == 'tab-map':
        # Carte de France des effectifs de police, avec une sélection d'année
        fig = px.choropleth(
            effectifs_par_dept_annee,
            geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
            locations="Numero Departement",
            featureidkey="properties.code",
            color="Nombre de policiers municipaux",
            hover_name="Numero Departement",
            animation_frame="Année",  # Animation par année
            title="Effectifs de Police Municipaux par Département (2016-2018)",
            color_continuous_scale="Blues"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        return html.Div([
            html.H2("Carte des Effectifs de Police par Département (2016-2018)"),
            dcc.Graph(figure=fig)
        ])
    elif tab == 'tab-evolution':
        # Graphique pour l'évolution des effectifs dans une ville
        return html.Div([
            html.H2("Évolution des Effectifs de Police Municipaux dans un Département"),
            dcc.Dropdown(
                id='departement-dropdown',
                options=[
                    {'label': f'Département {i}', 'value': str(i).zfill(2)} for i in range(1, 96)
                ],
                value='75',  # Valeur par défaut (Paris)
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
    y="Nombre de policiers municipaux",
    title=f"Évolution des Effectifs de Police Municipaux dans le Département {departement}",
     # Pour colorier les barres en fonction de l'année
    labels={"Nombre de policiers municipaux": "Nombre de policiers municipaux", "Année": "Année"},
    barmode="group"  # Affiche les barres côte à côte pour chaque année si besoin
)
    fig.update_layout(xaxis_title="Année", yaxis_title="Nombre de policiers municipaux")
    return fig

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
