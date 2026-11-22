from pathlib import Path
import json
import dash
from dash import html,dcc,Input,Output,State,callback
from src.inference import predict,explain_occlusion,decode_upload
import plotly.graph_objects as go

dash.register_page(__name__,path='/prediccion',name='Predicción CICO')
layout=html.Div([
 html.Div([html.Span('1 · Elige una imagen'),html.Span('2 · Analiza'),html.Span('3 · Interpreta con cautela')],className='prediction-steps'),
 html.Span('CICO / DEMOSTRACIÓN EXPLORATORIA',className='eyebrow'),html.H1('Explorar un recorte histológico'),
 html.P('Carga un recorte RGB de 128 × 128 píxeles, centrado en un núcleo y preparado como los recortes NuCLS. PNG o JPEG, máximo 2 MB. También se admite RGBA completamente opaco. No se admiten láminas completas ni se redimensiona la imagen.',className='lead'),
 html.Div([html.Strong('Modelo piloto · semilla 6101'),html.P('Seleccionado por el mayor macro-F1 de validación entre cinco semillas. Clasifica entre tumor, linfocito y estroma. No detecta automáticamente imágenes fuera del dominio ni acredita utilidad clínica.')],className='notice'),
 html.Div([html.H2('¿Quieres empezar con un ejemplo?'),html.P('Selecciona un recorte real de 128 × 128. La referencia se revela junto al ejemplo; no es una prueba independiente del modelo.'),dcc.Dropdown(id='pred-example',options=[{'label':'Caso '+x['caso']+' · referencia: '+x['clase_referencia'],'value':x['caso']} for x in json.loads((Path(__file__).resolve().parents[1]/'data/ejemplos.json').read_text())],placeholder='Elegir un ejemplo histológico…',clearable=False),html.Div(id='pred-example-info')],className='panel'),
 dcc.Checklist(id='pred-consent',options=[{'label':'Confirmo que es un recorte histológico sin datos personales y entiendo que el resultado es experimental, no un diagnóstico.','value':'yes'}],value=[]),
 dcc.Upload(id='pred-upload',children=html.Div([html.Strong('Seleccionar imagen PNG o JPG'),html.P('También puedes arrastrarla aquí. Primero marca la confirmación de arriba.')]),accept='.png,.jpg,.jpeg,image/png,image/jpeg',disabled=True,multiple=False,max_size=2*1024*1024,style={'border':'2px dashed #137d73','padding':'32px','margin':'24px 0','borderRadius':'12px'}),
 html.Div(id='pred-upload-local',role='status',style={'whiteSpace':'pre-wrap'}),
 dcc.Loading(html.Div(id='pred-upload-status',role='status')),
 html.P('Si el archivo está en Google Drive o iCloud, descárgalo primero al computador. Elegir un nombre no garantiza que el archivo esté disponible.'),
 html.Button('Analizar recorte',id='pred-run',n_clicks=0,className='button',disabled=True),
 dcc.Loading(html.Div(id='pred-result',role='status',style={'marginTop':'24px'})),
 html.P('Al seleccionar una imagen, se envía al servidor de Render para comprobarla y se procesa en memoria. La aplicación no la escribe en archivos ni la incorpora al entrenamiento. Las probabilidades no están calibradas y no expresan certeza clínica.'),
 html.Section([html.H2('¿Qué zonas influyen en esta puntuación?'),html.P('Oculta 64 regiones con el color medio del recorte y mide el cambio en la probabilidad de la clase elegida. Una caída positiva indica sensibilidad a esa región; no identifica células ni demuestra causalidad.'),html.Button('Calcular sensibilidad local',id='explain-run',n_clicks=0,className='button secondary',disabled=True),dcc.Loading(html.Div(id='explain-result',role='status'))],className='panel'),
 html.A('Descargar ejemplos con clase de referencia',href='/ejemplos',className='button'),html.A('Ver diagnósticos y calibración observada',href='/diagnosticos',className='button secondary'),html.A('Leer validación de exportación',href='/libro/16_exportacion_inferencia.html',className='button secondary')])

@callback(Output('pred-result','children'),Input('pred-run','n_clicks'),State('pred-upload','contents'),State('pred-consent','value'),prevent_initial_call=True)
def analyze(n,contents,consent):
 if 'yes' not in (consent or []):return html.P('Marca la confirmación antes de analizar.')
 if not contents:return html.P('Selecciona primero una imagen PNG o JPEG.')
 try:r=predict(contents)
 except ValueError as e:return html.P(str(e))
 except Exception:return html.P('El modelo no está disponible o no superó su comprobación. No se generó una predicción.')
 return html.Div([html.Img(src=contents,alt='Recorte analizado',style={'width':'256px','imageRendering':'auto','maxWidth':'100%'}),html.Div('DOMINIO NO VERIFICADO: una imagen ajena a histología también puede recibir una puntuación alta. No interpretes esta salida si el recorte no corresponde a NuCLS.',className='notice'),html.H2('Clase con mayor puntuación: '+r['prediction']),dcc.Graph(figure=go.Figure(go.Bar(x=r['probabilities'],y=r['labels'],orientation='h',text=[f'{p:.1%}' for p in r['probabilities']],textposition='auto',marker_color='#147d79')).update_layout(template='plotly_white',height=260,xaxis=dict(range=[0,1],tickformat='.0%',title='Puntuación del modelo · no calibrada'),margin=dict(l=90,r=25,t=15,b=50)),config={'displayModeBar':False}),html.Table([html.Thead(html.Tr([html.Th('Clase'),html.Th('Probabilidad del modelo')])) ,html.Tbody([html.Tr([html.Td(label),html.Td(f'{p:.1%}')]) for label,p in zip(r['labels'],r['probabilities'])])]),html.P(f"Tiempo de procesamiento en servidor: {r['latency_ms']:.1f} ms (sin red). Entropía: {r['entropy']:.3f} nats; dispersión de puntuaciones, no cobertura ni certeza clínica."),html.P('Semilla 6101 · tres clases posibles. El modelo siempre asigna una de ellas, incluso si el contenido no corresponde; no usar para decisiones clínicas.')],className='panel')


@callback(Output('explain-result','children'),Input('explain-run','n_clicks'),State('pred-upload','contents'),State('pred-consent','value'),prevent_initial_call=True)
def explain(n,contents,consent):
 if 'yes' not in (consent or []):return html.P('Marca la confirmación antes de analizar.')
 if not contents:return html.P('Selecciona primero una imagen PNG o JPEG.')
 try:r=explain_occlusion(contents)
 except ValueError as e:return html.P(str(e))
 except Exception:return html.P('No se pudo calcular la sensibilidad; no se muestra un mapa sustituto.')
 fig=go.Figure(go.Heatmap(z=r['effects'],x=[8+16*i for i in range(8)],y=[8+16*i for i in range(8)],colorscale='RdBu_r',zmid=0,colorbar={'title':'Caída de prob.'},hovertemplate='x=%{x}, y=%{y}<br>Caída: %{z:.4f}<extra></extra>'))
 fig.update_layout(template='plotly_white',xaxis_title='Posición horizontal (px)',yaxis_title='Posición vertical (px)',yaxis={'autorange':'reversed','scaleanchor':'x'},margin={'t':20},height=420)
 return html.Div([html.H3('Sensibilidad de la puntuación: '+r['target']),html.Div([html.Img(src=contents,alt='Recorte usado para sensibilidad local',style={'width':'100%','maxWidth':'400px'}),dcc.Graph(figure=fig)],className='two-col'),html.P(f"64 regiones de 16 × 16 px · {r['seconds']:.2f} s de servidor. Rojo: al ocultar, baja la puntuación; azul: sube. Un mapa uniforme puede indicar poca sensibilidad a esta intervención."),html.P(r['scope'],className='note')])


@callback(Output('pred-upload-status','children'),Output('pred-run','disabled'),Output('explain-run','disabled'),Output('pred-upload','disabled'),Input('pred-upload','contents'),Input('pred-upload','filename'),Input('pred-consent','value'))
def upload_status(contents,filename,consent):
 if 'yes' not in (consent or []):return html.P('1. Marca la confirmación; después selecciona tu imagen.'),True,True,True
 if not contents:return html.P('2. Selecciona una imagen. Cuando esté cargada aparecerán aquí su nombre y vista previa.'),True,True,False
 try:decode_upload(contents)
 except ValueError as e:return html.Div([html.Strong('La imagen no está lista para analizar. '),html.Span(str(e)),html.P('Elige otro recorte. No se cambia su tamaño automáticamente.')],className='notice'),True,True,False
 return html.Div([html.Strong('Imagen cargada y verificada: '+str(filename or 'recorte')),html.P('RGB · 128 × 128 píxeles. Ahora pulsa «Analizar recorte».'),html.Img(src=contents,alt='Vista previa del archivo cargado',style={'width':'128px','height':'128px'})],className='panel'),False,False,False

@callback(Output('pred-upload','contents'),Output('pred-upload','filename'),Output('pred-example-info','children'),Input('pred-example','value'),prevent_initial_call=True)
def choose_example(case):
 root=Path(__file__).resolve().parents[1]
 rows=json.loads((root/'data/ejemplos.json').read_text())
 r=next((x for x in rows if x['caso']==case),None)
 if r is None:return dash.no_update,dash.no_update,dash.no_update
 data='data:image/png;base64,'+(root/r['png_file']).read_text().strip()
 return data,r['archivo_ejemplo'],html.P(r['explicacion']+' Marca la confirmación para habilitar el análisis.',className='note')
