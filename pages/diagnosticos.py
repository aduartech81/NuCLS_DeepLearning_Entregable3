from pathlib import Path
import json,dash
from dash import html,dcc,Input,Output,callback,dash_table
import plotly.graph_objects as go
P=Path(__file__).resolve().parents[1]/'data/diagnosticos'
D=json.loads((P/'cico.json').read_text());C=json.loads((P/'contrastes.json').read_text());LABELS=['tumor','linfocito','estroma'];COLORS=['#087f8c','#b36b45','#72518f']
dash.register_page(__name__,path='/diagnosticos',name='Diagnósticos CICO')
layout=html.Div([html.H1('CICO: diagnósticos y contraste exploratorio'),html.P('Predicciones originales verificadas de las cinco semillas. Validación: 2.049 recortes de 21 pacientes, usada para elegir checkpoints. No es una prueba independiente.'),html.Label('Semilla',htmlFor='diag-seed'),dcc.Dropdown(id='diag-seed',options=list(D),value='6101',clearable=False),html.Div(id='diag-summary',className='notice'),html.Div([dcc.Graph(id='diag-cm'),dcc.Graph(id='diag-roc'),dcc.Graph(id='diag-pr'),dcc.Graph(id='diag-cal')],className='grid'),html.P('ROC y PR: uno contra el resto. AUC y AP calculadas con todos los umbrales; se reducen puntos solo para dibujar. PR depende de la prevalencia. Confiabilidad: 10 intervalos fijos de confianza máxima; no se ha ajustado un calibrador.'),html.H2('CICO frente a tres bases: mismos recortes y cinco semillas'),html.P(C['scope']),dash_table.DataTable(data=[{k:round(r[k],5) if isinstance(r[k],float) else r[k] for k in ['modelo','cico_media','base_media','diferencia_media','dz','p','p_holm','mde80_normal_aprox']} for r in C['tests']],columns=[{'name':k,'id':k} for k in ['modelo','cico_media','base_media','diferencia_media','dz','p','p_holm','mde80_normal_aprox']],export_format='csv',style_table={'overflowX':'auto'},style_cell={'whiteSpace':'normal','height':'auto','minWidth':'90px','padding':'10px'}),html.P('Hallazgo: CICO presenta menor Macro-F1 medio que las tres bases en este corte. p de Holm = 0,1875 no demuestra equivalencia ni superioridad. Δ = CICO − base; d_z = media de las diferencias / DE de las diferencias. Contraste bilateral exacto de rangos con signo; Holm sobre tres contrastes.'),html.P(C['power'],className='notice'),html.P(C['seed_uncertainty']),html.A('Ver métodos, evidencia y límites en el libro',href='/libro/19_contexto_y_diagnosticos.html')])
@callback(Output('diag-cm','figure'),Output('diag-roc','figure'),Output('diag-pr','figure'),Output('diag-cal','figure'),Output('diag-summary','children'),Input('diag-seed','value'))
def figures(seed):
 r=D[str(seed)];cm=go.Figure(go.Heatmap(z=r['cm'],x=LABELS,y=LABELS,text=r['cm'],texttemplate='%{text}',colorscale=[[0,'#faf8f5'],[1,'#087f8c']],showscale=False));cm.update_layout(title='Matriz de confusión · recuentos',xaxis_title='Predicción',yaxis_title='Referencia',yaxis={'autorange':'reversed'})
 roc=go.Figure();pr=go.Figure();cal=go.Figure()
 for i,c in enumerate(r['curves']):
  roc.add_scatter(x=c['roc_x'],y=c['roc_y'],mode='lines',name=f"{c['clase']} · AUC {c['auc']:.3f}",line={'color':COLORS[i]})
  pr.add_scatter(x=c['recall'],y=c['precision'],mode='lines',name=f"{c['clase']} · AP {c['ap']:.3f} · prevalencia {c['prevalencia']:.2f}",line={'color':COLORS[i]})
 roc.add_scatter(x=[0,1],y=[0,1],mode='lines',name='Azar',line={'color':'#54677a','dash':'dot'})
 roc.update_layout(title='ROC por clase',xaxis_title='Tasa de falsos positivos',yaxis_title='Sensibilidad')
 pr.update_layout(title='Precisión–recobrado por clase',xaxis_title='Recobrado',yaxis_title='Precisión')
 cal.add_scatter(x=[0,1],y=[0,1],name='Ideal',mode='lines',line={'color':'#54677a','dash':'dot'});cal.add_scatter(x=[b['confidence'] for b in r['bins']],y=[b['accuracy'] for b in r['bins']],text=[f"n={b['n']}" for b in r['bins']],name='Observado sin calibrar',mode='lines+markers',line={'color':'#087f8c'})
 cal.update_layout(title='Confiabilidad · confianza máxima',xaxis_title='Confianza media del intervalo',yaxis_title='Fracción correcta')
 for f in [cm,roc,pr,cal]:f.update_layout(template='plotly_white',height=430,margin={'t':65,'l':55,'r':20,'b':60},legend={'orientation':'h','y':-0.25})
 for f in [roc,pr,cal]:f.update_xaxes(range=[0,1]);f.update_yaxes(range=[0,1])
 text=f"Semilla {seed} · Macro-F1 {r['macro_f1']:.4f} · exactitud {r['accuracy']:.4f} · Brier multiclase (suma) {r['brier']:.4f} · ECE de 10 intervalos {r['ece']:.4f}. Hallazgo: la distancia a la diagonal mide desajuste observado de confianza; no acredita calibración externa."
 return cm,roc,pr,cal,text

layout.children.append(html.A('Comprobar mapas y planificación estadística',href='/calidad-explicaciones',className='button'))
