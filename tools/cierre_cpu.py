"""Read-only audit of received evidence; outputs go to a new directory. No checkpoints executed."""
from pathlib import Path
import argparse,csv,hashlib,json,zipfile
import numpy as np
import pandas as pd
CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def f1(y,p):
 cm=np.bincount(y*3+np.argmax(p,axis=1),minlength=9).reshape(3,3);den=cm.sum(0)+cm.sum(1)
 return float(np.divide(2*np.diag(cm),den,out=np.zeros(3),where=den!=0).mean())
def validate(y,p):
 assert len(y)==len(p) and p.shape[1]==3 and np.isfinite(p).all() and (p>=0).all() and (p<=1).all()
 assert np.allclose(p.sum(1),1,atol=1e-5) and np.isin(y,[0,1,2]).all()
def stats(y,p):
 pred=p.argmax(1);conf=p.max(1);correct=pred==y;bins=np.minimum((conf*10).astype(int),9)
 ece=sum(abs(np.mean(correct[bins==i])-np.mean(conf[bins==i]))*np.mean(bins==i) for i in range(10) if (bins==i).any())
 return {'macro_f1':f1(y,p),'accuracy':float(correct.mean()),'brier':float(((p-np.eye(3)[y])**2).sum(1).mean()),'log_loss':float(-np.log(np.clip(p[np.arange(len(y)),y],1e-12,1)).mean()),'ece_fijo10':float(ece)}
def cluster_ci(y,p,groups,reps=2000):
 unique=np.unique(groups);ids=[np.flatnonzero(groups==g) for g in unique];rng=np.random.default_rng(20261121);values=[]
 for _ in range(reps):
  ix=np.concatenate([ids[i] for i in rng.integers(0,len(ids),len(ids))]);values.append(list(stats(y[ix],p[ix]).values()))
 q=np.quantile(values,[.025,.975],axis=0)
 return {k:[float(q[0,i]),float(q[1,i])] for i,k in enumerate(stats(y,p))}
def audit66(root,out):
 idx=pd.read_csv(root/'indice_validacion.csv');assert len(idx)==66
 rows=[];hashes={};signature=None
 for r in idx.to_dict('records'):
  folder=root/'final'/f"{r['modelo']}_{r['semilla']}";res=json.loads((folder/'resultado.json').read_text());hist=json.loads((folder/'historia.json').read_text());curves=pd.read_csv(folder/'curvas.csv');df=pd.read_csv(folder/'predicciones_validacion.csv');pat=pd.read_csv(folder/'metricas_por_paciente.csv')
  assert sha(folder/'resultado.json')==r['resultado_sha256'];assert res['modelo']==r['modelo'] and res['semilla']==r['semilla']
  sig=list(zip(df.archivo,df.paciente,df.clase_real))
  if signature is None:signature=sig
  assert signature==sig and len(df)==2049 and df.archivo.nunique()==2049 and df.paciente.nunique()==21
  y=df.clase_real.map(dict(zip(CLASSES,range(3)))).to_numpy();p=df[['p_tumor','p_linfocito','p_estroma']].to_numpy();validate(y,p)
  assert np.array_equal(df.clase_predicha.to_numpy(),np.array(CLASSES)[p.argmax(1)])
  val=f1(y,p);assert abs(val-res['validacion']['macro_f1'])<1e-8 and abs(val-r['macro_f1_validacion'])<1e-8
  assert len(hist)==res['epocas_ejecutadas']==len(curves)
  assert [x['epoca'] for x in hist]==list(range(1,len(hist)+1))
  for k in curves.columns:assert np.allclose(curves[k],np.array([x[k] for x in hist]),rtol=1e-10,atol=1e-10)
  best=max(hist,key=lambda x:x['val_macro_f1']);assert best['epoca']==res['mejor_epoca'] and abs(best['val_macro_f1']-val)<1e-8
  for pr in pat.to_dict('records'):
   ix=np.flatnonzero(df.paciente.to_numpy()==pr['paciente']);assert len(ix)==pr['n'] and abs(f1(y[ix],p[ix])-pr['macro_f1_tres_clases'])<1e-8
  assert len(pat)==21
  for q in folder.iterdir():
   if q.is_file():hashes[str(q.relative_to(root))]=sha(q)
  rows.append({'modelo':r['modelo'],'semilla':r['semilla'],'macro_f1':val,'epocas':len(hist),'mejor_epoca':res['mejor_epoca'],'predicciones':len(df),'pacientes':21,'estado':'VERIFICADA'})
 assert len({(r['modelo'],r['semilla']) for r in rows})==66
 pd.DataFrame(rows).to_csv(out/'auditoria_66.csv',index=False)
 (out/'hashes_66.json').write_text(json.dumps(hashes,indent=2))
 return {'corridas':66,'modelos':3,'semillas_por_modelo':22,'archivos':len(hashes),'predicciones_por_corrida':2049,'pacientes':21,'comprobado':['hash resultado contra índice','probabilidades y etiquetas','F1 recalculado','historias y curvas idénticas','mejor época','métricas por paciente'],'limite':'Auditoría de archivos recibidos; no ejecución independiente ni verificación de pesos, que no se incluyen en esta carpeta.'}
def audit65(root,out):
 rows=[];validation=[];files=0;signature=None
 for folder in sorted((root/'corridas').iterdir()):
  if not folder.is_dir():continue
  meta=json.loads((folder/'completo.json').read_text())
  for name,h in meta['archivos'].items():assert sha(folder/name)==h;files+=1
  vm=json.loads((folder/'validation.json').read_text());assert sha(folder/'validation.npz')==vm['predicciones_sha256'];files+=1
  with np.load(folder/'validation.npz',allow_pickle=False) as d:validate(d['y'],d['p']);validation.append({'modelo':folder.name.rsplit('_',1)[0],'f1':f1(d['y'],d['p'])})
  df=pd.read_csv(folder/'predicciones_reserva.csv');sig=list(zip(df.archivo,df.paciente,df.clase_real))
  if signature is None:signature=sig
  assert sig==signature
  with np.load(folder/'reserva.npz',allow_pickle=False) as d:
   y=d['y'];p=d['p'];validate(y,p);assert np.array_equal(y,df.clase_real.map(dict(zip(CLASSES,range(3)))).to_numpy());assert np.allclose(p,df[['p_tumor','p_linfocito','p_estroma']],atol=1e-12)
   rows.append({'modelo':folder.name.rsplit('_',1)[0],'semilla':int(folder.name.rsplit('_',1)[1]),**stats(y,p)})
 assert len(rows)==65
 pd.DataFrame(rows).to_csv(out/'metricas_65_recalculadas.csv',index=False)
 top=pd.DataFrame(validation).groupby('modelo').f1.mean().sort_values(ascending=False).head(3).index.tolist()
 errors=[];diagnostics=[];error_sets={}
 for model in top:
  folders=[root/'corridas'/f'{model}_{seed}' for seed in range(6101,6106)];ps=[]
  for folder in folders:
   with np.load(folder/'reserva.npz',allow_pickle=False) as d:ps.append(d['p'].copy());y=d['y'].copy()
  p=np.mean(ps,axis=0);df=pd.read_csv(folders[0]/'predicciones_reserva.csv');groups=df.paciente.to_numpy();err=np.flatnonzero(p.argmax(1)!=y)
  error_sets[model]=set(df.iloc[err].archivo)
  selected=np.random.default_rng(20261121).choice(err,min(100,len(err)),replace=False)
  for ix in selected:
   errors.append({'modelo':model,'archivo':df.iloc[ix].archivo,'paciente':df.iloc[ix].paciente,'clase_real':CLASSES[y[ix]],'clase_predicha':CLASSES[p[ix].argmax()],'probabilidad_maxima':float(p[ix].max()),'categoria_revision':'','revisor':'','justificacion':'','etiqueta_disputada':''})
  diagnostics.append({'modelo':model,'unidad':'ensamble de cinco semillas; selección por media de validación','n':len(y),'pacientes':len(set(groups)),'errores':len(err),'errores_muestreados':len(selected),'metricas':stats(y,p),'IC95_bootstrap_paciente_2000':cluster_ci(y,p,groups),'limites':'Reserva histórica expuesta, solo seis pacientes. Intervalos descriptivos, condicionados al ensamble; sin calibración ajustada ni garantía de cobertura.'})
 pd.DataFrame(errors).to_csv(out/'REVISION_HUMANA_300_ERRORES.csv',index=False)
 overlap=[{'modelo_a':a,'modelo_b':b,'errores_comunes':len(error_sets[a]&error_sets[b]),'union':len(error_sets[a]|error_sets[b])} for i,a in enumerate(top) for b in top[i+1:]]
 return {'corridas':65,'huellas_verificadas':files,'top3_por_validacion':top,'diagnosticos_ensambles':diagnostics,'errores_compartidos':overlap,'revision_humana':'Preparada, NO adjudicada. No equivale a cerrar 100 errores por modelo.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bases',type=Path,required=True);ap.add_argument('--reserva',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 report={'alcance':'Auditoría CPU de predicciones recibidas. Ningún entrenamiento ni modificación de fuentes.'}
 report['bases66']=audit66(a.bases,a.out);print('66 verificadas',flush=True)
 report['reserva65']=audit65(a.reserva,a.out);print('65 verificadas y diagnóstico calculado',flush=True)
 (a.out/'cierre_cpu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False));print(a.out,flush=True)
if __name__=='__main__':main()
