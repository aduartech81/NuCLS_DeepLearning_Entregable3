from pathlib import Path
import json,dash
from dash import html,dcc,Input,Output,callback
import numpy as np
import plotly.graph_objects as go
D=json.loads((Path(__file__).resolve().parents[1]/'data/diagnosticos/eda.json').read_text());G=D['groups'];colors=['#087f8c','#b36b45','#72518f']
dash.register_page(__name__,path='/eda-e3',name='EDA del piloto')
layout=html.Div([html.H1('EDA del manifiesto E3'),html.P('Corte del piloto: 14.539 train y 2.049 validación. Todos los gráficos de esta página responden a ambos filtros. Los diagnósticos históricos E1/E2 permanecen separados.'),html.Label('Particiones'),dcc.Dropdown(id='ee-split',options=['train','validation'],value=['train','validation'],multi=True),html.Label('Clases'),dcc.Dropdown(id='ee-class',options=sorted({r['clase'] for r in G}),value=sorted({r['clase'] for r in G}),multi=True),html.Div(id='ee-note',className='notice'),dcc.Graph(id='ee-count'),html.P('Hallazgo de recuentos: la clase dominante se recalcula en el resumen según la selección; no se confunde el número de recortes con pacientes independientes.'),dcc.Graph(id='ee-intensity'),html.P('Las intensidades medias aproximadas y la composición de la selección se calculan arriba a partir de los histogramas. Las diferencias de apariencia no identifican por sí mismas su causa ni prueban cambio de dominio.'),dcc.Graph(id='ee-duplicates'),html.P('La representación de pacientes cambia por clase: un paciente puede aparecer en varias barras y no debe contarse dos veces como independiente. La auditoría no encontró duplicados exactos; eso no descarta similitud visual.'),html.P(f"Manifiesto completo: {D['duplicate_groups']} grupos duplicados exactos; {D['cross_split_pixel_groups']} compartidos entre train/validación; {D['conflicting_label_groups']} con etiquetas distintas. No equivale a una auditoría humana del ruido de etiquetas."),html.A('Volver al EDA histórico',href='/datos')])
@callback(Output('ee-count','figure'),Output('ee-intensity','figure'),Output('ee-duplicates','figure'),Output('ee-note','children'),Input('ee-split','value'),Input('ee-class','value'))
def show(splits,classes):
 rows=[r for r in G if r['split'] in (splits or []) and r['clase'] in (classes or [])];a=go.Figure();b=go.Figure();c=go.Figure()
 for i,cl in enumerate(sorted(classes or [])):
  rr=[r for r in rows if r['clase']==cl]
  if not rr:continue
  a.add_bar(x=[r['split'] for r in rr],y=[r['n'] for r in rr],name=cl,marker_color=colors[i%3]);c.add_bar(x=[r['split'] for r in rr],y=[r['patients'] for r in rr],name=cl,marker_color=colors[i%3]);h=np.sum([r['hist'] for r in rr],axis=0)
  for k,ch in enumerate(['R','G','B']):b.add_scatter(x=list(range(8,256,16)),y=(h[k]/h[k].sum()).tolist(),name=cl+' · '+ch,mode='lines',line={'color':colors[i%3],'dash':['solid','dash','dot'][k]})
 for f,title,y in [(a,'Recortes por clase y partición','Recortes'),(b,'Intensidad por canal y clase · 16 intervalos','Fracción de píxeles'),(c,'Pacientes representados por clase · no sumar entre clases','Pacientes')]:f.update_layout(title=title,template='plotly_white',barmode='group',yaxis_title=y,legend={'orientation':'h'},margin={'t':60,'b':90})
 total=sum(r['n'] for r in rows);tot={cl:sum(r['n'] for r in rows if r['clase']==cl) for cl in classes or []};dominant=max(tot,key=tot.get) if total else 'ninguna'
 summaries=[]
 for split in splits or []:
  rr=[r for r in rows if r['split']==split];n=sum(r['n'] for r in rr)
  if not n:continue
  hh=np.sum([r['hist'] for r in rr],axis=0);mu=(hh@np.arange(8,256,16))/hh.sum(1)
  comp=', '.join(f"{r['clase']}: {r['n']} ({100*r['n']/n:.1f} %)" for r in rr)
  summaries.append(html.P(f"{split}: {n:,} recortes. {comp}. RGB medio aproximado: {mu[0]:.1f}, {mu[1]:.1f}, {mu[2]:.1f} / 255."))
 return a,b,c,[html.Strong(f'{total:,} recortes seleccionados. Clase más frecuente: {dominant}.'),*summaries,html.P('RGB aproximado por centros de 16 intervalos; no media exacta por imagen. Las curvas se normalizan por clase. No son medidas de pacientes independientes.')]

