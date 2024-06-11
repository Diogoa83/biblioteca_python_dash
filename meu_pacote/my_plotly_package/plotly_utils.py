
import numpy as np
import json
import unidecode
import geopandas as gpd
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json



def criar_grafico_barras(dataframe, x_valores, y_valores, titulo, altura, largura, matriz, coluna_rotulo, cores_matriz, nome_eixos, orientacao):
    fig2 = px.bar(
        dataframe,
        x=x_valores,
        y=y_valores,
        color=matriz,
        title=titulo,
        barmode='group',
        text=coluna_rotulo,
        color_discrete_map=cores_matriz,
        labels=nome_eixos,
        orientation=orientacao  # Adicionando a orientação horizontal
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        width=largura,
        height=altura,
        xaxis_title=x_valores,
        yaxis_title=y_valores
    )

    fig2.update_layout(
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.1,
            xanchor="center",
            x=-0.12
        )
    )
    return fig2


def processo_geojson(dataframe, geojson_path):
    with open(geojson_path, 'r', encoding='utf-8') as geojson_file:
        geojson_data = json.load(geojson_file)
        
    geojson_df = pd.DataFrame(geojson_data['features'])
    geojson_df['GEOCODIGO'] = geojson_df['properties'].apply(lambda x: x.get('GEOCODIGO'))
    geojson_df['Municipio'] = geojson_df['properties'].apply(lambda x: x.get('Municipio'))
    geojson_df['Municipio'] = geojson_df['Municipio'].str.upper()
    
    merged_data = pd.merge(dataframe, geojson_df, left_on='Municipio', right_on='Municipio', how='left')
    
    gdf_geojson = gpd.GeoDataFrame.from_features(geojson_data['features'])
    gdf_geojson.crs = 'EPSG:4326'
    gdf_geojson['Municipio'] = gdf_geojson['Municipio'].str.upper()
    gdf_geojson = gdf_geojson.merge(merged_data, left_on='Municipio', right_on='Municipio', how='left')
    
    gdf_geojson = gpd.GeoDataFrame(gdf_geojson, geometry='geometry_x', crs='EPSG:4326')
    geojson_for_plot = json.loads(gdf_geojson.to_json())
    
    return geojson_for_plot




def mapa_coropletico(dataframe, geojson, localizacao, key_geojson, coloracao, hover_data, estilo_mapa, zoom, coordenadas_centralizar, opacite, escala_coloracao, largura, altura, titulo):
    """
    Cria um mapa coroplético usando Plotly Express.

    Parametros:
    dataframe = DataFrame contendo os dados a serem plotados.
    geojson = Dados GeoJSON para o mapa.
    localizacao = Nome da coluna no DataFrame que contém os identificadores de localização.
    key_geojson = Chave no GeoJSON que corresponde aos identificadores de localização.
    coloracao = Nome da coluna no DataFrame para definir a cor.
    hover_data = Lista de colunas no DataFrame para exibir nos dados de hover.
    estilo_mapa  = Estilo do mapa Mapbox.
    zoom = Nível de zoom do mapa.
    coordenadas_centralizar = Dicionário com 'lat' e 'lon' para centralizar o mapa.
    opacite = Opacidade das áreas do mapa.
    escala_coloracao = Escala de cores para o mapa.
    largura = Largura da figura.
    altura = Altura da figura.
    titulo = Título do mapa.

    Returns:
    Figure: Figura do Plotly Express.
    """
    
    figure = px.choropleth_mapbox(
        dataframe,
        geojson=geojson,
        locations=localizacao,
        featureidkey=key_geojson,
        color=coloracao,
        hover_data=hover_data,
        mapbox_style=estilo_mapa,
        zoom=zoom,
        center=coordenadas_centralizar,
        opacity=opacite,
        color_continuous_scale=escala_coloracao,
        color_continuous_midpoint=True
    )
    figure.update_layout(
        width=largura,
        height=altura,
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            yanchor="bottom",
            len=0.5,
            y=0.05,
            xanchor="left",
            x=0.05
        ),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title_text=titulo,
        title_x=0.5,
        title_font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    )
    return figure