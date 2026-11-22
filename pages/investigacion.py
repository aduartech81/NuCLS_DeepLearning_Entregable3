from pathlib import Path
import json
import dash
from dash import html, dcc, Input, Output, callback
ROOT = Path(__file__).resolve().parents[1]
ROWS = json.loads((ROOT/'revision/novedad_20261118/matriz.json').read_text())
dash.register_page(__name__, path='/investigacion', name='Novedad y protocolo')
layout = html.Div([
 html.Span('04 / NOVEDAD Y PROTOCOLO · 18 NOV 2026', className='eyebrow'),
 html.H1(['Una diferencia concreta.', html.Br(), html.Span('Una prueba por construir.', className='accent')]),
 html.P('CICO explora una corrección contextual acotada por desacuerdo entre orientaciones. La revisión no acredita todavía originalidad ni superioridad.', className='lead'),
 html.Div([html.Div([html.Small('ANTECEDENTES'),html.H2(str(len(ROWS))),html.P('Con nivel de lectura explícito')],className='card'),html.Div([html.Small('PILOTO VERIFICADO'),html.H2('5'),html.P('Cinco semillas completas; resultados exploratorios en Piloto')],className='card'),html.Div([html.Small('ABLACIONES VERIFICADAS'),html.H2('15 / 15'),html.P('Cinco semillas por variante; evidencia exploratoria')],className='card')],className='grid'),
 html.H2('Qué existe y qué propone CICO'),
 html.P('Selecciona un antecedente para ver el solapamiento, la diferencia candidata y el alcance de la lectura.'),
 dcc.Dropdown(id='antecedente-e3', options=[{'label':r['titulo'],'value':i} for i,r in enumerate(ROWS)], value=0,clearable=False),
 html.Div(id='antecedente-detalle-e3',className='panel'),
 html.H2('Secuencia de evidencia'),
 html.Div([html.Div(t,className='stage') for t in ['Datos auditados','Piloto de cinco semillas','Diagnóstico y potencia','Comparación final']],className='flow'),
 html.Div([html.H2('La receta vigente permanece fija'),html.P('β = 0,5 · λ = 1 · ancho = 16 · batch = 32 · máximo 25 épocas · paciencia 5. Solo train y validación. El plazo no transforma este piloto en confirmación.'),html.P('La región central no es una máscara nuclear. La dispersión no es incertidumbre calibrada. El costo incluye ocho pases del encoder.')],className='panel'),
 html.Details([html.Summary('Consultar plan de interpretación y criterios de integración'),dcc.Markdown((ROOT/'book/07_plan_lectura.md').read_text())],className='panel'),
 html.P('Los antecedentes aquí listados son vigilancia de novedad; no modifican los conteos PRISMA de E1/E2.')])
@callback(Output('antecedente-detalle-e3','children'),Input('antecedente-e3','value'))
def detalle_antecedente(index):
 r=ROWS[int(index)]
 return [html.H3(r['titulo']),html.Small(r['lectura']),html.P(r['antecedente']),html.P(r['diferencia_o_limite']),html.A('Consultar fuente primaria ↗',href=r['url'],target='_blank',rel='noopener noreferrer')]

import plotly.express as px
lit=json.loads((ROOT/'data/proyecto/literatura.json').read_text())
lf=px.bar(x=list(lit['estados_mutuamente_excluyentes']),y=list(lit['estados_mutuamente_excluyentes'].values()),labels={'x':'Decisión documentada','y':'Registros'},template='plotly_white',color_discrete_sequence=['#087f8c'])
lf.update_layout(height=470,margin=dict(t=20,b=150),xaxis_tickangle=-35)
layout.children.insert(3,html.Section([html.H2('E1 · trazabilidad de la revisión de literatura'),html.P('1.717 registros identificados en Scopus, Web of Science e IEEE Xplore; 1.330 unidades de cribado. Corte documental: 8 noviembre 2026.'),dcc.Graph(figure=lf),html.P(lit['nota'],className='note'),html.P('Estos conteos pertenecen a la revisión heredada; no se suman a los antecedentes de novedad E3.')],className='panel'))

