# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np
# from plotly.io import write_html
# import plotly.express as px
# import plotly
# import dash 
# from dash import Dash, html, dcc, Input, Output



# effectot = "C:\Users\romai\OneDrive\Documents\Esiee\E4\\effectif_total2.cv"



# gapminder = px.data.gapminder()  # (1)
# years = gapminder["year"].unique()
# data = {year: gapminder.query("year == @year") for year in years}  # (2)


# # Initialiser l'application Dash
# app = Dash(__name__)  # (3)

# # Layout de l'application
# app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'row'}, children=[
#     # Colonne de gauche pour le graphique
#     html.Div(style={'flex': '70%', 'padding': '20px'}, children=[
#         html.H1(children='Espérance de vie vs PIB par habitant',
#                 style={'textAlign': 'center', 'color': '#7FDBFF'}),  # (5)

#         dcc.Dropdown(
#             id='year-dropdown',
#             options=[{'label': str(year), 'value': year} for year in years],
#             value=2002,  # Valeur par défaut
#         ),

#         dcc.Graph(id='graph1'),  # Graphique dynamique
#     ]),

#     # Colonne de droite pour les boutons et le contenu
#     html.Div(style={'flex': '30%', 'padding': '20px'}, children=[
#         html.Button('Afficher la carte', id='map-button', n_clicks=0),
#         html.Button('Afficher le texte', id='text-button', n_clicks=0),
#         html.Button('Afficher un autre graphique', id='graph2-button', n_clicks=0),

#         html.Div(id='dynamic-content', style={'marginTop': '20px'}),
#     ])
# ])

# # Callback pour mettre à jour le graphique en fonction de l'année sélectionnée
# @app.callback(
#     Output('graph1', 'figure'),  # (1)
#     Input('year-dropdown', 'value')  # (2)
# )
# def update_figure(input_value):  # (3)
#     filtered_data = data[input_value]
#     return px.scatter(filtered_data, x="gdpPercap", y="lifeExp",
#                        color="continent", size="pop",
#                        hover_name="country")  # (4)

# # Callback pour afficher le contenu dynamique
# @app.callback(
#     Output('dynamic-content', 'children'),
#     Input('map-button', 'n_clicks'),
#     Input('text-button', 'n_clicks'),
#     Input('graph2-button', 'n_clicks'),
# )
# def display_content(map_clicks, text_clicks, graph2_clicks):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         return "Sélectionnez un bouton pour afficher du contenu."
    
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]

#     if button_id == 'map-button':
#         return dcc.Graph(figure=px.choropleth(gapminder, locations="iso_alpha", color="lifeExp", 
#                                                hover_name="country", animation_frame="year", 
#                                                title="Carte de l'espérance de vie"))
#     elif button_id == 'text-button':
#         return html.Div("Voici un texte explicatif sur les données.")
#     elif button_id == 'graph2-button':
#         return dcc.Graph(figure=px.bar(gapminder.query("year == 2007"), x="continent", y="pop",
#                                         title="Population par continent en 2007"))

# if __name__ == '__main__':
#     app.run_server(debug=True)  # (8)






import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.io import write_html
import plotly.express as px
import dash 
from dash import Dash, html, dcc, Input, Output

# Chemin d'accès vers le fichier CSV
effectot_chemin = "C:\\Users\\romai\\OneDrive\\Documents\\Esiee\\E4\\effectif_total2.csv"

# Chargement du fichier CSV dans un DataFrame
effectot = pd.read_csv(effectot_chemin)

# Vérification des années uniques dans les données
years = effectot["year"].unique()
data = {year: effectot.query("year == @year") for year in years}

# Initialiser l'application Dash
app = Dash(__name__)

# Layout de l'application
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'row'}, children=[
    # Colonne de gauche pour le graphique
    html.Div(style={'flex': '70%', 'padding': '20px'}, children=[
        html.H1(children='Espérance de vie vs PIB par habitant',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),

        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in years],
            value=years[0],  # Valeur par défaut à la première année disponible
        ),

        dcc.Graph(id='graph1'),  # Graphique dynamique
    ]),

    # Colonne de droite pour les boutons et le contenu
    html.Div(style={'flex': '30%', 'padding': '20px'}, children=[
        html.Button('Afficher la carte', id='map-button', n_clicks=0),
        html.Button('Afficher le texte', id='text-button', n_clicks=0),
        html.Button('Afficher un autre graphique', id='graph2-button', n_clicks=0),

        html.Div(id='dynamic-content', style={'marginTop': '20px'}),
    ])
])

# Callback pour mettre à jour le graphique en fonction de l'année sélectionnée
@app.callback(
    Output('graph1', 'figure'),
    Input('year-dropdown', 'value')
)
def update_figure(input_value):
    filtered_data = data[input_value]
    return px.scatter(filtered_data, x="gdpPercap", y="lifeExp",
                       color="continent", size="pop",
                       hover_name="country")

# Callback pour afficher le contenu dynamique
@app.callback(
    Output('dynamic-content', 'children'),
    Input('map-button', 'n_clicks'),
    Input('text-button', 'n_clicks'),
    Input('graph2-button', 'n_clicks'),
)
def display_content(map_clicks, text_clicks, graph2_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "Sélectionnez un bouton pour afficher du contenu."
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'map-button':
        return dcc.Graph(figure=px.choropleth(effectot, locations="iso_alpha", color="lifeExp", 
                                               hover_name="country", animation_frame="year", 
                                               title="Carte de l'espérance de vie"))
    elif button_id == 'text-button':
        return html.Div("Voici un texte explicatif sur les données.")
    elif button_id == 'graph2-button':
        return dcc.Graph(figure=px.bar(effectot.query("year == 2007"), x="continent", y="pop",
                                        title="Population par continent en 2007"))

if __name__ == '__main__':
    app.run_server(debug=True)

