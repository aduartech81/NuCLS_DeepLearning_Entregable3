from pathlib import Path
import json,dash
from dash import html,dcc,Input,Output,callback
import numpy as np
import plotly.graph_objects as go
D=json.loads((Path(__file__).resolve().parents[1]/'data/diagnosticos/eda.json').read_text());G=D['groups'];colors=['#087f8c','#b36b45','#72518f']
dash.register_page(__name__,path='/eda-e3',name='EDA del piloto')
layout=html.Div([html.H1('EDA del manifiesto E3'),html.P('Corte del piloto: 14.539 train y 2.049 validación. Todos los gráficos de esta página responden a ambos filtros. Los diagnósticos históricos E1/E2 permanecen separados.'),html.Label('Particiones'),dcc.Dropdown(id='ee-split',options=['train','validation'],value=['train','validation'],multi=True),html.Label('Clases'),dcc.Dropdown(id='ee-class',options=sorted({r['clase'] for r in G}),value=sorted({r['clase'] for r in G}),multi=True),html.Div(id='ee-note',className='notice'),dcc.Graph(id='ee-count'),html.P('Hallazgo de recuentos: la clase dominante se recalcula en el resumen según la selección; no se confunde el número de recortes con pacientes independientes.'),dcc.Graph(id='ee-intensity'),html.P('Hallazgo de color: los canales y clases pueden ocupar intervalos distintos; la distribución describe la tinción y el fondo, no demuestra por sí sola cambio de dominio.'),dcc.Graph(id='ee-duplicates'),html.P('Hallazgo de duplicados: se cuentan registros cuyo hash de píxeles se repite en el manifiesto completo. La ausencia de coincidencias exactas no descarta similitud visual o fuga por paciente.'),html.P(f"Manifiesto completo: {D['duplicate_groups']} grupos duplicados exactos; {D['cross_split_pixel_groups']} compartidos entre train/validación; {D['conflicting_label_groups']} con etiquetas distintas. No equivale a una auditoría humana del ruido de etiquetas."),html.A('Volver al EDA histórico',href='/datos')])
@callback(Output('ee-count','figure'),Output('ee-intensity','figure'),Output('ee-duplicates','figure'),Output('ee-note','children'),Input('ee-split','value'),Input('ee-class','value'))
def show(splits,classes):
 rows=[r for r in G if r['split'] in (splits or []) and r['clase'] in (classes or [])];a=go.Figure();b=go.Figure();c=go.Figure()
 for i,cl in enumerate(sorted(classes or [])):
  rr=[r for r in rows if r['clase']==cl]
  if not rr:continue
  a.add_bar(x=[r['split'] for r in rr],y=[r['n'] for r in rr],name=cl,marker_color=colors[i%3]);c.add_bar(x=[r['split'] for r in rr],y=[r['duplicated_records'] for r in rr],name=cl,marker_color=colors[i%3]);h=np.sum([r['hist'] for r in rr],axis=0)
  for k,ch in enumerate(['R','G','B']):b.add_scatter(x=list(range(8,256,16)),y=(h[k]/h[k].sum()).tolist(),name=cl+' · '+ch,mode='lines',line={'color':colors[i%3],'dash':['solid','dash','dot'][k]})
 for f,title,y in [(a,'Recortes por clase y partición','Recortes'),(b,'Intensidad por canal y clase · 16 intervalos','Fracción de píxeles'),(c,'Registros con duplicación exacta','Registros')]:f.update_layout(title=title,template='plotly_white',barmode='group',yaxis_title=y,legend={'orientation':'h'},margin={'t':60,'b':90})
 total=sum(r['n'] for r in rows);tot={cl:sum(r['n'] for r in rows if r['clase']==cl) for cl in classes or []};dominant=max(tot,key=tot.get) if total else 'ninguna'
 return a,b,c,f'{total:,} recortes seleccionados. Clase más frecuente: {dominant}. Las curvas de color se normalizan dentro de cada clase seleccionada.'
