"""Diagnóstico descriptivo reproducible de seis ejemplos públicos. No entrena."""
from pathlib import Path
import json,hashlib,time,platform
import numpy as np
from src.inference import decode_upload,engine,ROOT

def evaluate():
 session,meta=engine();mean=np.array(meta['mean'],np.float32);std=np.array(meta['std'],np.float32)
 def prob(a):
  x=np.ascontiguousarray(((a-mean)/std).transpose(2,0,1)[None]);z=session.run(['logits'],{'image':x})[0][0];p=np.exp(z-z.max());return p/p.sum()
 def sensitivity(a,target):
  base=prob(a)[target];fill=a.mean((0,1));effects=[]
  for k in range(64):
   masked=a.copy();i,j=divmod(k,8);masked[i*16:(i+1)*16,j*16:(j+1)*16]=fill
   effects.append(float(base-prob(masked)[target]))
  return np.array(effects).reshape(8,8)
 fractions=np.arange(0,65,8)/64
 def curves(a,target,order):
  fill=a.mean((0,1));deleted=a.copy();inserted=np.broadcast_to(fill,a.shape).copy();d=[float(prob(deleted)[target])];s=[float(prob(inserted)[target])]
  for step,k in enumerate(order,1):
   i,j=divmod(int(k),8);sl=np.s_[i*16:(i+1)*16,j*16:(j+1)*16]
   deleted[sl]=fill;inserted[sl]=a[sl]
   if step%8==0:d.append(float(prob(deleted)[target]));s.append(float(prob(inserted)[target]))
  return np.array(d),np.array(s)
 rows=[];start=time.perf_counter()
 for example in json.loads((ROOT/'data/ejemplos.json').read_text()):
  content='data:image/png;base64,'+(ROOT/example['png_file']).read_text().strip();a=decode_upload(content);p=prob(a);target=int(p.argmax());effects=sensitivity(a,target)
  order=np.argsort(-effects.ravel(),kind='stable');d,s=curves(a,target,order)
  random_d=[];random_s=[]
  for seed in range(10):
   rd,rs=curves(a,target,np.random.default_rng(20261122+seed).permutation(64));random_d.append(rd);random_s.append(rs)
  rd=np.array(random_d);rs=np.array(random_s);rotated=np.rot90(a).copy();rot_effect=sensitivity(rotated,target);aligned=np.rot90(rot_effect,-1)
  corr=float(np.corrcoef(effects.ravel(),aligned.ravel())[0,1]) if effects.std()>1e-12 and aligned.std()>1e-12 else None
  rows.append(dict(caso=example['caso'],imagen_sha256=example['sha256'],clase_referencia=example['clase_referencia'],clase_objetivo=meta['labels_es'][target],fracciones=fractions.tolist(),eliminacion=d.tolist(),insercion=s.tolist(),eliminacion_aleatoria_media=rd.mean(0).tolist(),insercion_aleatoria_media=rs.mean(0).tolist(),auc_eliminacion=float(np.trapezoid(d,fractions)),auc_insercion=float(np.trapezoid(s,fractions)),auc_eliminacion_aleatoria=float(np.trapezoid(rd,fractions,axis=1).mean()),auc_insercion_aleatoria=float(np.trapezoid(rs,fractions,axis=1).mean()),correlacion_mapa_rotado=corr,error_absoluto_mapa_rotado=float(np.abs(effects-aligned).max()),cambio_max_prob_rotacion=float(np.abs(p-prob(rotated)).max()),rango_mapa=float(np.ptp(effects))))
  print(example['caso'],'completo',flush=True)
 out=dict(fecha='2026-11-22',modelo_sha256=meta['sha256'],proveedores=session.get_providers(),python=platform.python_version(),numpy=np.__version__,semillas_control=list(range(20261122,20261132)),metodo='Oclusión 8×8, bloques 16px, relleno media RGB de la imagen, orden descendente de caída de probabilidad. Curvas acumuladas cada 8 bloques; diez órdenes aleatorios fijos. Rotación 90 grados y alineación inversa del mapa.',alcance='Seis ejemplos públicos de validación, seleccionados para demostración. Diagnóstico descriptivo, no muestra independiente ni validación clínica. La referencia aleatoria es un control del orden; no prueba causalidad. La rotación prueba una simetría de diseño de CICO, no robustez general. No corrige Inception E2 ni cierra fidelidad/estabilidad de la familia.',segundos=time.perf_counter()-start,casos=rows)
 (ROOT/'data/diagnosticos/explicaciones_cpu.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':evaluate()
