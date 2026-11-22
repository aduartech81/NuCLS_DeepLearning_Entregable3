from pathlib import Path
import json
import dash
from dash import html,dcc,dash_table,Input,Output,callback
import plotly.graph_objects as go
dash.register_page(__name__,path='/ablaciones',name='Ablaciones E3')
D=json.loads((Path(__file__).resolve().parents[1]/'data/ablaciones_verificadas.json').read_text())
LABELS={'cico_completo':'CICO completo','sin_contraste':'Sin contraste','sin_amortiguacion':'Sin amortiguación','sin_contexto':'Sin contexto'}
def curve(seed):
 f=go.Figure()
 for r in D['corridas']:
  if r['semilla']==int(seed):f.add_trace(go.Scatter(x=[h['epoch'] for h in r['historia']],y=[h['val_macro_f1'] for h in r['historia']],name=LABELS[r['variante']],mode='lines+markers'))
 f.update_layout(template='plotly_white',xaxis_title='Época (parada temprana real)',yaxis_title='Macro-F1 de validación',height=440,legend=dict(orientation='h'))
 return f
@callback(Output('abl-curvas','figure'),Input('abl-semilla','value'))
def update_curve(seed):return curve(seed)
def layout():
 fig=go.Figure()
 for seed in range(6101,6106):
  rows=[x for x in D['corridas'] if x['semilla']==seed]
  fig.add_trace(go.Scatter(x=[LABELS[x['variante']] for x in rows],y=[x['macro_f1'] for x in rows],mode='lines+markers',name=str(seed)))
 fig.update_layout(template='plotly_white',yaxis_title='Macro-F1 de validación',height=420,legend_title='Semilla emparejada')
 summary=[dict(variante=LABELS[x['variante']],media=round(x['media'],4),sd=round(x['sd'],4),delta=round(x['delta_vs_cico'],4),p_holm=x.get('p_holm3','—')) for x in D['resumen']]
 return html.Div([html.Span('E3 / RESULTADOS VERIFICADOS',className='eyebrow'),html.H1('Ablaciones: resultados y límites'),html.H2('15 de 15 ablaciones verificadas'),html.P('91 archivos coinciden con el manifiesto SHA-256. Métricas recalculadas desde predicciones; comparación con cinco corridas CICO sobre las mismas 2.049 imágenes de 21 pacientes.'),html.P('El modelo completo no supera consistentemente las variantes. Ningún contraste resulta significativo. Esto no demuestra equivalencia ni valida superioridad clínica.',className='notice'),dcc.Graph(figure=fig),dash_table.DataTable(data=summary,columns=[{'name':k,'id':k} for k in summary[0]],style_table={'overflowX':'auto'},style_cell={'padding':12,'textAlign':'left'}),html.P('Media ± SD entre cinco semillas. Delta = variante − CICO. Prueba exacta pareada bilateral por signos (32 permutaciones); Holm para tres contrastes. Análisis exploratorio sobre checkpoints elegidos por validación, sin test independiente.'),html.H2('Curvas reales de entrenamiento'),html.Label('Semilla',htmlFor='abl-semilla'),dcc.Dropdown(id='abl-semilla',options=[{'label':str(s),'value':s} for s in range(6101,6106)],value=6101,clearable=False),dcc.Graph(id='abl-curvas',figure=curve(6101)),html.H2('Lo que aún exige E3'),html.Ul([html.Li('Base sin todos los componentes, componentes por separado y controles adicionales de D4 y capacidad.'),html.Li('Benchmark final común con Top10 y bases fuertes, mínimo diez semillas y potencia 0,90.'),html.Li('Partición confirmatoria independiente y tres datasets externos definidos antes de examinar resultados.'),html.Li('Pruebas complementarias, intervalos de efecto y corrección por familia; estas ablaciones no cierran esos requisitos.')]),html.H2('PCam — E2'),html.P('Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado.'),html.A('Descargar resultados e historias verificados',href='/assets/ablaciones_verificadas.json',className='button'),html.Br(),html.A('Leer análisis en el libro',href='/libro/15_ablaciones_y_transicion.html',className='button')])
