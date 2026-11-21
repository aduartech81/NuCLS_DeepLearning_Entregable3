from pathlib import Path
import json
import dash
from dash import html,dcc,Input,Output,callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__,path='/datos',name='Datos y EDA')
P=Path(__file__).resolve().parents[1]/'data/proyecto'
classes=pd.read_csv(P/'clases.csv');quality=pd.read_csv(P/'calidad_histogramas.csv');domain=json.loads((P/'dominio.json').read_text())
layout=html.Div([html.Span('DATOS / EXPLORACIÓN / CALIDAD',className='eyebrow'),html.H1('La muestra detrás de cada métrica.'),html.P('Selección histórica de clases E1: 14.428 recortes de entrenamiento y 3.571 de validación. Este corte no se mezcla con el manifiesto del piloto E3 (14.539 y 2.049).',className='lead'),
 dbc.Row([dbc.Col([html.Label('Particiones',htmlFor='eda-splits'),dcc.Dropdown(id='eda-splits',options=classes.particion.unique().tolist(),value=classes.particion.unique().tolist(),multi=True)],md=6),dbc.Col([html.Label('Clases',htmlFor='eda-classes'),dcc.Dropdown(id='eda-classes',options=classes.clase.unique().tolist(),value=classes.clase.unique().tolist(),multi=True)],md=6)],className='g-3 panel'),
 html.P('Ambos filtros actualizan los tres gráficos y los totales de esta sección. Vaciar la selección muestra un estado sin datos.'),html.Div(id='eda-count',role='status',className='notice'),
 dbc.Row([dbc.Col(dcc.Graph(id='eda-counts'),lg=6),dbc.Col(dcc.Graph(id='eda-retention'),lg=6)],className='g-3'),dcc.Graph(id='eda-composition'),
 html.Details([html.Summary('Diagnósticos históricos agregados: otro corte, sin desagregación por los filtros anteriores'),html.P('Los archivos agregados disponibles no permiten cruzar calidad o dominio con clase y partición. Estos gráficos conservan su población original; no cambian con los filtros.'),html.Label('Característica de calidad',htmlFor='quality-feature'),dcc.Dropdown(id='quality-feature',options=[{'label':x.replace('_',' '),'value':x} for x in quality.variable.unique()],value='laplaciano_var',clearable=False),dcc.Graph(id='quality-hist'),dcc.Graph(figure=px.bar(x=['Dominio (2 clases)','Sitio (8 clases)'],y=[domain['dominio']['balanced_accuracy'],domain['sitio']['balanced_accuracy']],text_auto='.3f',labels={'x':'Tarea diagnóstica','y':'Balanced accuracy OOF'},template='plotly_white')),html.P('104 pacientes en dominio y 77 en sitio. Son tareas diferentes; sus alturas no constituyen un ranking.')],className='panel'),
 html.Section([html.H2('Unidad independiente y evidencia visual'),html.P('Los recortes están agrupados por paciente. Un intervalo por paciente difiere de la variación entre semillas.'),html.A('Ver imágenes histológicas y explicación',href='/histologia',className='button'),html.A('Ver diagnóstico y cierre CPU',href='/cierre',className='button secondary')],className='panel')])
@callback(Output('eda-counts','figure'),Output('eda-retention','figure'),Output('eda-composition','figure'),Output('eda-count','children'),Input('eda-splits','value'),Input('eda-classes','value'))
def filter_eda(splits,labels):
 d=classes[classes.particion.isin(splits or [])&classes.clase.isin(labels or [])].copy()
 if d.empty:
  f=px.bar(template='plotly_white');f.add_annotation(text='Sin datos para esta selección',showarrow=False)
  return f,f,f,'0 recortes seleccionados'
 d['retencion_pct']=100*d.incluidas/d.origen;d['composicion_pct']=100*d.incluidas/d.groupby('particion').incluidas.transform('sum')
 common=dict(x='clase',color='particion',barmode='group',template='plotly_white')
 a=px.bar(d,y='incluidas',labels={'incluidas':'Recortes incluidos'},**common)
 b=px.bar(d,y='retencion_pct',labels={'retencion_pct':'Retención frente al origen (%)'},**common);b.update_yaxes(range=[0,100])
 c=px.bar(d,y='composicion_pct',labels={'composicion_pct':'Composición de la selección por partición (%)'},**common);c.update_yaxes(range=[0,100])
 for f in [a,b,c]:f.update_layout(margin=dict(t=25),legend_title_text='Partición')
 return a,b,c,f"{int(d.incluidas.sum()):,} recortes incluidos de {int(d.origen.sum()):,} originales dentro de la selección. Los porcentajes de composición se recalculan por partición."
@callback(Output('quality-hist','figure'),Input('quality-feature','value'))
def histogram(feature):
 if feature not in quality.variable.unique():feature='laplaciano_var'
 d=quality[quality.variable==feature];f=px.bar(d,x='centro',y='cantidad',template='plotly_white',labels={'centro':feature.replace('_',' '),'cantidad':'Imágenes por intervalo'});f.update_traces(marker_color='#087f8c');return f
