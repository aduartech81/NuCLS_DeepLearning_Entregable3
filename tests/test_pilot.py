import csv,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
import pytest
import torch
torch.set_num_threads(2)
from training import pilot

def dataset(tmp_path):
 root=tmp_path/'data';root.mkdir();rows=[]
 cfg=json.loads((Path(__file__).parents[1]/'experiments/piloto_v1.json').read_text())
 for s in ['train','validation']:
  for c,name in enumerate(cfg['classes']):
   a=np.zeros((128,128,3),dtype=np.uint8);a[:,:,c]=150+(s=='validation')
   file=f'{s}_{c}.png';Image.fromarray(a).save(root/file)
   rows.append(dict(particion=s,estado='incluida',paciente=s,tss=s,sha_pixeles=hashlib.sha256(a.tobytes()).hexdigest(),clase=name,archivo=file))
 with (root/'manifiesto.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 cfg.update(manifest_sha256=pilot.sha(root/'manifiesto.csv'),counts={'train':3,'validation':3},patients={'train':1,'validation':1},epochs=2,min_epochs=2,batch=3,seeds=[6101],model_config={'width':2,'classes':3})
 conf=tmp_path/'cfg.json';conf.write_text(json.dumps(cfg));return root,conf

def test_audit_and_integrity(tmp_path):
 root,c=dataset(tmp_path);cfg=json.loads(c.read_text());assert len(pilot.audit(root,cfg)['train'])==3
 (root/'train_0.png').write_bytes(b'broken')
 with pytest.raises(Exception):pilot.audit(root,cfg)

def test_resume_matches_and_complete_skips(tmp_path,monkeypatch):
 root,c=dataset(tmp_path);full=tmp_path/'full';res=tmp_path/'resume'
 pilot.run(root,full,c,device='cpu')
 original=pilot.atomic
 def interrupt_after_checkpoint(path,obj):
  original(path,obj)
  if path.name=='ultimo.pt' and obj['epoch']==1:raise RuntimeError('synthetic interruption')
 monkeypatch.setattr(pilot,'atomic',interrupt_after_checkpoint)
 with pytest.raises(RuntimeError):pilot.run(root,res,c,device='cpu')
 monkeypatch.setattr(pilot,'atomic',original);pilot.run(root,res,c,device='cpu')
 a=torch.load(full/'6101/mejor.pt',weights_only=True);b=torch.load(res/'6101/mejor.pt',weights_only=True)
 for k in a['model']:torch.testing.assert_close(a['model'][k],b['model'][k],rtol=0,atol=0)
 stamp=(res/'6101/mejor.pt').stat().st_mtime_ns
 pilot.run(root,res,c,device='cpu');assert (res/'6101/mejor.pt').stat().st_mtime_ns==stamp
 (res/'6101/predicciones.json').write_text('[]')
 with pytest.raises(ValueError):pilot.run(root,res,c,device='cpu')

def test_existing_lock_preserved(tmp_path):
 root,c=dataset(tmp_path);out=tmp_path/'out';out.mkdir();lock=out/'EJECUCION_ACTIVA.json';lock.write_text('{}')
 with pytest.raises(FileExistsError):pilot.run(root,out,c,device='cpu')
 assert lock.read_text()=='{}'
