from pathlib import Path
import json
import hashlib
import dash_bootstrap_components as dbc
import dash
from dash import html,dcc,Input,Output,State,callback
from src.inference import predict,explain_occlusion,decode_upload,check_basic_input
from src.domain_guard import enforce
import plotly.graph_objects as go

dash.register_page(__name__,path='/prediccion',name='Predicción CICO')
layout=html.Div([
 dcc.Store(id="pred-memory",storage_type="memory"),
 dcc.Store(id="explain-memory",storage_type="memory"),
 html.Div([html.Span('1 · Elige una imagen'),html.Span('2 · Analiza'),html.Span('3 · Interpreta con cautela')],className='prediction-steps'),
 html.Span('CICO / DEMOSTRACIÓN EXPLORATORIA',className='eyebrow'),html.H1('Explorar un recorte histológico'),
 html.P('Carga un recorte RGB de 128 × 128 píxeles, centrado en un núcleo y preparado como los recortes NuCLS. PNG o JPEG, máximo 2 MB. También se admite RGBA completamente opaco. No se admiten láminas completas ni se redimensiona la imagen.',className='lead'),
 html.Div([html.Strong('Modelo piloto · semilla 6101'),html.P('Seleccionado por el mayor macro-F1 de validación entre cinco semillas. Clasifica entre tumor, linfocito y estroma. Incluye un filtro experimental de apariencia: bloquea algunas entradas atípicas, pero no acredita que una imagen sea histológica ni su utilidad clínica.')],className='notice'),
 html.Div([html.H2('¿Quieres empezar con un ejemplo?'),html.P('Selecciona un recorte real de 128 × 128. La referencia se revela junto al ejemplo; no es una prueba independiente del modelo.'),dcc.Dropdown(id='pred-example',options=[{'label':'Caso '+x['caso']+' · referencia: '+x['clase_referencia'],'value':x['caso']} for x in json.loads((Path(__file__).resolve().parents[1]/'data/ejemplos.json').read_text())],placeholder='Elegir un ejemplo histológico…',clearable=False),html.Div(id='pred-example-info')],className='panel'),
 dcc.Checklist(id='pred-consent',options=[{'label':'Confirmo que es un recorte histológico sin datos personales y entiendo que el resultado es experimental, no un diagnóstico.','value':'yes'}],value=[]),
 dcc.Upload(id='pred-upload',children=html.Div([html.Button('Seleccionar imagen PNG o JPG',type='button',className='button',id='pred-file-button'),html.P('También puedes arrastrarla aquí. Primero marca la confirmación de arriba.')]),accept='.png,.jpg,.jpeg,image/png,image/jpeg',disabled=True,multiple=False,max_size=2*1024*1024,style={'border':'2px dashed #137d73','padding':'32px','margin':'24px 0','borderRadius':'12px'}),
 html.Div(id='pred-upload-local',role='status',style={'whiteSpace':'pre-wrap'}),
 dcc.Loading(html.Div(id='pred-upload-status',role='status')),
 html.P('Para probar el formulario, usa los PNG originales del paquete de ejemplos. No subas capturas de pantalla, campos completos ni imágenes ampliadas. Si están en Drive o iCloud, descárgalos primero al computador.'),html.A('Descargar imágenes listas para subir (ZIP)',href='/ejemplos-prueba.zip',className='button secondary'),
 html.Button('Analizar recorte',id='pred-run',n_clicks=0,className='button',disabled=True),
 dcc.Loading(html.Div(id='pred-result',role='status',style={'marginTop':'24px'})),
 html.P('Al seleccionar una imagen, se envía al servidor de Render para comprobarla y se procesa en memoria. La aplicación no la escribe en archivos ni la incorpora al entrenamiento. Los resultados se conservan solo en memoria de esta pestaña; al cambiar de imagen o retirar la confirmación se limpian. Las probabilidades no están calibradas y no expresan certeza clínica.'),
 html.Section([html.H2('¿Qué zonas influyen en esta puntuación?'),html.P('Oculta 64 regiones con el color medio del recorte y mide el cambio en la probabilidad de la clase elegida. Una caída positiva indica sensibilidad a esa región; no identifica células ni demuestra causalidad.'),html.Button('Calcular sensibilidad local',id='explain-run',n_clicks=0,className='button secondary',disabled=True),dcc.Loading(html.Div(id='explain-result',role='status'))],className='panel'),
 html.A('Descargar ejemplos con clase de referencia',href='/ejemplos',className='button'),html.A('Ver diagnósticos y calibración observada',href='/diagnosticos',className='button secondary'),html.A('Leer validación de exportación',href='/libro/16_exportacion_inferencia.html',className='button secondary')])

def analyze(n,contents,consent):
 if 'yes' not in (consent or []):return dbc.Alert('Marca la confirmación antes de analizar.',color='warning')
 if not contents:return dbc.Alert('Selecciona primero una imagen PNG o JPEG.',color='warning')
 try:
  enforce(decode_upload(contents));r=predict(contents)
 except ValueError as e:return dbc.Alert(str(e),color='warning')
 except Exception:return dbc.Alert('El modelo no está disponible o no superó su comprobación. No se generó una predicción.',color='danger')
 return html.Div([html.Img(src=contents,alt='Recorte analizado',style={'width':'256px','imageRendering':'auto','maxWidth':'100%'}),html.Div('APARIENCIA COMPATIBLE CON EL FILTRO EXPERIMENTAL; DOMINIO NO CERTIFICADO. Una imagen ajena a histología que supere el filtro también puede recibir una puntuación alta.',className='notice'),html.H2('Clase con mayor puntuación: '+r['prediction']),dcc.Graph(figure=go.Figure(go.Bar(x=r['probabilities'],y=r['labels'],orientation='h',text=[f'{p:.1%}' for p in r['probabilities']],textposition='auto',marker_color='#147d79')).update_layout(template='plotly_white',height=260,xaxis=dict(range=[0,1],tickformat='.0%',title='Puntuación del modelo · no calibrada'),margin=dict(l=90,r=25,t=15,b=50)),config={'displayModeBar':False}),html.Table([html.Thead(html.Tr([html.Th('Clase'),html.Th('Probabilidad del modelo')])) ,html.Tbody([html.Tr([html.Td(label),html.Td(f'{p:.1%}')]) for label,p in zip(r['labels'],r['probabilities'])])]),html.P(f"Tiempo del cálculo original en servidor (se reutiliza si la imagen no cambia): {r['latency_ms']:.1f} ms (sin red). Entropía: {r['entropy']:.3f} nats; dispersión de puntuaciones, no cobertura ni certeza clínica."),html.P('Semilla 6101 · tres clases posibles. El modelo siempre asigna una de ellas, incluso si el contenido no corresponde; no usar para decisiones clínicas.')],className='panel')


def explain(n,contents,consent):
 if 'yes' not in (consent or []):return dbc.Alert('Marca la confirmación antes de analizar.',color='warning')
 if not contents:return dbc.Alert('Selecciona primero una imagen PNG o JPEG.',color='warning')
 try:
  enforce(decode_upload(contents))
  key=hashlib.sha256(contents.split(',',1)[1].strip().encode()).hexdigest()
  precomputed=json.loads((Path(__file__).resolve().parents[1]/'data/explicaciones_ejemplos.json').read_text())
  r=precomputed.get(key)
  if r is None:r=explain_occlusion(contents)
 except ValueError as e:return dbc.Alert(str(e),color='warning')
 except Exception:return dbc.Alert('No se pudo calcular la sensibilidad; no se muestra un mapa sustituto.',color='danger')
 fig=go.Figure(go.Heatmap(z=r['effects'],x=[8+16*i for i in range(8)],y=[8+16*i for i in range(8)],colorscale='RdBu_r',zmid=0,colorbar={'title':'Caída de prob.'},hovertemplate='x=%{x}, y=%{y}<br>Caída: %{z:.4f}<extra></extra>'))
 fig.update_layout(template='plotly_white',xaxis_title='Posición horizontal (px)',yaxis_title='Posición vertical (px)',yaxis={'autorange':'reversed','scaleanchor':'x'},margin={'t':20},height=420)
 return html.Div([html.H3('Sensibilidad de la puntuación: '+r['target']),dbc.Row([dbc.Col(html.Img(src=contents,alt='Recorte usado para sensibilidad local',style={'width':'100%','maxWidth':'400px'}),xs=12,md=6),dbc.Col(dcc.Graph(figure=fig),xs=12,md=6)]),html.P(f"64 regiones de 16 × 16 px · {r['seconds']:.2f} s de servidor. Rojo: al ocultar, baja la puntuación; azul: sube. Un mapa uniforme puede indicar poca sensibilidad a esta intervención."),html.P(r['scope'],className='note')])


@callback(Output('pred-upload-status','children'),Output('pred-run','disabled'),Output('explain-run','disabled'),Output('pred-upload','disabled'),Input('pred-upload','contents'),Input('pred-upload','filename'),Input('pred-consent','value'))
def upload_status(contents,filename,consent):
 if 'yes' not in (consent or []):return html.P('1. Marca la confirmación; después selecciona tu imagen.'),True,True,True
 if not contents:return html.P('2. Selecciona una imagen. Cuando esté cargada aparecerán aquí su nombre y vista previa.'),True,True,False
 try:
  pixels=decode_upload(contents);check_basic_input(pixels);enforce(pixels)
 except ValueError as e:return html.Div([html.Strong('La imagen no está lista para analizar. '),html.Span(str(e)),html.P('Elige otro recorte. No se cambia su tamaño automáticamente.')],className='notice'),True,True,False
 except Exception:return html.Div('No se pudo comprobar la imagen en el servidor. Vuelve a intentarlo; no se ha generado una predicción.',className='notice'),True,True,False
 return html.Div([html.Strong('Formato y apariencia aceptados: '+str(filename or 'recorte')),html.P('RGB · 128 × 128 píxeles. Ahora pulsa «Analizar recorte».'),html.Img(src=contents,alt='Vista previa del archivo cargado',style={'width':'128px','height':'128px'})],className='panel'),False,False,False

@callback(Output('pred-upload','contents'),Output('pred-upload','filename'),Output('pred-example-info','children'),Input('pred-example','value'),prevent_initial_call=True)
def choose_example(case):
 root=Path(__file__).resolve().parents[1]
 rows=json.loads((root/'data/ejemplos.json').read_text())
 r=next((x for x in rows if x['caso']==case),None)
 if r is None:return dash.no_update,dash.no_update,dash.no_update
 data='data:image/png;base64,'+(root/r['png_file']).read_text().strip()
 return data,r['archivo_ejemplo'],html.P(r['explicacion']+' Marca la confirmación para habilitar el análisis.',className='note')


def cached_view(action, contents, consent, cached, compute, n):
 # Browser memory only. Cache is display-only, never scientific evidence or model input.
 if action not in ('pred-run','explain-run') or 'yes' not in (consent or []) or not contents:
  return None,None
 model_sha=json.loads((Path(__file__).resolve().parents[1]/'models/cico_6101.json').read_text())['sha256']
 key=hashlib.sha256((model_sha+contents).encode()).hexdigest()
 if isinstance(cached,dict) and cached.get('key')==key and 'view' in cached:
  return cached['view'],dash.no_update
 view=compute(n,contents,consent)
 # Failures are not cached: a transient failure must be retryable.
 if isinstance(view,dbc.Alert):return view,None
 return view,{'key':key,'view':view}

@callback(Output('pred-result','children'),Output('pred-memory','data'),Input('pred-run','n_clicks'),Input('pred-upload','contents'),Input('pred-consent','value'),State('pred-memory','data'),prevent_initial_call=True)
def analyze_cached(n,contents,consent,cached):
 return cached_view(dash.ctx.triggered_id,contents,consent,cached,analyze,n)

@callback(Output('explain-result','children'),Output('explain-memory','data'),Input('explain-run','n_clicks'),Input('pred-upload','contents'),Input('pred-consent','value'),State('explain-memory','data'),prevent_initial_call=True)
def explain_cached(n,contents,consent,cached):
 return cached_view(dash.ctx.triggered_id,contents,consent,cached,explain,n)

layout.children.append(html.Div([html.H2('Alcance del filtro de apariencia'),html.P('En 1.097 recortes de 11 pacientes de validación histórica no usados para fijar el umbral, aceptó el 79,9 %. Rechazó tejido válido: 44,5 % de linfocitos, 19,7 % de estroma y 5,6 % de tumor. Rechazó cinco patrones sintéticos; no se ha probado con una colección externa representativa. Pasar el filtro no valida el diagnóstico.'),html.A('Ver método y resultados del filtro',href='/libro/28_cierre_revision.html#control-de-apariencia')],className='panel'))
