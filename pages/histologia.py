from pathlib import Path
import json
import dash
from dash import html,dcc,Input,Output,callback
import plotly.graph_objects as go

dash.register_page(__name__,path='/histologia',name='Histología')
ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'data/histologia/casos.json').read_text())
LABELS={'tumor_nonMitotic':'Tumor no mitótico','lymphocyte':'Linfocito','nonTILnonMQ_stromal':'Estroma no TIL / no macrófago'}
def dropdown(id,title,opts):
 return html.Div([html.Label(title,htmlFor=id),dcc.Dropdown(id=id,options=[{'label':'Todos','value':'todos'}]+[{'label':label,'value':key} for key,label in opts],value='todos',clearable=False)])
layout=html.Div([html.Span('TEJIDO · ANOTACIÓN · PREDICCIÓN',className='eyebrow'),html.H1('La histología, en primer plano'),html.P('Explora el campo original y el núcleo anotado. Contrasta la referencia del conjunto con la predicción histórica del modelo.',className='lead'),html.Div([html.Div([html.H2('36'),html.P('núcleos diferentes')],className='card'),html.Div([html.H2('21'),html.P('pacientes de validación')],className='card'),html.Div([html.H2('18 + 18'),html.P('aciertos y discrepancias seleccionados')],className='card')],className='grid'),html.Div([dropdown('h-clase','Clase de referencia',list(LABELS.items())),dropdown('h-modelo','Modelo',[(v,v) for v in ['resnet50','densenet121','softmaxcnn_bn']]),dropdown('h-resultado','Resultado',[('acierto','Acierto'),('discrepancia','Discrepancia')])],className='hist-filters'),html.Label('Caso para inspeccionar',htmlFor='h-caso'),dcc.Dropdown(id='h-caso',clearable=False),html.Div(id='h-viewer'),html.H2('Exploración de los casos'),html.P('Selecciona un caso en el visor superior para examinarlo en detalle. Las miniaturas conservan el color original.'),html.Div(id='h-grid',className='hist-grid'),html.Div([html.H2('Cómo interpretar estas imágenes'),html.P('La línea amarilla sigue la anotación original del núcleo objetivo. Una anotación rectangular no equivale a segmentación. No es un mapa de atención ni Grad-CAM.'),html.P('Se muestra el campo de contexto original, no el recorte exacto de 128 × 128 usado por el clasificador. Las probabilidades corresponden a predicciones históricas de E2, semilla 6113; no son predicciones de CICO.'),html.P('Selección ilustrativa de dos casos por modelo, clase y resultado: no estima prevalencias ni tasas de acierto. Se cotejaron 6.147 predicciones sobre 2.049 núcleos de validación. No se muestran imágenes de reserva.'),html.A('Descargar trazabilidad de los casos',href='/histologia-evidencia/casos.json'),html.P('E3: la comparación visual con CICO se incorporará cuando sus predicciones estén disponibles. No se atribuyen causas morfológicas a las discrepancias sin revisión experta.')],className='notice')])
def selected(clase,modelo,resultado):
 return [r for r in CASES if (clase=='todos' or r['clase_real']==clase) and (modelo=='todos' or r['modelo']==modelo) and (resultado=='todos' or r['acierto']==(resultado=='acierto'))]
@callback(Output('h-caso','options'),Output('h-caso','value'),Output('h-grid','children'),Input('h-clase','value'),Input('h-modelo','value'),Input('h-resultado','value'))
def filter_cases(clase,modelo,resultado):
 rows=selected(clase,modelo,resultado)
 opts=[{'label':f"Caso {r['caso']} · {LABELS[r['clase_real']]} · {r['modelo']} · "+('Acierto' if r['acierto'] else 'Discrepancia'),'value':r['caso']} for r in rows]
 cards=[html.Figure([html.Img(src=f"/histologia-imagen/{r['caso']}/anotada",alt=f"Caso {r['caso']}: núcleo anotado, {LABELS[r['clase_real']]}"),html.Figcaption([html.Strong(f"Caso {r['caso']} · {LABELS[r['clase_real']]}"),html.P(r['modelo']+' · '+('Acierto' if r['acierto'] else 'Discrepancia'))])],className='hist-card') for r in rows]
 return opts,rows[0]['caso'] if rows else None,cards
@callback(Output('h-viewer','children'),Input('h-caso','value'))
def show_case(case):
 if not case:return html.P('No hay casos para esta combinación.')
 r=next(x for x in CASES if x['caso']==case)
 fig=go.Figure(go.Bar(x=[float(r[k]) for k in ['p_tumor','p_linfocito','p_estroma']],y=['Tumor no mitótico','Linfocito','Estroma'],orientation='h',marker_color=['#9e83b5','#328b98','#dba45e'],text=[f"{float(r[k]):.1%}" for k in ['p_tumor','p_linfocito','p_estroma']],textposition='auto'))
 fig.update_layout(height=230,margin=dict(l=145,r=25,t=15,b=40),xaxis=dict(range=[0,1],tickformat='.0%',title='Probabilidad registrada'),font=dict(size=14),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
 return [html.Div([html.H2(f"Caso {case} · "+('Acierto' if r['acierto'] else 'Discrepancia')),html.P(f"Referencia: {LABELS[r['clase_real']]} · Predicción: {LABELS[r['clase_predicha']]}"),html.P(f"{r['modelo']} · Semilla {r['semilla']} · Validación · Anotación {r['tipo']}")],className='hist-case-heading'),html.Div([html.Figure([html.H3(title),html.A(html.Img(src=f'/histologia-imagen/{case}/{mode}',alt=title+' del caso '+case),href=f'/histologia-imagen/{case}/{mode}',target='_blank'),html.Figcaption('Pulsa la imagen para abrirla y ampliarla.')]) for mode,title in [('limpia','Campo histológico original'),('anotada','Núcleo objetivo anotado')]],className='hist-pair'),dcc.Graph(figure=fig,config={'displayModeBar':False}),html.Details([html.Summary('Procedencia y verificación'),html.P(f"Paciente del conjunto público: {r['paciente']} · Fila de anotación: {r['fila']} · Campo: {r['dimensiones_campo'][0]} × {r['dimensiones_campo'][1]} px"),html.P('SHA-256 del campo original: '+r['sha_campo']),html.P('Fuente de predicciones: '+r['fuente_predicciones'])])]
