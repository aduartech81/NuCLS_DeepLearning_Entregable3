from pathlib import Path
import json,zipfile,hashlib,csv,io,collections,base64
import numpy as np
from PIL import Image
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--piloto',required=True);ap.add_argument('--datos',required=True);a=ap.parse_args()
R=Path(__file__).resolve().parents[1]; out=R/'data/diagnosticos';out.mkdir(exist_ok=True)
classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']; names=['tumor','linfocito','estroma'];diag={}
with zipfile.ZipFile(a.piloto) as z:
 for seed in range(6101,6106):
  raw=z.read(f'resultados/{seed}/predicciones.json');res=json.loads(z.read(f'resultados/{seed}/resultado.json'));assert hashlib.sha256(raw).hexdigest()==res['predictions_sha256']
  rows=json.loads(raw); y=np.array([classes.index(r['clase']) for r in rows]);p=np.array([r['probabilidades'] for r in rows]);assert len(y)==2049 and np.allclose(p.sum(1),1,atol=1e-6)
  pred=p.argmax(1);cm=np.zeros((3,3),int);np.add.at(cm,(y,pred),1);f1=2*cm.diagonal()/(cm.sum(0)+cm.sum(1));assert abs(f1.mean()-res['val_macro_f1'])<1e-6
  conf=p.max(1);acc=pred==y;bins=[]
  for i in range(10):
   m=(conf>=i/10)&((conf<(i+1)/10) if i<9 else conf<=1)
   if m.any():bins.append(dict(n=int(m.sum()),confidence=float(conf[m].mean()),accuracy=float(acc[m].mean()),left=i/10,right=(i+1)/10))
  curves=[]
  for k in range(3):
   order=np.argsort(-p[:,k],kind='stable');yy=(y[order]==k);scores=p[order,k];ends=np.r_[np.flatnonzero(np.diff(scores)),len(y)-1];tp=np.cumsum(yy)[ends];fp=np.cumsum(~yy)[ends];tpr=np.r_[0,tp/yy.sum()];fpr=np.r_[0,fp/(~yy).sum()];rec=np.r_[0,tp/yy.sum()];prec=np.r_[1,tp/(tp+fp)];auc=float(np.trapezoid(tpr,fpr));ap=float(np.sum(np.diff(rec)*prec[1:]));idx=np.unique(np.r_[0,np.linspace(0,len(rec)-1,min(220,len(rec))).astype(int),len(rec)-1]);curves.append(dict(clase=names[k],roc_x=fpr[idx].tolist(),roc_y=tpr[idx].tolist(),recall=rec[idx].tolist(),precision=prec[idx].tolist(),auc=auc,ap=ap,prevalencia=float((y==k).mean())))
  diag[str(seed)]=dict(n=len(y),patients=len(set(r['paciente'] for r in rows)),cm=cm.tolist(),f1=f1.tolist(),macro_f1=float(f1.mean()),accuracy=float(acc.mean()),brier=float(np.mean(np.sum((p-np.eye(3)[y])**2,axis=1))),ece=float(sum(b['n']*abs(b['confidence']-b['accuracy']) for b in bins)/len(y)),bins=bins,curves=curves,predictions_sha256=hashlib.sha256(raw).hexdigest())
(out/'cico.json').write_text(json.dumps(diag))
# Current E3 manifest: filters apply to all newly derived graphs. No sources altered.
with zipfile.ZipFile(a.datos) as z:
 raw=z.read('manifiesto.csv');rows=[r for r in csv.DictReader(io.StringIO(raw.decode())) if r['particion'] in ('train','validation')];counts=collections.Counter(r['sha_pixeles'] for r in rows);grouped=collections.defaultdict(list)
 for r in rows: grouped[(r['particion'],r['clase'])].append(r)
 groups=[]
 for (split,cl),rs in grouped.items():
  hist=np.zeros((3,16),int)
  for r in rs:
   rawim=z.read(r['archivo']);assert hashlib.sha256(rawim).hexdigest()==r['sha_archivo'];a=np.array(Image.open(io.BytesIO(rawim)));assert a.shape==(128,128,3)
   for k in range(3):hist[k]+=np.histogram(a[:,:,k],bins=np.linspace(0,256,17))[0]
  groups.append(dict(split=split,clase=cl,n=len(rs),patients=len(set(r['paciente'] for r in rs)),duplicated_records=sum(counts[r['sha_pixeles']]>1 for r in rs),hist=hist.tolist()))
 sha_classes=collections.defaultdict(set);sha_splits=collections.defaultdict(set)
 for r in rows:sha_classes[r['sha_pixeles']].add(r['clase']);sha_splits[r['sha_pixeles']].add(r['particion'])
 (out/'eda.json').write_text(json.dumps(dict(groups=groups,manifest_sha256=hashlib.sha256(raw).hexdigest(),duplicate_groups=sum(v>1 for v in counts.values()),conflicting_label_groups=sum(len(v)>1 for v in sha_classes.values()),cross_split_pixel_groups=sum(len(v)>1 for v in sha_splits.values()),scope='Igualdad exacta de píxeles; no descarta duplicados aproximados ni ruido semántico de etiqueta.')))
print('Diagnósticos de 5 semillas y EDA de',len(rows),'imágenes verificados')
