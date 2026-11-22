import json,hashlib
from pathlib import Path
import numpy as np
from app import app
from dash import html,no_update
from pages.prediccion import cached_view
from pages.calidad_explicaciones import show
from tools.documentar_analisis_cpu import explanations,power
R=Path(__file__).resolve().parents[1]

def test_cache_reuses_only_matching_image_and_clears_on_change():
 calls=[]
 def compute(*args):calls.append(args);return html.P('resultado')
 view,cache=cached_view('pred-run','image-a',['yes'],None,compute,1)
 reused,update=cached_view('pred-run','image-a',['yes'],cache,compute,2)
 assert len(calls)==1 and update is no_update
 assert cached_view('pred-upload','image-b',['yes'],cache,compute,2)==(None,None)
 assert cached_view('pred-consent','image-a',[],cache,compute,2)==(None,None)
 cached_view('pred-run','image-b',['yes'],cache,compute,3)
 assert len(calls)==2

def test_quality_results_have_provenance_and_finite_curves():
 d=json.loads((R/'data/diagnosticos/explicaciones_cpu.json').read_text())
 assert d['modelo_sha256']==hashlib.sha256((R/'models/cico_6101.onnx').read_bytes()).hexdigest()
 images=json.loads((R/'data/ejemplos.json').read_text())
 assert len(d['casos'])==len(images)==6
 for r in d['casos']:
  assert r['imagen_sha256']==next(x['sha256'] for x in images if x['caso']==r['caso'])
  for k in ['eliminacion','insercion','eliminacion_aleatoria_media','insercion_aleatoria_media']:
   a=np.asarray(r[k]);assert a.shape==(9,) and np.isfinite(a).all() and ((a>=0)&(a<=1)).all()
  assert np.isclose(r['eliminacion'][0],r['insercion'][-1])
  assert np.isclose(r['eliminacion'][-1],r['insercion'][0])
  assert len(show(r['caso']))==3
 assert app.server.test_client().get('/calidad-explicaciones').status_code==200

def test_cpu_book_matches_shared_data():
 assert (R/'book/22_calidad_explicaciones.md').read_text()==explanations()
 assert (R/'book/23_planificacion_potencia.md').read_text()==power()
 d=json.loads((R/'data/diagnosticos/planificacion_potencia.json').read_text())
 for r in d['filas']:
  n=[x['n_con_piso_guia'] for x in r['escenarios']]
  assert all(a>=b for a,b in zip(n,n[1:])) and min(n)>=10

def test_dash_prediction_cache_roundtrip_and_invalidation():
 client=app.server.test_client();client.get('/_dash-dependencies')
 row=json.loads((R/'data/ejemplos.json').read_text())[0]
 contents='data:image/png;base64,'+(R/row['png_file']).read_text().strip()
 payload={'output':'..pred-result.children...pred-memory.data..','outputs':[{'id':'pred-result','property':'children'},{'id':'pred-memory','property':'data'}],'inputs':[{'id':'pred-run','property':'n_clicks','value':1},{'id':'pred-upload','property':'contents','value':contents},{'id':'pred-consent','property':'value','value':['yes']}],'state':[{'id':'pred-memory','property':'data','value':None}],'changedPropIds':['pred-run.n_clicks']}
 response=client.post('/_dash-update-component',json=payload)
 assert response.status_code==200
 data=response.get_json()['response'];assert 'Clase con mayor' in json.dumps(data)
 payload['state'][0]['value']=data['pred-memory']['data'];payload['inputs'][0]['value']=2
 second=client.post('/_dash-update-component',json=payload).get_json()['response']
 assert second['pred-result']==data['pred-result'] and 'pred-memory' not in second
 payload['changedPropIds']=['pred-consent.value'];payload['inputs'][2]['value']=[]
 third=client.post('/_dash-update-component',json=payload).get_json()['response']
 assert third['pred-result']['children'] is None and third['pred-memory']['data'] is None
