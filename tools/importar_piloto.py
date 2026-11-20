"""Receive RunPod results without executing checkpoints or training code."""
from pathlib import Path
import argparse, csv, hashlib, io, json, math, statistics, zipfile
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
SEEDS=[6101,6102,6103,6104,6105]
def require(ok,message):
 if not ok:raise ValueError(message)
def receive(archive):
 cfg=json.loads((ROOT/'experiments/piloto_v1.json').read_text())
 runs=[];identities=set();reference=None
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();require(len(names)==len(set(names)),'Nombres duplicados en ZIP')
  require('resultados/EJECUCION_ACTIVA.json' not in names,'ZIP contiene ejecución activa')
  for name in ['training/pilot.py','src/original_model.py','experiments/piloto_v1.json']:
   require(z.read('codigo/'+name)==(ROOT/name).read_bytes(),'Código o configuración distintos: '+name)
  for seed in SEEDS:
   prefix=f'resultados/{seed}/'
   result=json.loads(z.read(prefix+'resultado.json'));history=json.loads(z.read(prefix+'historia.json'))
   predbytes=z.read(prefix+'predicciones.json');pred=json.loads(predbytes)
   require(result['semilla']==seed,'Semilla incorrecta')
   require(result['scope']==cfg['scope'],'Alcance distinto')
   for filename,key in [('mejor.pt','checkpoint_sha256'),('predicciones.json','predictions_sha256')]:
    h=hashlib.sha256()
    with z.open(prefix+filename) as f:
     for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    require(h.hexdigest()==result[key],'Huella distinta: '+filename)
   require(0<len(history)<=cfg['epochs'],'Historia inválida')
   require([x['epoch'] for x in history]==list(range(1,len(history)+1)),'Épocas discontinuas')
   for row in history:
    require(all(math.isfinite(row[k]) for k in ['loss','val_macro_f1','seconds']),'Métrica no finita')
    require(0<=row['val_macro_f1']<=1 and row['seconds']>0,'Métrica fuera de rango')
   best=max(history,key=lambda x:x['val_macro_f1'])
   require(best['epoch']==result['best_epoch'],'Mejor época incoherente')
   require(abs(best['val_macro_f1']-result['val_macro_f1'])<1e-6,'F1 diferente a historia')
   require(len(pred)==cfg['counts']['validation'],'Conteo incorrecto de predicciones')
   ids=[p['archivo'] for p in pred];require(len(set(ids))==len(ids),'Predicciones duplicadas')
   require(all(x.startswith('validation/') for x in ids),'Predicción fuera de validación')
   signature=[(p['archivo'],p['paciente'],p['clase']) for p in pred]
   if reference is None:reference=signature
   else:require(signature==reference,'Muestras u orden distintos entre semillas')
   require(len({p['paciente'] for p in pred})==cfg['patients']['validation'],'Pacientes incorrectos')
   cm=[[0]*3 for _ in range(3)]
   for p in pred:
    probs=p['probabilidades'];require(len(probs)==3 and all(math.isfinite(v) and 0<=v<=1 for v in probs),'Probabilidades inválidas')
    require(abs(sum(probs)-1)<1e-5,'Probabilidades no suman uno')
    cm[cfg['classes'].index(p['clase'])][max(range(3),key=lambda i:probs[i])]+=1
   f1=sum(2*cm[i][i]/(sum(cm[i])+sum(row[i] for row in cm)) if sum(cm[i])+sum(row[i] for row in cm) else 0 for i in range(3))/3
   require(abs(f1-result['val_macro_f1'])<1e-6,'F1 no coincide con predicciones')
   identities.add(result['identity'])
   runs.append(dict(seed=seed,history=history,val_macro_f1=f1,best_epoch=result['best_epoch'],checkpoint_sha256=result['checkpoint_sha256'],predictions_sha256=result['predictions_sha256']))
 require(len(identities)==1,'Entornos/identidades distintos')
 return runs

def main():
 p=argparse.ArgumentParser();p.add_argument('zip',type=Path);p.add_argument('--check-only',action='store_true');a=p.parse_args()
 runs=receive(a.zip)
 print('Cinco semillas verificadas; checkpoint tratado como bytes, sin ejecutarlo.')
 if a.check_only:return
 h=hashlib.sha256()
 with a.zip.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 doc=dict(updated=datetime.now(timezone.utc).isoformat(),source='ZIP RunPod verificado por huellas, código, conteos y F1 recalculado; no constituye reproducción independiente.',status='Piloto de desarrollo completo',complete_seeds=5,planned_seeds=5,verified_artifacts=True,archive_sha256=h.hexdigest(),runs=runs)
 dest=ROOT/'data/piloto_estado.json';tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False));tmp.replace(dest)
 table=io.StringIO();w=csv.DictWriter(table,fieldnames=['seed','val_macro_f1','best_epoch','checkpoint_sha256','predictions_sha256']);w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in runs)
 (ROOT/'data/piloto_resumen.csv').write_text(table.getvalue())
 scores=[r['val_macro_f1'] for r in runs]
 text='# Resultados del piloto E3\n\nActualización: '+doc['updated']+'\n\n'+doc['source']+'\n\nSHA256 del ZIP: `'+doc['archive_sha256']+'`.\n\n| Semilla | Mejor época | Macro-F1 validación |\n|---|---:|---:|\n'
 text+=''.join(f"| {r['seed']} | {r['best_epoch']} | {r['val_macro_f1']:.6f} |\n" for r in runs)
 text+=f'\nMedia ± DE entre cinco semillas: {statistics.mean(scores):.6f} ± {statistics.stdev(scores):.6f}. La DE no es un intervalo de confianza.\n\nSelección realizada por validación; no se acredita evaluación en reserva, superioridad ni benchmark final. Las curvas del dashboard usan la misma fuente validada.\n'
 (ROOT/'book/14_resultados_piloto.md').write_text(text)
 toc=ROOT/'book/_toc.yml';s=toc.read_text()
 if '14_resultados_piloto' not in s:toc.write_text(s+'  - file: 14_resultados_piloto\n')
 print('Actualizados datos web y capítulo. Compilar libro y desplegar después de revisar.')
if __name__=='__main__':main()
