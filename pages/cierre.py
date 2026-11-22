from pathlib import Path
import json
PCAM_ESTADO=json.loads((Path(__file__).resolve().parents[1]/'data/pcam_estado.json').read_text())['estado']
from pathlib import Path
import json
import dash
from dash import html,dcc
import plotly.graph_objects as go
dash.register_page(__name__,path='/cierre',name='Cierre CPU')
e=json.loads((Path(__file__).resolve().parents[1]/'data/cierre_cpu.json').read_text())
rows=e['reserva65']['diagnosticos_ensambles']
from src.plots import intervalos_por_paciente
f=intervalos_por_paciente(rows)
layout=html.Div([html.Span('EVIDENCIA / 21 NOVIEMBRE 2026',className='eyebrow'),html.H1('Cierre documental y análisis CPU'),html.P('66 corridas de desarrollo auditadas; 65 evaluaciones de reserva cotejadas. No se repitió ningún entrenamiento.',className='lead'),html.Div([html.H2('Qué se comprobó'),html.Ul([html.Li(x) for x in e['bases66']['comprobado']]),html.P(e['bases66']['limite'])],className='panel'),dcc.Graph(figure=f),html.P('Tres ensambles de cinco semillas seleccionados por validación. Reserva histórica expuesta: 969 recortes de solo seis pacientes. Los intervalos no acreditan confirmación independiente ni cobertura clínica.',className='notice'),html.H2('Errores listos para revisión humana'),html.P('Se prepararon 100 errores por ensamble, 300 filas en total. Las categorías y decisiones humanas siguen vacías. Esta preparación no cierra la adjudicación exigida por modelo.'),html.H2('Pendientes que siguen abiertos'),html.Ul([html.Li('15 ablaciones recibidas y verificadas; completar controles y evaluación final E3.'),html.Li(PCAM_ESTADO),html.Li('Calibración independiente, cobertura, validación externa, fidelidad y estabilidad de explicaciones.'),html.Li('Revisión bibliográfica, licencia y autoría, reproducción por tercero y sustentación.')]),html.A('Leer cierre y paquete de reproducibilidad',href='/libro/18_cierre_cpu.html',className='button')])

import pandas as pd
from dash import Input,Output,callback
master=pd.read_csv(Path(__file__).resolve().parents[1]/'data/tabla_maestra_disponible.csv')
layout.children.extend([html.H2('Tabla maestra disponible'),html.P('Seleccione un corte. Las poblaciones diferentes no forman un ranking conjunto. Faltan los resultados finales aún no recibidos.'),dcc.Dropdown(id='master-stage',options=master.etapa.unique().tolist(),value=master.etapa.iloc[0],clearable=False),html.Div(id='master-table')])
@callback(Output('master-table','children'),Input('master-stage','value'))
def table(stage):
 d=master[master.etapa==stage].sort_values('macro_f1',ascending=False)
 return html.Table([html.Thead(html.Tr([html.Th(x) for x in ['Modelo','Semillas','Macro-F1','DE semillas']])),html.Tbody([html.Tr([html.Td(x.modelo),html.Td(x.semillas),html.Td(f'{x.macro_f1:.4f}'),html.Td(f'{x.sd_semillas:.4f}')]) for x in d.itertuples()])])
