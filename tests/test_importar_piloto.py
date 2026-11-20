import hashlib,json,zipfile
import pytest
from tools.importar_piloto import ROOT,SEEDS,receive

def fixture_zip(path,damage=None):
 cfg=json.loads((ROOT/'experiments/piloto_v1.json').read_text())
 pred=[dict(archivo=f'validation/test_{i}.png',paciente=f'p{i%21}',clase=cfg['classes'][i%3],probabilidades=[float(j==i%3) for j in range(3)]) for i in range(2049)]
 pb=json.dumps(pred).encode();weights=b'synthetic bytes for receiver test only'
 with zipfile.ZipFile(path,'w') as z:
  for n in ['training/pilot.py','src/original_model.py','experiments/piloto_v1.json']:z.writestr('codigo/'+n,(ROOT/n).read_bytes())
  for seed in SEEDS:
   prefix=f'resultados/{seed}/'
   result=dict(semilla=seed,scope=cfg['scope'],best_epoch=1,val_macro_f1=1.,identity='test',checkpoint_sha256=hashlib.sha256(weights).hexdigest(),predictions_sha256=hashlib.sha256(pb).hexdigest())
   if damage=='metric' and seed==6105:result['val_macro_f1']=.2
   z.writestr(prefix+'resultado.json',json.dumps(result));z.writestr(prefix+'historia.json',json.dumps([dict(epoch=1,loss=.1,val_macro_f1=1.,seconds=1.)]))
   z.writestr(prefix+'predicciones.json',pb);z.writestr(prefix+'mejor.pt',b'changed' if damage=='hash' and seed==6105 else weights)

def test_accepts_coherent_archive(tmp_path):
 p=tmp_path/'test.zip';fixture_zip(p);assert len(receive(p))==5
@pytest.mark.parametrize('damage',['hash','metric'])
def test_rejects_inconsistent_evidence(tmp_path,damage):
 p=tmp_path/'test.zip';fixture_zip(p,damage)
 with pytest.raises(ValueError):receive(p)
