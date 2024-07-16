from my_plotly_package.plotly_utils import criar_grafico_barras, processo_geojson_municipio, mapa_coropletico, criar_grafico_pizza_simples, card_porcentagem, card, criar_grafico_pizza_simples, processo_geojson_regiao
import dash
from dash import html, dcc, Input, Output, State, callback, Dash, register_page, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import psycopg2

register_page(__name__, path='/framework')


###################################################### CONEXAO TABELA DO BANCO  ################################################################

conexao_info = {
    'database': "db_dados_tratados",
    'host': "10.111.9.167",
    'user': "user_dados_tratados",
    'password': "Tr@tADOS_PrOc355ing",
    'port': "5432"
}

def executar_consulta(query):
    with psycopg2.connect(**conexao_info) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(query)
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
    return pd.DataFrame(resultados, columns=colunas)

query4 = "SELECT * FROM painel_python.tabela_bivalente_cobertura_municipios"
df_municipio = executar_consulta(query4)

###################################################### ESPAÇO PARA ETL, TRATAMENTO DOS DADOS, AGRUPAMENTOS  ################################################################













################################################################################################### ESTILIZAÇÃO ################################################################
markdown_text = '''
Exemplo para aplicar Markdown no painel.
'''

tab_card = {'height': '100%'}

config_graph={"displayModeBar": False, "showTips": False, 'scrollZoom': False, "showTips": True}


labels={'Faixa Etaria': 'Faixa Etaria', 'Contagem Doses': 'Contagem Doses'}

cores_matriz = {
    'Masculino': '#ff9999',
    'Feminino': '#66b3ff',
}

################################################################################################### DROPDOWNS, SELECT BOX ################################################################

# Criar a lista de opções para o Dropdown
municipio_options = [{'label': municipio, 'value': municipio} for municipio in sorted(df_municipio['municipio'].unique())]
dropdown_municipios = dcc.Dropdown(
    id='select-municipio-bivalente2',
    options=municipio_options,    #value=municipio_options[0]['value'],  # Define um valor inicial do select box
    clearable=True,
    placeholder="Selecione um Municipio"  
)
                                                                                                    #############
# Criar a lista de opções para o Dropdown
regiao_options = [{'label': regiao, 'value': regiao} for regiao in df_municipio['regiao_saude'].unique()]
dropdown_regiao = dcc.Dropdown(
    id='select-regiao2',
    options=regiao_options,    #value=municipio_options[0]['value'],  # Define um valor inicial do select box
    clearable=True,
    placeholder="Selecione uma Região"
  
)
                                                                                                    #############

options_sexo = [{'label': sexo, 'value': sexo} for sexo in df_municipio['sexo'].unique()]
dropdown_sexo = dcc.Dropdown(
    id='select-sexo-municipio2',
    options=options_sexo,
    clearable=True,
    placeholder="Selecione um Sexo"
    )

limpar_filtro = dbc.Button("Limpar Filtro", id='limpar-filtro-btn2', n_clicks=0, size="sm", color="success")


################################################################################################### GRAFICOS ################################################################








################################################################################################### CALLBACK ################################################################








################################################################################################### LOGICA DO FILTRO ################################################################

# def update_graphs(selected_municipio):
#     if selected_municipio:





#     return 

################################################################################################### LAYOUT ################################################################



@callback(
    dash.dependencies.Output("modal2", "is_open"),
    [dash.dependencies.Input("open2", "n_clicks"),
     dash.dependencies.Input("close2", "n_clicks")],
    [dash.dependencies.State("modal2", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open


layout = html.Div([
    #LINHA 1
    dbc.Row([
        #COLUNA 1 - LINHA 1
        dbc.Col(width=4),  # Espaço extra à esquerda, se necessário

        #COLUNA 2 - LINHA 1
        dbc.Col([
        ], width=4),

        #COLUNA 3 - LINHA 1
        dbc.Col(width=4),  # Espaço extra à esquerda, se necessário
    ], style={'width': '100%'}, className='mt-2'),  # Removido cálculo da altura


    #LINHA 2
    #DROPDOWNS
    dbc.Row([
        dbc.Col([
            dbc.Col([
                html.Img(
                    src="https://www.saude.sc.gov.br/images/stories/website/2023_marca_ses.png",
                    alt="Logotipo da Saúde SC",
                    style={'width': '70%', 'height': '70%', 'margin-top': '10px'}
                )
            ], style={'text-align': 'center'}),  # Add text-align: center
        ], sm=2, lg=2),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Dropdown(
                        id='select-municipio-bivalente2',
                        #options=municipio_options,
                        clearable=True,
                        placeholder="Selecione um Município"
                    ),
                ]),
                style={'border': 0}
            ),
            sm=9,
            lg=2
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        dropdown_sexo
                    ]),
                ]),
                style={'border': 0}
            ),
            sm=9,
            lg=2
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        dropdown_regiao
                    ]),
                ]),
                style={'border': 0}
            ),
            sm=9,
            lg=2
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        limpar_filtro
                    ])
                ]),
                style={'border': 0}
            ),
            sm=9,
            lg=2
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dbc.Button("Informações", id="open2", color='success'),
                
                    # Modal que contém as informações em Markdown
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Informações Adicionais"),
                            dbc.ModalBody(dcc.Markdown(children=markdown_text)),
                            dbc.ModalFooter(
                                dbc.Button("Fechar", id="close2", className="ml-auto")
                            ),
                        ],
                        id="modal2",
                        size="lg"  # Define o tamanho do modal (sm, md, lg, xl)
                        #centered=True  # Centraliza o modal na tela
                    ),
                ]),
                style={'border': 0}
            ),
            sm=9,
            lg=2
        ),


    ], style={'margin-bottom': '0px', 'background-color': 'white'}, className='sticky-top'),


    #LINHA 3 CARDS
    dbc.Row([
        #COLUNA 1 - LINHA 3
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                ]),
                style={'border': 0}
            )
        ],sm=2, lg=2),

        #COLUNA 2 - LINHA 3
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                ]),
                style={'backgroundColor': '#f8f9fa'}
            ),
            xs=12, sm=6, md=4, lg=2, xl=2,
            className="mb-4"  # Adiciona um espaçamento na parte inferior quando os cards empilham
        ),

        #COLUNA 3 - LINHA 3
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                ),
                style={'backgroundColor': '#f8f9fa'}
            ),
            xs=12, sm=6, md=4, lg=2, xl=2,
            className="mb-4"  # Adiciona um espaçamento na parte inferior quando os cards empilham
        ),

        #COLUNA 4 - LINHA 3
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                        #dcc.Graph(id='card-populacao',config=config_graph),
                ),
                style={'backgroundColor': '#f8f9fa'}
            ),
            xs=12, sm=6, md=4, lg=2, xl=2,
            className="mb-4"  # Adiciona um espaçamento na parte inferior quando os cards empilham
        ),
        #COLUNA 5 - LINHA 3
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                        #cc.Graph(id='card2-test', config=config_graph),
                ),
                style={'backgroundColor': '#f8f9fa'}  # Defina a cor de fundo do card inteiro
            ),
            xs=12, sm=6, md=4, lg=2, xl=2,
            className="mb-4"  # Adiciona um espaçamento na parte inferior quando os cards empilham
        ),
    ], style={'margin-bottom': '0px'}),  # Remover a altura fixa


    # LINHA 4
    dbc.Row([
        #COLUNA 1 - LINHA 4
        dbc.Col([
            dbc.Card([
                        #dcc.Graph(id='mapa-coropletico',config=config_graph),
            ], style={'border': 0})
        ], sm=6, md=6, lg=6),

        #COLUNA 2 - LINHA 4
        dbc.Col([
            dbc.Card([
                        #dcc.Graph(id='bar-chart',config=config_graph),
            ], style={'border': 0})
        ], sm=6, md=6, lg=6)

    ], style={'width': '100%', 'margin-bottom': '0px'}),


    # LINHA 5
    dbc.Row([
        #COLUNA 1 - LINHA 5
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        #dcc.Graph(id='bar-chart1', config=config_graph),
                ], style={'padding': '10px'})  # Adjust padding as needed
            ],style={'border': 0})
        ], sm=6, md=6, lg=6),

        #COLUNA 2 - LINHA 5
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        #dcc.Graph(config=config_graph),
                ], style={'padding': '10px'})  # Adjust padding as needed
            ],style={'border': 0})
        ], sm=6, md=6, lg=6)

    ], style={'width': '100%', 'margin-bottom': '0px'}),


    # LINHA 6
    dbc.Row([
        #COLUNA 1 - LINHA 6
        dbc.Col([
            dbc.Card([
                     dbc.CardBody([
                        #dcc.Graph(id='mapacoropletico2',config=config_graph),
                        ], style={'border':0, 'overflow-x':'auto', 'weidth':'90%'})
            ],style={'border':0})
        ], sm=12, md=12, lg=12),
    ], style={'width': '100%', 'margin-bottom': '0px'}),


    # LINHA 7
    # linha para adicionar tabela e gerar tabela em excel
    dbc.Row([
        #COLUNA 1 - LINHA 7
        dbc.Col([

        ], sm=12, md=12, lg=12),
    ], style={'width': '100%', 'height': '100%'}),
    dcc.Download(id='download-excel-bivalente-regiao2'),


], style={'width': '100%', 'height': '100%'})







