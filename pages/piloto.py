from pathlib import Path
import json
import dash
from dash import html,dcc
import plotly.graph_objects as go
ROOT=Path(__file__).resolve().parents[1]
dash.register_page(__name__,path='/piloto',name='Piloto E3')
def layout():
 d=json.loads((ROOT/'data/piloto_estado.json').read_text())
 fig=go.Figure()
 runs=d.get('runs',[{'seed':d.get('seed',6101),'history':d.get('history',[])}])
 for run in runs:
  h=run['history'];fig.add_trace(go.Scatter(x=[x['epoch'] for x in h],y=[x['val_macro_f1'] for x in h],mode='lines+markers',name=str(run['seed'])))
 fig.update_layout(template='plotly_white',xaxis_title='Época',yaxis_title='Macro-F1 de validación',yaxis_range=[0,1],legend_title='Semilla')
 return html.Div([html.Span('PILOTO / EVIDENCIA E3',className='eyebrow'),html.H1('Aprendizaje observado, alcance explícito.'),html.P('Actualizado: '+d['updated']+' · '+d['status'],className='lead'),html.Div([html.H2(str(d['complete_seeds'])+' / '+str(d['planned_seeds'])+' semillas completas recibidas'),html.P(d['source']),html.P('Esta página muestra una instantánea fechada; no consulta ni controla RunPod.')],className='panel'),dcc.Graph(figure=fig),html.P('Cada curva corresponde a validación. No es un resultado en reserva ni una comparación confirmatoria.'),html.Div([html.H2('Qué permite concluir el piloto'),html.P('Mide factibilidad, variación entre semillas y costo. Cinco semillas no sustituyen el mínimo final ni el análisis de potencia de la guía. No se ajusta el protocolo por el mejor punto observado.')],className='panel'),html.A('Procedimiento de integración y entrega →',href='/libro/13_cierre_operativo.html',className='button')])
