from pathlib import Path
import json,itertools,hashlib
import numpy as np
from scipy import stats
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'data/diagnosticos/contrastes.json').read_text());results=[]
for r in C['tests']:
 a=np.array(r['valores']);d=a[:,1]-a[:,2];signs=np.array(list(itertools.product([-1,1],repeat=len(d))));ranks=stats.rankdata(abs(d));obs=abs(np.sum(np.sign(d)*ranks));pw=float(np.mean(abs(signs@ranks)>=obs-1e-12));pp=float(np.mean(abs(signs@d)>=abs(d.sum())-1e-12));tt=stats.ttest_1samp(d,0);sw=stats.shapiro(d);half=stats.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d))
 results.append(dict(modelo=r['modelo'],n=len(d),delta=float(d.mean()),dz=r['dz'],ci95_semillas=[float(d.mean()-half),float(d.mean()+half)],p_t=float(tt.pvalue),p_wilcoxon=pw,p_permutacion=pp,p_conjunta=max(float(tt.pvalue),pw,pp),shapiro_p=float(sw.pvalue),todas_diferencias_negativas=bool((d<0).all())))
for key in ['p_t','p_wilcoxon','p_permutacion','p_conjunta']:
 prev=0
 for rank,i in enumerate(sorted(range(len(results)),key=lambda i:results[i][key])):
  prev=max(prev,min(1,results[i][key]*(len(results)-rank)));results[i][key+'_holm']=prev
runs=json.loads((R/'data/piloto_estado.json').read_text())['runs'];epochs=[]
for r in runs:
 h=r['history'];best=max(h,key=lambda e:e['val_macro_f1'])
 assert best['epoch']==r['best_epoch']
 epochs.append(dict(seed=r['seed'],best_epoch=r['best_epoch'],epochs=len(h),loss_inicial=h[0]['loss'],loss_final=h[-1]['loss'],f1_inicial=h[0]['val_macro_f1'],f1_final=h[-1]['val_macro_f1'],max_f1=best['val_macro_f1'],history=h))
eda=json.loads((R/'data/diagnosticos/eda.json').read_text());erows=[]
for r in eda['groups']:
 total=sum(x['n'] for x in eda['groups'] if x['split']==r['split']);hist=np.array(r['hist']);means=(hist@np.arange(8,256,16))/hist.sum(1)
 erows.append(dict(split=r['split'],clase=r['clase'],n=r['n'],porcentaje=100*r['n']/total,rgb_aproximado=means.tolist()))
out=dict(scope='Análisis post hoc; mismas predicciones y mismos 21 pacientes de validación. No aporta nuevas réplicas ni partición independiente.',contrastes=results,epochs=epochs,eda=erows,assumptions='t pareada: diferencias independientes entre entrenamientos y aproximadamente normales. Wilcoxon: diferencias simétricas. Permutación de signos: intercambiabilidad de signos bajo H0. Shapiro con n=5 tiene poca potencia y no demuestra normalidad; independencia entre pacientes no se obtiene repitiendo semillas. Ninguna prueba convierte validación usada para seleccionar modelos en test final.',source_sha256={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['data/diagnosticos/contrastes.json','data/piloto_estado.json','data/diagnosticos/eda.json']})
(R/'data/diagnosticos/cierre_revision.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(results,indent=2));print(json.dumps(erows,indent=2))
