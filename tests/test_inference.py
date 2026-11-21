import base64,io,json,zipfile
from pathlib import Path
import numpy as np
import pytest
from PIL import Image
from src.inference import decode_upload,predict,engine,ROOT

def upload(a,mode='RGB',fmt='PNG'):
 b=io.BytesIO();Image.fromarray(a,mode=mode).save(b,format=fmt)
 return 'data:image/'+('png' if fmt=='PNG' else 'jpeg')+';base64,'+base64.b64encode(b.getvalue()).decode()

def test_real_checkpoint_input_matches_onnx():
 golden=np.load(ROOT/'models/verification.npz');_,meta=engine()
 x=golden['image'][0].transpose(1,2,0)
 pixels=np.clip(np.rint((x*np.asarray(meta['std'])+np.asarray(meta['mean']))*255),0,255).astype('uint8')
 r=predict(upload(pixels));logits=golden['logits'][0];p=np.exp(logits-logits.max());p/=p.sum()
 np.testing.assert_allclose(r['probabilities'],p,atol=1e-5,rtol=0)
 assert abs(sum(r['probabilities'])-1)<1e-6

@pytest.mark.parametrize('contents',[
 'data:image/png;base64,!!!',
 'data:text/plain;base64,YWJj',
 upload(np.zeros((256,128,3),dtype='uint8')),
 upload(np.zeros((128,128,4),dtype='uint8'),mode='RGBA'),
 'data:image/png;base64,'+'A'*(3*1024*1024),
])
def test_rejects_invalid_upload(contents):
 with pytest.raises(ValueError):decode_upload(contents)

def test_unverified_model_rejected(tmp_path,monkeypatch):
 import src.inference as inf
 folder=tmp_path/'models';folder.mkdir();(folder/'cico_6101.json').write_text(json.dumps({'verified':False}));engine.cache_clear();monkeypatch.setattr(inf,'ROOT',tmp_path)
 with pytest.raises(RuntimeError):engine()
 engine.cache_clear()
