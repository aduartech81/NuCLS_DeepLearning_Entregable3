import json
import pytest
import numpy as np
from app import app
from pages.datos import filter_eda,classes
from src.inference import explain_occlusion,predict
from tests.test_inference import upload
from tools.cierre_cpu import stats,cluster_ci,validate

def test_perfect_predictions_and_cluster_intervals():
 y=np.array([0,1,2,0,1,2]);p=np.eye(3)[y];s=stats(y,p)
 assert s['macro_f1']==s['accuracy']==1 and s['brier']==s['ece_fijo10']==0
 ci=cluster_ci(y,p,np.array(['a']*3+['b']*3),reps=25)
 assert ci['macro_f1']==[1,1]

def test_filtered_counts_and_empty_selection():
 a,b,c,msg=filter_eda(classes.particion.unique().tolist(),classes.clase.unique().tolist())
 assert sum(sum(t.y) for t in a.data)==classes.incluidas.sum()
 for t in c.data:assert np.isclose(sum(t.y),100)
 assert filter_eda([],[])[3]=='0 recortes seleccionados'

def test_occlusion_constant_input_and_latency():
 with pytest.raises(ValueError,match='uniforme'):explain_occlusion(upload(np.zeros((128,128,3),dtype='uint8')))
 image=upload(np.random.default_rng(5).integers(0,256,(128,128,3),dtype='uint8'))
 result=explain_occlusion(image)
 assert np.asarray(result['effects']).shape==(8,8)
 assert np.isfinite(result['effects']).all()
 pred=predict(image)
 assert pred['latency_ms']>0 and 0<=pred['entropy']<=np.log(3)+1e-6

def test_new_route_and_callback_registration():
 client=app.server.test_client()
 assert client.get('/cierre').status_code==200
 deps=client.get('/_dash-dependencies').get_json()
 assert any('explain-result.children' in x['output'] and 'explain-memory.data' in x['output'] for x in deps)
 assert any('eda-counts.figure' in x['output'] for x in deps)
