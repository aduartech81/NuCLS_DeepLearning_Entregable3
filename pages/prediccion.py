import dash
from dash import html,dcc,Input,Output,State,callback
from src.inference import predict

dash.register_page(__name__,path='/prediccion',name='Predicción CICO')
layout=html.Div([
 html.Span('CICO / DEMOSTRACIÓN EXPLORATORIA',className='eyebrow'),html.H1('Explorar un recorte histológico'),
 html.P('Carga un recorte RGB de 128 × 128 píxeles, centrado en un núcleo y preparado como los recortes NuCLS. PNG o JPEG, máximo 2 MB. No se admiten láminas completas ni se redimensiona la imagen.',className='lead'),
 html.Div([html.Strong('Modelo piloto · semilla 6101'),html.P('Seleccionado por el mayor macro-F1 de validación entre cinco semillas. Clasifica entre tumor, linfocito y estroma. No detecta automáticamente imágenes fuera del dominio ni acredita utilidad clínica.')],className='notice'),
 dcc.Checklist(id='pred-consent',options=[{'label':'Confirmo que es un recorte histológico sin datos personales y entiendo que el resultado es experimental, no un diagnóstico.','value':'yes'}],value=[]),
 dcc.Upload(id='pred-upload',children=html.Div(['Arrastra el recorte o ',html.A('selecciona una imagen')]),accept='image/png,image/jpeg',multiple=False,max_size=2*1024*1024,style={'border':'2px dashed #137d73','padding':'32px','margin':'24px 0','borderRadius':'12px'}),
 html.Button('Analizar recorte',id='pred-run',n_clicks=0,className='button'),
 dcc.Loading(html.Div(id='pred-result',role='status',style={'marginTop':'24px'})),
 html.P('Al analizar, la imagen se envía al servidor de Render y se procesa en memoria. La aplicación no la escribe en archivos ni la incorpora al entrenamiento. Las probabilidades no están calibradas y no expresan certeza clínica.'),
 html.A('Leer validación de exportación',href='/libro/16_exportacion_inferencia.html',className='button secondary')])

@callback(Output('pred-result','children'),Input('pred-run','n_clicks'),State('pred-upload','contents'),State('pred-consent','value'),prevent_initial_call=True)
def analyze(n,contents,consent):
 if 'yes' not in (consent or []):return html.P('Marca la confirmación antes de analizar.')
 if not contents:return html.P('Selecciona primero una imagen PNG o JPEG.')
 try:r=predict(contents)
 except ValueError as e:return html.P(str(e))
 except Exception:return html.P('El modelo no está disponible o no superó su comprobación. No se generó una predicción.')
 return html.Div([html.Img(src=contents,alt='Recorte analizado',style={'width':'256px','imageRendering':'auto','maxWidth':'100%'}),html.H2('Clase con mayor puntuación: '+r['prediction']),html.Table([html.Thead(html.Tr([html.Th('Clase'),html.Th('Probabilidad del modelo')])) ,html.Tbody([html.Tr([html.Td(label),html.Td(f'{p:.1%}')]) for label,p in zip(r['labels'],r['probabilities'])])]),html.P('Semilla 6101 · tres clases posibles. El modelo siempre asigna una de ellas, incluso si el contenido no corresponde; no usar para decisiones clínicas.')],className='panel')
