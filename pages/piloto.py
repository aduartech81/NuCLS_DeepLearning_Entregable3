from pathlib import Path
import json,statistics
import dash
from dash import html,dcc,dash_table
import plotly.graph_objects as go
ROOT=Path(__file__).resolve().parents[1]
dash.register_page(__name__,path='/piloto',name='Piloto E3')
def layout():
 d=json.loads((ROOT/'data/piloto_estado.json').read_text());runs=d.get('runs',[])
 fig=go.Figure();loss=go.Figure();rows=[]
 for run in runs:
  h=run['history'];fig.add_trace(go.Scatter(x=[x['epoch'] for x in h],y=[x['val_macro_f1'] for x in h],mode='lines+markers',name=str(run['seed'])))
  loss.add_trace(go.Scatter(x=[x['epoch'] for x in h],y=[x['loss'] for x in h],mode='lines+markers',name=str(run['seed'])))
  rows.append({'Semilla':run['seed'],'Épocas':len(h),'Mejor época':run['best_epoch'],'Macro-F1 validación':round(run['val_macro_f1'],6)})
 for f,y in [(fig,'Macro-F1 de validación'),(loss,'Pérdida de entrenamiento')]:f.update_layout(template='plotly_white',xaxis_title='Época',yaxis_title=y,legend_title='Semilla',font=dict(size=14))
 fig.update_yaxes(range=[0,1]);scores=[x['val_macro_f1'] for x in runs]
 return html.Div([html.Span('PILOTO / EVIDENCIA E3',className='eyebrow'),html.H1('Cinco semillas. Evidencia verificada.'),html.P('Actualizado: '+d['updated'],className='lead'),html.Div([html.H2(str(d['complete_seeds'])+' / '+str(d['planned_seeds'])+' semillas completas verificadas'),html.P(d['source']),html.P(f"Media ± DE: {statistics.mean(scores):.4f} ± {statistics.stdev(scores):.4f}. La DE no es un intervalo de confianza.")],className='panel'),dash_table.DataTable(data=rows,columns=[{'name':k,'id':k} for k in rows[0]],export_format='csv',style_table={'overflowX':'auto'},style_cell={'fontSize':16,'padding':14,'textAlign':'left'}),html.H2('Trayectorias de validación'),dcc.Graph(figure=fig),html.H2('Aprendizaje en entrenamiento'),dcc.Graph(figure=loss),html.Div([html.H2('Por qué tres semillas terminan en época 6'),html.P('6103–6105 tuvieron su mejor checkpoint en época 1 y acumularon cinco épocas sin mejora. La parada es coherente con el protocolo, pero evidencia variación entre semillas y exige discutir optimización y estabilidad. No se reiniciaron corridas para mejorar su resultado.')],className='panel'),html.P('Cada resultado corresponde al checkpoint seleccionado por validación. Esta misma validación no es una prueba independiente; no demuestra superioridad frente a E1/E2. Las cinco semillas no sustituyen el benchmark final ni la potencia exigida.'),html.A('Leer resultados y verificación',href='/libro/14_resultados_piloto.html',className='button'),html.A('Ver avance de ablaciones',href='/ablaciones',className='button secondary'),html.A('Consultar pendientes',href='/libro/14_estado_entrega.html',className='button secondary')])
