import base64,json
import numpy as np
import pytest
from app import app
from src.domain_guard import enforce,assess,features
from src.inference import ROOT,decode_upload
from tests.test_inference import upload
from pages.prediccion import analyze,explain,upload_status
import dash_bootstrap_components as dbc

def test_noise_gradient_blocked_before_classification():
 rng=np.random.default_rng(20261122);g=np.tile(np.linspace(0,1,128),(128,1));a=np.clip(np.repeat(g[:,:,None],3,2)+rng.normal(0,.05,(128,128,3)),0,1)
 data=upload((a*255).astype('uint8'))
 assert not assess(decode_upload(data))['accepted']
 assert upload_status(data,'noise.png',['yes'])[1:]==(True,True,False)
 assert isinstance(analyze(1,data,['yes']),dbc.Alert)
 assert isinstance(explain(1,data,['yes']),dbc.Alert)

def test_public_examples_still_usable():
 for r in json.loads((ROOT/'data/ejemplos.json').read_text()):
  a=decode_upload('data:image/png;base64,'+(ROOT/r['png_file']).read_text().strip());assert enforce(a)['accepted']

def test_feature_definition_and_threshold_boundary():
 a=np.random.default_rng(8).random((128,128,3));f=features(a);assert len(f)==36
 m={'mean':f.tolist(),'scale':[1]*36,'precision':np.eye(36).tolist(),'threshold':0}
 assert assess(a,m)['accepted']
 assert not assess(a,dict(m,mean=(f+1).tolist()))['accepted']
