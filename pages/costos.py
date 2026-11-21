from pathlib import Path
import json,dash
from dash import html,dcc,dash_table
import pandas as pd
import plotly.graph_objects as go
R=Path(__file__).resolve().parents[1];P=R/'data/heredado_e2'
df=pd.read_csv(P/'resumen_reserva.csv').merge(pd.read_csv(P/'costos_resumen.csv'),on='modelo');cal=pd.read_csv(P/'metricas_por_semilla.csv').groupby('modelo')[['brier','ece_fijo10']].mean().reset_index();df=df.merge(cal,on='modelo').sort_values('macro_f1_media',ascending=False)
# Strictly empirical frontier in this historical cohort, no uncertainty/superiority claim.
front=[]
for _,r in df.iterrows():
 dominated=((df.parametros<=r.parametros)&(df.macro_f1_media>=r.macro_f1_media)&((df.parametros<r.parametros)|(df.macro_f1_media>r.macro_f1_media))).any()
 if not dominated:front.append(r.modelo)
f=df[df.modelo.isin(front)].sort_values('parametros');fig=go.Figure();fig.add_scatter(x=df.parametros,y=df.macro_f1_media,text=df.modelo,mode='markers',name='13 arquitecturas E2',marker={'color':'#54677a'});fig.add_scatter(x=f.parametros,y=f.macro_f1_media,text=f.modelo,mode='lines+markers',name='No dominados empíricos',line={'color':'#087f8c'});fig.update_layout(template='plotly_white',title='Frontera descriptiva: parámetros vs Macro-F1 de reserva E2',xaxis={'title':'Parámetros (escala log)','type':'log'},yaxis_title='Macro-F1 medio · reserva histórica')
rows=[]
for i,r in enumerate(df.to_dict('records')):rows.append({'puesto_historico':i+1,'modelo':r['modelo'],'particion':'Reserva histórica E2','macro_f1':round(r['macro_f1_media'],4),'parametros':int(r['parametros']),'FLOPs_cubiertos':int(r['FLOPs_operaciones_cubiertas_por_profiler']),'latencia_ms':round(r['latencia_ms_por_recorte_batch32'],4),'entorno':'GPU histórica · por recorte batch32','Brier':round(r['brier'],4),'ECE10':round(r['ece_fijo10'],4)})
meta=json.loads((R/'models/cico_6101.json').read_text());cost=json.loads((R/'data/diagnosticos/costo_cico.json').read_text());diag=json.loads((R/'data/diagnosticos/cico.json').read_text())['6101'];cico={'modelo':'CICO 6101 seleccionado','particion':'Validación E3 (otra partición)','macro_f1':round(diag['macro_f1'],4),'parametros':cost['parametros'],'FLOPs_cubiertos':cost['FLOPs_cubiertos_profiler'],'latencia_ms':round(meta['latency_cpu_local']['median_ms'],4),'entorno':'CPU local · batch1 · mediana','Brier':round(diag['brier'],4),'ECE10':round(diag['ece'],4)}
def table(rows):return dash_table.DataTable(data=rows,columns=[{'name':k,'id':k} for k in rows[0]],sort_action='native',filter_action='native',export_format='csv',style_table={'overflowX':'auto'},style_cell={'whiteSpace':'normal','height':'auto','minWidth':'95px','padding':'10px'})
dash.register_page(__name__,path='/costos',name='Costos y Pareto')
layout=html.Div([html.H1('Costos, calibración observada y frontera descriptiva'),html.P('Top-10 histórico y tres arquitecturas adicionales; todas las filas de esta primera tabla usan la reserva E2. El orden es descriptivo y no acredita superioridad. Brier y ECE son promedios de cinco semillas sin recalibración.'),table(rows),dcc.Graph(figure=fig),html.P('No dominados por menor número de parámetros y mayor Macro-F1 observado: '+', '.join(front)+'. No incorpora incertidumbre y no es una frontera confirmatoria.'),html.H2('CICO separado: otra partición y entorno'),table([cico]),html.P('Las latencias CPU/GPU y batch1/batch32 no son directamente comparables. FLOPs incluye solo operaciones cubiertas por el profiler, no todas las funciones elementales. CICO no se incorpora al ranking ni a la frontera E2.'),html.A('Comparación CICO–bases sobre la misma validación',href='/diagnosticos',className='button'),html.P('El diagrama confirmatorio de diferencia crítica y el Top-10 frente a CICO bajo protocolo común siguen pendientes.')])
