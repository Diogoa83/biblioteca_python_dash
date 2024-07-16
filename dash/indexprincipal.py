import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dbc.Container([
        #html.H1("Vacinometro Bivalente", style={'fontSize': '20px', 'textAlign': 'center'}),
        
        # Botões de navegação
        html.Div([
            dbc.Button(
                page['name'], 
                href=f"/vacinometro-dev{page['path']}", 
                color="success", 
                className="me-1 btn-sm",  # Adiciona a classe 'btn-sm' para diminuir o tamanho do botão
                external_link=True,
                style={'textDecoration': 'none', 'marginTop': '10px'}  # Adiciona espaçamento superior de 10 pixels
            ) for page in dash.page_registry.values()
        ], className="d-flex flex-wrap justify-content-center"),
        html.Hr(),
    ]),
    
    html.Div(dash.page_container),

], style={'height': '100%', 'width': "100%"})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8052)






