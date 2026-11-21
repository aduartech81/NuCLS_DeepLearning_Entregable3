import base64,hashlib,json
import numpy as np
import pytest
from app import app
from src.inference import decode_upload,predict,ROOT
from tests.test_inference import upload
from pages.diagnosticos import figures,D
from pages.eda_e3 import show,G

def test_rgba_opaque_preserves_pixels_and_rejects_partial():
 rgb=np.random.default_rng(7).integers(0,256,(128,128,3),dtype=np.uint8)
 rgba=np.concatenate([rgb,np.full((128,128,1),255,dtype=np.uint8)],axis=2)
 np.testing.assert_array_equal(decode_upload(upload(rgb)),decode_upload(upload(rgba,'RGBA')))
 rgba[0,0,3]=254
 with pytest.raises(ValueError,match='alfa'):decode_upload(upload(rgba,'RGBA'))

def test_uniform_input_is_rejected_before_model_inference():
 with pytest.raises(ValueError,match='uniforme'):predict(upload(np.zeros((128,128,3),dtype=np.uint8)))

def test_new_diagnostics_and_empty_filters():
 for seed in D:
  fs=figures(seed);assert len(fs)==5 and sum(map(sum,D[seed]['cm']))==2049
  for c in D[seed]['curves']:
   assert 0<=c['auc']<=1 and 0<=c['ap']<=1
 assert sum(r['n'] for r in G)==16588
 fs=show([],[]);assert len(fs[0].data)==0 and '0 recortes' in fs[-1]

def test_example_download_matches_manifest():
 c=app.server.test_client()
 for r in json.loads((ROOT/'data/ejemplos.json').read_text()):
  response=c.get('/ejemplo-png/'+r['caso']);assert response.status_code==200
  assert hashlib.sha256(response.data).hexdigest()==r['sha256'];decode_upload('data:image/png;base64,'+base64.b64encode(response.data).decode())
 assert c.get('/ejemplo-png/no-existe').status_code==404
 assert c.get('/model-card').status_code==200
