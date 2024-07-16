from my_plotly_package.plotly_utils import criar_grafico_barras, processo_geojson_municipio, mapa_coropletico, criar_grafico_pizza_simples, card_porcentagem, card, criar_grafico_pizza_simples, processo_geojson_regiao
import dash
from dash import html, dcc, Input, Output, State, callback, Dash, register_page, dash_table
import dash_bootstrap_components as dbc

import geopandas as gpd
from unidecode import unidecode
import pandas as pd
import json
from dash.dependencies import Input, Output, State
import psycopg2

register_page(__name__, path='/framework_test')



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

#query2 = "SELECT * FROM painel_python.bivalente_doses_faixaetaria_mun"
query4 = "SELECT * FROM painel_python.tabela_bivalente_cobertura_municipios"
query = "SELECT * FROM painel_python.tabela_monovalente_cobertura_municipios"


data = executar_consulta(query)
df_municipio = executar_consulta(query4)

###################################################### ETL, TRATAMENTO DOS DADOS, AGRUPAMENTOS  ################################################################


df_municipio = df_municipio.rename(columns={'regiao_saude':'Região Saude','municipio':'Municipio', 'sexo':'Sexo', 'pop':'População', 'contagem_dose':'Numero de Vacinas', 'porcentagem':'Porcentagem (%)', 'faixa_etaria':'Faixa Etaria'})

#df_regiao = df_regiao.rename (columns={'regiao_saude':'Região Saude', 'sexo':'Sexo', 'pop':'População', 'contagem_dose':'Numero de Vacinas', 'porcentagem':'Porcentagem (%)', 'faixa_etaria':'Faixa Etaria'})


primeiradose = data[data['dose']=='1ª DOSE']

primeiradose = primeiradose.rename(columns={'municipio_paciente':'Municipio', 'sexo':'Sexo', 'contagem_dose':'Contagem Doses'})
primeiradose_municipio = primeiradose.groupby(['Municipio', 'Sexo']).agg({'Contagem Doses':'sum', 'pop':'sum'}).reset_index()


labels={'Faixa Etaria': 'Faixa Etaria', 'Contagem Doses': 'Contagem Doses'}




pizza_simples = primeiradose_municipio.groupby(['Municipio','Sexo']).agg({'Contagem Doses':'sum'}).reset_index()

################################################################################################### ESTILIZAÇÃO ################################################################
markdown_text = '''
Exemplo para aplicar Markdown no painel.
'''

cores_matriz = {'Masculino': '#8ac0de', 'Feminino': '#f5c9bf'}



cores_matriz2 = {
    'Masculino': '#ff9999',
    'Feminino': '#66b3ff',
}


# ========== Styles ============ #
tab_card = {'height': '100%'}

config_graph={"displayModeBar": False, "showTips": False, 'scrollZoom': False, "showTips": True}

################################################################################################### DROPDOWNS, SELECT BOX ################################################################

# Criar a lista de opções para o Dropdown
municipio_options = [{'label': municipio, 'value': municipio} for municipio in sorted( primeiradose_municipio['Municipio'].unique())]
dropdown_municipios = dcc.Dropdown(
    id='select-municipio-bivalente',
    options=municipio_options,    #value=municipio_options[0]['value'],  # Define um valor inicial do select box
    clearable=True,
    placeholder="Selecione um Municipio"  
)
                                                                                                    #############
# Criar a lista de opções para o Dropdown
regiao_options = [{'label': regiao, 'value': regiao} for regiao in df_municipio['Região Saude'].unique()]
dropdown_regiao = dcc.Dropdown(
    id='select-regiao',
    options=regiao_options,    #value=municipio_options[0]['value'],  # Define um valor inicial do select box
    clearable=True,
    placeholder="Selecione uma Região"
  
)
                                                                                                    #############

options_sexo = [{'label': sexo, 'value': sexo} for sexo in df_municipio['Sexo'].unique()]
dropdown_sexo = dcc.Dropdown(
    id='select-sexo-municipio',
    options=options_sexo,
    clearable=True,
    placeholder="Selecione um Sexo"
    )

limpar_filtro = dbc.Button("Limpar Filtro", id='limpar-filtro-btn', n_clicks=0, size="sm", color="success")


################################################################################################### GRAFICOS ################################################################


    # Uso da função
geojson_path3 = r"C:\Users\jesusda\Documents\VSCode Projetos\projeto_dash\SC2.json" # caminho
geojson_for_plot3 = processo_geojson_municipio(primeiradose_municipio, geojson_path3)

################################################################################################### CALLBACK ################################################################
# CALLBACK PARA ABA DE INFORMAÇÕES
# Callback para abrir e fechar o modal




@callback(
    [
     Output('bar-chart-vertical', 'figure'),
     Output('bar-chart-horizontal', 'figure'),
     Output('card-total', 'figure'),
     Output('card-porcentagem', 'figure'),
     Output('card-numero-doses', 'figure'),
     Output('grafico-pizza', 'figure'),
     Output('mapacoropletico', 'figure')
    ],
    [
     Input('select-municipio-bivalente', 'value')
    ]
)

################################################################################################### LOGICA DO FILTRO ################################################################

def update_graphs(selected_municipio):
    if selected_municipio:
        filtered_df = primeiradose_municipio[primeiradose_municipio['Municipio'] == selected_municipio]
        total = df_municipio[df_municipio['Municipio'] == selected_municipio]['População'].sum()
        contagem_doses = df_municipio[df_municipio['Municipio'] == selected_municipio]['Numero de Vacinas'].sum()
        pizza = pizza_simples[pizza_simples['Municipio'] == selected_municipio]
        porcentagem = contagem_doses / total * 100
        
        # Filtrando GeoJSON
        selected_feature = next((feature for feature in geojson_for_plot3["features"] if feature["properties"]["Municipio"] == selected_municipio), None)
        if selected_feature:
            # Calcular o centro do polígono
            coords = selected_feature["geometry"]["coordinates"][0]
            latitude = sum([point[1] for point in coords]) / len(coords)
            longitude = sum([point[0] for point in coords]) / len(coords)
            mapa_filtrado = {
                "type": geojson_for_plot3["type"],
                "features": [selected_feature]
            }
            zoom = 9
        else:
            latitude = -27.5954
            longitude = -51.024735
            zoom = 9
            mapa_filtrado = geojson_for_plot3


    else:
        filtered_df = primeiradose_municipio
        total = df_municipio['População'].sum()
        contagem_doses = df_municipio['Numero de Vacinas'].sum()
        porcentagem = contagem_doses / total * 100
        pizza = pizza_simples.groupby(['Sexo']).agg({'Contagem Doses':'sum'}).reset_index()
        mapa_filtrado = geojson_for_plot3
        latitude = -27.5954
        longitude = -51.024735
        zoom = 6



    fig_vertical = criar_grafico_barras(
        filtered_df.head(20), 
        'Municipio', 
        'Contagem Doses', 
        'Contagem de Doses por Município', 
        500, 
        900, 
        'Sexo',
        'Contagem Doses',
        cores_matriz,
        labels,
        'v'
    )

    fig_horizontal = criar_grafico_barras(
        filtered_df.head(20), 
        'Contagem Doses', 
        'Municipio', 
        'Contagem de Doses por Município', 
        500, 
        900, 
        'Sexo',
        'Contagem Doses',
        cores_matriz,
        labels,
        'h'
    )

    mapa = mapa_coropletico(
        primeiradose_municipio,
        mapa_filtrado,
        'Municipio',
        'properties.Municipio',
        'Contagem Doses',
        ['Municipio', 'Contagem Doses'],
        'white-bg',
        zoom,
        {"lat": latitude, "lon": longitude},
        1,
        "Teal",
        400,
        1000,
        'Vacinação'
    )

    total = f"{total:,.0f}".replace(',', '.')
    contagem_doses = f"{contagem_doses:,.0f}".replace(',', '.')



    grafico_pizza = criar_grafico_pizza_simples(pizza, 'Contagem Doses', 'Sexo', 'Grafico de Pizza por Municipio e Sexo', 400, 1000, cores_matriz2)
    card_populacao = card(total, 80, 200, "População Total")
    card_numero_doses = card(contagem_doses, 80, 200, "Contagem Doses")
    porcentagem_ = card_porcentagem(porcentagem, 80, 200, "Porcentagem (%)")

    return fig_vertical, fig_horizontal, card_populacao, porcentagem_, card_numero_doses, grafico_pizza, mapa

################################################################################################### LAYOUT ################################################################


@callback(
    dash.dependencies.Output("modal", "is_open"),
    [dash.dependencies.Input("open", "n_clicks"),
     dash.dependencies.Input("close", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
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


    # Define o layout do aplicativo
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
                        id='select-municipio-bivalente',
                        options=municipio_options,
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
                        #dropdown_sexo
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
                        #dropdown_regiao
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
                        #limpar_filtro
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
                    dbc.Button("Informações", id="open", color='success'),
                
                    # Modal que contém as informações em Markdown
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Informações Adicionais"),
                            dbc.ModalBody(dcc.Markdown(children=markdown_text)),
                            dbc.ModalFooter(
                                dbc.Button("Fechar", id="close", className="ml-auto")
                            ),
                        ],
                        id="modal",
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


    #LINHA 3
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
                        dcc.Graph(id='card-total', config=config_graph),
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
                        dcc.Graph(id='card-porcentagem', config=config_graph),
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
                        dcc.Graph(id='card-numero-doses', config=config_graph),
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
                dcc.Graph(id='bar-chart-horizontal', config=config_graph),
            ], style={'border': 0})
        ], sm=6, md=6, lg=6),

        #COLUNA 2 - LINHA 4
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='bar-chart-vertical', config=config_graph),
            ], style={'border': 0})
        ], sm=6, md=6, lg=6)

    ], style={'width': '95%', 'margin-bottom': '0px'}),


    # LINHA 5
    dbc.Row([
        #COLUNA 1 - LINHA 5
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        dcc.Graph(id='grafico-pizza', config=config_graph),
                ], style={'padding': '10px'})  # Adjust padding as needed
            ],style={'border': 0})
        ], sm=6, md=6, lg=6),

        #COLUNA 2 - LINHA 5
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        dcc.Graph(id='mapacoropletico', config=config_graph),
                ], style={'padding': '10px'})  # Adjust padding as needed
            ],style={'border': 0})
        ], sm=6, md=6, lg=6)

    ], style={'width': '95%', 'margin-bottom': '0px'}),


    # LINHA 6
    dbc.Row([
        #COLUNA 1 - LINHA 6
        dbc.Col([
            dbc.Card([
                     dbc.CardBody([
                            dcc.Graph(id='mapacoropletico-regiao'),
                        ], style={'border':0, 'overflow-x':'auto', 'weidth':'90%'})
            ],style={'border':0})
        ], sm=12, md=12, lg=12),
    ], style={'width': '95%', 'margin-bottom': '0px'}),

    # LINHA 7
    # linha para adicionar tabela e gerar tabela em excel
    dbc.Row([
        #COLUNA 1 - LINHA 7
        dbc.Col([

        ], sm=12, md=12, lg=12),
    ], style={'width': '95%', 'height': '100%'}),
    dcc.Download(id='download-excel-bivalente-regiao'),

    # LINHA 8
    # linha para adicionar tabela e gerar tabela em excel
    dbc.Row([
        #COLUNA 1 - LINHA 8
        dbc.Col([

        ], sm=12, md=12, lg=12),
    ], style={'width': '95%', 'height': '100%'}),
    dcc.Download(id='download-excel-bivalente-municipio')


], style={'width': '95%', 'height': '100%'})







