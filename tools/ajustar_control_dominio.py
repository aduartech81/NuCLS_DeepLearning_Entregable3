"""Fit on train; threshold on 10 validation patients; evaluate remaining 11 and fixed synthetic stressors."""
from pathlib import Path
import sys,zipfile,csv,io,json,hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.domain_guard import features,assess
R=Path(__file__).resolve().parents[1]
zpath=Path(sys.argv[1]);records=[];vectors=[]
with zipfile.ZipFile(zpath) as z:
 manifest=z.read('manifiesto.csv');assert hashlib.sha256(manifest).hexdigest()=='623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4'
 for row in csv.DictReader(io.StringIO(manifest.decode())):
  if row['estado']!='incluida' or row['particion'] not in ('train','validation'):continue
  raw=z.read(row['archivo']);assert hashlib.sha256(raw).hexdigest()==row['sha_archivo']
  a=np.asarray(Image.open(io.BytesIO(raw)).convert('RGB'),dtype=float)/255
  records.append(row);vectors.append(features(a))
X=np.array(vectors);train=np.array([r['particion']=='train' for r in records]);patients=sorted({r['paciente'] for r in records if r['particion']=='validation'});calpatients=patients[:10]
cal=np.array([r['particion']=='validation' and r['paciente'] in calpatients for r in records]);hold=~(train|cal)
mean=X[train].mean(0);scale=np.maximum(X[train].std(0),1e-6);Z=(X-mean)/scale;cov=np.cov(Z[train],rowvar=False);precision=np.linalg.inv(.9*cov+.1*np.eye(X.shape[1]));scores=np.sqrt(np.maximum(0,np.einsum('ij,jk,ik->i',Z,precision,Z)));threshold=float(np.quantile(scores[cal],.95,method='higher'))
m=dict(version='appearance-v1',mean=mean.tolist(),scale=scale.tolist(),precision=precision.tolist(),threshold=threshold,calibration_patients=calpatients,threshold_rule='Percentil 95 superior de distancia en los primeros 10 pacientes de validación ordenados; fijado antes de evaluar los otros 11 y los sintéticos.',manifest_sha256=hashlib.sha256(manifest).hexdigest())
(R/'models/domain_guard.json').write_text(json.dumps(m,indent=2))
summary=[]
for name,mask in [('ajuste_train',train),('umbral_validacion',cal),('comprobacion_validacion',hold)]:
 for cl in ['TODAS']+sorted({r['clase'] for r in records}):
  subset=mask & np.array([cl=='TODAS' or r['clase']==cl for r in records]);summary.append(dict(grupo=name,clase=cl,n=int(subset.sum()),aceptadas=int((scores[subset]<=threshold).sum()),fraccion_aceptada=float((scores[subset]<=threshold).mean())))
rng=np.random.default_rng(20261122);g=np.tile(np.linspace(0,1,128),(128,1));samples={'ruido_rgb':rng.random((128,128,3)),'gradiente_ruido':np.clip(np.repeat(g[:,:,None],3,axis=2)+rng.normal(0,.05,(128,128,3)),0,1),'tablero_gris':np.repeat(((np.indices((128,128)).sum(0)//8)%2)[:,:,None],3,axis=2),'gradiente_colores':np.stack([g,g.T,1-g],2),'ruido_rosado':np.clip(np.array([.8,.5,.75])+rng.normal(0,.1,(128,128,3)),0,1)}
stress=[dict(nombre=k,**assess(v,m)) for k,v in samples.items()]
report=dict(scope='Diagnóstico post hoc de apariencia. Pacientes de validación histórica: no prueba confirmatoria independiente, no OOD clínicamente validado.',threshold=threshold,patients_evaluacion=patients[10:],resultados=summary,sinteticos=stress,limitations='No hay fotografías naturales ni tejidos externos etiquetados en esta comprobación. Puede aceptar imágenes sintéticas con apariencia similar y rechazar histología válida. No es calibración de probabilidades ni cobertura garantizada.',model_sha256=hashlib.sha256((R/'models/domain_guard.json').read_bytes()).hexdigest())
(R/'data/diagnosticos/control_dominio.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
