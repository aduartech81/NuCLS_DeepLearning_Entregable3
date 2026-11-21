from pathlib import Path
import json
import dash
from dash import html,dcc,Input,Output,callback,dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__,path='/proyecto',name='Proyecto completo')
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'data/proyecto'; E=ROOT/'data/heredado_e2'
base=pd.read_csv(P/'e1_resumen.csv'); expanded=pd.read_csv(P/'bases22.csv'); summary=pd.read_csv(E/'resumen_reserva.csv'); runs=pd.read_csv(E/'metricas_por_semilla.csv'); costs=pd.read_csv(E/'costos_resumen.csv'); contrasts=pd.read_csv(P/'contrastes22.csv')
def graph(fig):
 fig.update_layout(template='plotly_white',font=dict(family='Arial',size=14),paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=30,r=25,t=35,b=45))
 return dcc.Graph(figure=fig,config={'displaylogo':False})
def table(df):
 return dash_table.DataTable(data=df.round(5).to_dict('records'),columns=[{'name':c.replace('_',' '),'id':c} for c in df],page_size=13,sort_action='native',filter_action='native',export_format='csv',style_table={'overflowX':'auto'},style_cell={'textAlign':'left','fontFamily':'Arial','fontSize':14,'padding':'12px','minWidth':100,'maxWidth':270,'whiteSpace':'normal'},style_header={'backgroundColor':'#eaf0f5','fontWeight':'bold'})
def panel(title,body,note=None):return html.Section([html.H2(title),html.P(note,className='note') if note else None,body],className='panel')
layout=html.Div([html.Span('PROYECTO FINAL / E1 + E2 + E3',className='eyebrow'),html.H1('De los baselines al modelo propio.'),html.P('Explore la evidencia acumulada sin confundir etapas, particiones ni niveles de validación.',className='lead'),html.Div([html.Div([html.Label('Etapa experimental'),dcc.Dropdown(id='scope-final',options=[{'label':'E1 · baselines originales (11 semillas)','value':'E1'},{'label':'E2 · baselines ampliados (22 semillas)','value':'E2-validacion'},{'label':'E2 · reserva histórica (13 modelos × 5 semillas)','value':'E2-reserva'}],value='E2-reserva',clearable=False)],className='filter'),html.Div([html.Label('Arquitecturas de interés'),dcc.Dropdown(id='models-final',multi=True,placeholder='Todas las arquitecturas')],className='filter')],className='filters'),html.Div(id='project-evidence'),panel('E3 · aporte y límite actual',html.Div([html.Div([html.H3('CICO'),html.P('Centro + contexto acotado por desacuerdo entre ocho vistas D4. Una propiedad algebraica no demuestra superioridad predictiva.')]),html.A('Ver curvas del piloto',href='/piloto',className='button'),html.A('Revisar diseño y ecuación',href='/modelos',className='button secondary')]),'El piloto E3 no se agrega al ranking de reserva: corresponde a otra etapa y todavía no hay resultados finales recibidos.'),panel('Ablaciones de preprocesamiento E2',table(pd.read_csv(E/'ablaciones_contrastes.csv')),'15 corridas históricas; no sustituyen ablaciones propias CICO. Ausencia de significación no demuestra equivalencia.'),panel('Ensambles y calibración E2',table(pd.read_csv(E/'resumen_ensembles.csv')),'Resultados históricos en reserva; no constituyen evaluación independiente E3.'),panel('Mapa de arquitecturas de E2',html.Div([html.Details([html.Summary(p.stem.replace('_',' ')),html.Img(src='/assets/proyecto/'+p.name,alt='Diagrama de arquitectura '+p.stem,style={'width':'100%','background':'white'})]) for p in sorted((ROOT/'assets/proyecto').glob('*.svg')) if p.stem not in ['confusion_reserva_cierre11','calibracion_reserva_cierre11','flujo_literatura','PRISMA_E2_parcial']],className='architecture-grid'),'Diagramas bibliográficos heredados de E2; abrir cada arquitectura para examinarla.')])
@callback(Output('models-final','options'),Output('models-final','value'),Input('scope-final','value'))
def options(scope):
 names=summary.modelo.tolist() if scope=='E2-reserva' else base.modelo.tolist()
 return [{'label':n,'value':n} for n in names],[]
@callback(Output('project-evidence','children'),Input('scope-final','value'),Input('models-final','value'))
def render_evidence(scope,models):
 if scope=='E2-reserva':
  d=summary.copy(); d=d[d.modelo.isin(models)] if models else d
  d=d.sort_values('macro_f1_media'); selected=runs[runs.modelo.isin(d.modelo)]
  fig=px.bar(d,x='macro_f1_media',y='modelo',orientation='h',error_x='macro_f1_sd',color='macro_f1_media',color_continuous_scale='Teal',labels={'macro_f1_media':'Macro-F1 medio ± DE entre semillas','modelo':''});fig.update_layout(height=540,xaxis_range=[0,1],coloraxis_showscale=False)
  box=px.box(selected,x='modelo',y='macro_f1',points='all',color='modelo',labels={'macro_f1':'Macro-F1 · reserva','modelo':''});box.update_layout(showlegend=False,height=460)
  heat=selected.groupby('modelo')[['macro_f1','accuracy','balanced_accuracy','auc_macro','ap_macro']].mean()
  hf=px.imshow(heat,text_auto='.3f',zmin=0,zmax=1,color_continuous_scale='Teal',aspect='auto');hf.update_layout(height=max(340,len(heat)*32))
  c=costs.merge(d,on='modelo'); cf=px.scatter(c,x='parametros',y='macro_f1_media',hover_name='modelo',size='memoria_pico_inferencia_bytes',color='modelo',log_x=True,labels={'parametros':'Parámetros (escala log)','macro_f1_media':'Macro-F1 histórico'});cf.update_layout(showlegend=False)
  return [html.Div('Reserva histórica: 969 recortes, 6 pacientes. E2 reporta 65 evaluaciones; PCam está detenido.',className='notice'),panel('Comparación de arquitecturas',graph(fig),'Barras de error: desviación entre cinco semillas, no intervalo por paciente. Mayor media no demuestra superioridad.'),panel('Variabilidad entre ejecuciones',graph(box)),panel('Perfil de métricas',graph(hf),'Promedios entre semillas. Estas métricas no tienen la misma interpretación ni sustituyen el contraste estadístico.'),panel('Desempeño y complejidad',graph(cf),'Tamaño del punto: memoria pico de inferencia del registro histórico. No es una medición nueva de CPU en Render.'),panel('Tabla verificable y exportable',table(d),'IC95_paciente es el intervalo por paciente. Se conserva separado de la desviación entre semillas.')]
 if scope=='E1':
  d=base.copy(); d=d[d.modelo.isin(models)] if models else d
  melted=d.melt(id_vars=['modelo'],value_vars=['macro_f1_val_media','macro_f1_reserva_media'],var_name='particion',value_name='Macro-F1')
  fig=px.bar(melted,x='modelo',y='Macro-F1',color='particion',barmode='group',color_discrete_sequence=['#087f8c','#a75383']);fig.update_yaxes(range=[0,1])
  return [html.Div('E1 · cierre original de 11 semillas. Comparación descriptiva de validación y reserva; no mezclar con las corridas posteriores de E2.',className='notice'),panel('Tres baselines y cambio de dominio',graph(fig)),panel('Resultados originales',table(d)),panel('Dónde se equivoca el modelo',html.Img(src='/assets/proyecto/confusion_reserva_cierre11.svg',alt='Matrices de confusión del cierre E1',className='wide-figure'),'Figura original del cierre E1; no corresponde al piloto CICO.'),panel('Confianza y calibración',html.Img(src='/assets/proyecto/calibracion_reserva_cierre11.svg',alt='Calibración de los modelos E1',className='wide-figure'))]
 d=expanded.copy(); d=d[d.modelo.isin(models)] if models else d
 fig=go.Figure(go.Scatter(x=d.media,y=d.modelo,mode='markers',marker=dict(size=15,color='#087f8c'),error_x=dict(type='data',symmetric=False,array=d.IC95_sup-d.media,arrayminus=d.media-d.IC95_inf)));fig.update_xaxes(title='Macro-F1 de validación · IC95 entre 22 semillas',range=[.65,.85])
 ef=go.Figure(go.Scatter(x=contrasts.diferencia,y=contrasts.comparacion,mode='markers',error_x=dict(type='data',symmetric=False,array=contrasts.IC95_sup-contrasts.diferencia,arrayminus=contrasts.diferencia-contrasts.IC95_inf)));ef.add_vline(x=0,line_dash='dash');ef.update_xaxes(title='Diferencia pareada · IC95')
 return [html.Div('E2 · ampliación de los tres baselines a 22 semillas sobre validación fija. No son 22 pacientes independientes.',className='notice'),panel('Estimación y variabilidad del baseline',graph(fig)),panel('Tamaño de las diferencias',graph(ef),'El intervalo que cruza cero no establece equivalencia. Consultar ajuste de Holm y potencia en la tabla.'),panel('Contrastes, efecto y potencia',table(contrasts)),panel('Resumen de las 66 corridas',table(d))]
