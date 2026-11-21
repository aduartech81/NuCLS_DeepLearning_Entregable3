from pathlib import Path
import json,zipfile,csv,io,hashlib
import numpy as np
from statistics import NormalDist
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--piloto',required=True);ap.add_argument('--bases',required=True);ap.add_argument('--hashes',required=True);a=ap.parse_args()
R=Path(__file__).resolve().parents[1];B=Path(a.bases);hashes=json.loads(Path(a.hashes).read_text());CL=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
def f1(y,p):
 c=np.bincount(y*3+p.argmax(1),minlength=9).reshape(3,3);d=c.sum(0)+c.sum(1);return float(np.divide(2*c.diagonal(),d,out=np.zeros(3),where=d!=0).mean())
def wilcoxon(d):
 d=d[d!=0];a=np.abs(d);r=np.array([1+(a<v).sum()+((a==v).sum()-1)/2 for v in a]);scaled=(2*r).astype(int);dist={0:1}
 for rank in scaled:
  nxt=dist.copy()
  for k,v in dist.items():nxt[k+rank]=nxt.get(k+rank,0)+v
  dist=nxt
 observed=int(scaled[d>0].sum());total=int(scaled.sum());p=sum(v for s,v in dist.items() if abs(s-total/2)>=abs(observed-total/2))/(2**len(d));return float(p)
results=[];source=[]
with zipfile.ZipFile(a.piloto) as z:
 for model in ['softmaxcnn_bn','densenet121','resnet50']:
  vals=[]
  for seed in range(6101,6106):
   name=f'final/{model}_{seed}/predicciones_validacion.csv';raw=(B/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==hashes[name];base=list(csv.DictReader(io.StringIO(raw.decode())));craw=z.read(f'resultados/{seed}/predicciones.json');cico=json.loads(craw);res=json.loads(z.read(f'resultados/{seed}/resultado.json'));assert hashlib.sha256(craw).hexdigest()==res['predictions_sha256'];bm={r['archivo']:r for r in base};assert len(bm)==2049 and set(bm)=={r['archivo'] for r in cico}
   for c in cico:assert bm[c['archivo']]['clase_real']==c['clase'] and bm[c['archivo']]['paciente']==c['paciente']
   y=np.array([CL.index(c['clase']) for c in cico]);bp=np.array([[float(bm[c['archivo']][k]) for k in ['p_tumor','p_linfocito','p_estroma']] for c in cico]);cp=np.array([c['probabilidades'] for c in cico]);vals.append([seed,f1(y,cp),f1(y,bp)]);source.append(dict(model=model,seed=seed,base_sha256=hashes[name],cico_sha256=hashlib.sha256(craw).hexdigest()))
  a=np.array(vals);d=a[:,1]-a[:,2];sd=float(d.std(ddof=1));results.append(dict(modelo=model,semillas=[6101,6102,6103,6104,6105],valores=vals,cico_media=float(a[:,1].mean()),base_media=float(a[:,2].mean()),diferencia_media=float(d.mean()),sd_diferencia=sd,dz=float(d.mean()/sd) if sd else None,p=wilcoxon(d),mde80_normal_aprox=float((NormalDist().inv_cdf(1-.05/6)+NormalDist().inv_cdf(.8))*sd/np.sqrt(5))))
order=sorted(range(3),key=lambda i:results[i]['p']);prev=0
for rank,i in enumerate(order):prev=max(prev,min(1,results[i]['p']*(3-rank)));results[i]['p_holm']=prev
out=dict(scope='Comparación exploratoria post hoc en validación compartida: 2.049 recortes, 21 pacientes, cinco semillas emparejadas. No test sellado ni comparación de presupuestos de ajuste equivalentes.',tests=results,sources=source,power='Con cinco diferencias no nulas, el menor p bilateral exacto de Wilcoxon es 2/32=0,0625: no puede alcanzar alfa 0,05, incluso antes de Holm. No se acredita potencia 0,80. MDE normal aproximada (Bonferroni 3, 80%) es orientativa para planificación, no potencia del test exacto ni garantía de tamaño muestral.',seed_uncertainty='El pareamiento mide variación entre entrenamientos sobre pacientes fijos; no sustituye incertidumbre por paciente ni demuestra generalización. Los presupuestos históricos de entrenamiento y selección difieren.')
(R/'data/diagnosticos/contrastes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(results,indent=2))
