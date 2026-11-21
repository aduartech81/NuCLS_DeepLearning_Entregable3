from pathlib import Path
import json
import dash
from dash import html,dcc,dash_table
import plotly.graph_objects as go
dash.register_page(__name__,path='/ablaciones',name='Ablaciones E3')
def layout():
 d=json.loads((Path(__file__).resolve().parents[1]/'data/ablaciones_estado.json').read_text())
 variants=['sin_contraste','sin_amortiguacion','sin_contexto'];labels=['Sin contraste','Sin amortiguación','Sin contexto']
 matrix=[[2 if x['estado']=='Completa reportada' else 1 if x['estado']=='Reanudación reportada' else 0 for x in d['runs'] if x['variante']==v] for v in variants]
 fig=go.Figure(go.Heatmap(z=matrix,x=[str(s) for s in range(6101,6106)],y=labels,zmin=0,zmax=2,colorscale=[[0,'#e2e8f0'],[.49,'#e2e8f0'],[.5,'#fbbf24'],[.99,'#fbbf24'],[1,'#14b8a6']],showscale=False,hovertemplate='%{y} · semilla %{x}<extra></extra>'))
 fig.update_layout(template='plotly_white',height=300,margin=dict(l=160,r=20,t=20,b=40),xaxis_title='Semilla')
 return html.Div([html.Span('E3 / ABLACIONES',className='eyebrow'),html.H1('Qué aporta cada componente'),html.P(d['corte']),html.P(d['fuente'],className='notice'),html.H2('4 de 15 corridas completas reportadas'),html.P('Verde: completa reportada · amarillo: reanudación reportada · gris: pendiente.'),dcc.Graph(figure=fig),html.P('La última salida reporta sin_amortiguacion / 6102 en ejecución, con época 3 guardada. No confirma progreso posterior ni métricas finales.'),dash_table.DataTable(data=d['runs'],columns=[{'name':k.replace('_',' ').capitalize(),'id':k} for k in ['variante','semilla','estado','ultima_epoca_guardada']],style_table={'overflowX':'auto'},style_cell={'padding':12,'textAlign':'left'}),html.H2('Comparación prevista'),html.P('Mismo conjunto train/validation, semillas y receta. Cada variante cambia un único control. Se compararán semillas emparejadas con CICO completo; las corridas pendientes no se tratarán como ceros ni se mezclarán tamaños de muestra.'),html.P('El control adicional sin D4 queda pendiente. No se atribuye superioridad, efecto causal clínico ni cumplimiento del benchmark final a este avance.'),html.A('Leer protocolo y estado',href='/libro/15_ablaciones_y_transicion.html',className='button')])
