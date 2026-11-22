"""Auditoría de integridad y separación; lee el ZIP, nunca cambia particiones."""
import argparse,csv,hashlib,io,json,itertools,zipfile,collections
from pathlib import Path
from PIL import Image

def audit(path):
 groups=collections.defaultdict(list);verified=0
 with zipfile.ZipFile(path) as z:
  raw=z.read('manifiesto.csv');rows=list(csv.DictReader(io.StringIO(raw.decode())))
  names=set(z.namelist())
  for r in rows:
   groups[r['particion']].append(r)
   if r['particion'] not in ('train','validation'):continue
   assert r['archivo'] in names,r['archivo']
   data=z.read(r['archivo']);assert hashlib.sha256(data).hexdigest()==r['sha_archivo']
   with Image.open(io.BytesIO(data)) as im:
    assert im.size==(128,128) and im.mode=='RGB'
    assert hashlib.sha256(im.tobytes()).hexdigest()==r['sha_pixeles']
   verified+=1
 pairs=[]
 for a,b in itertools.combinations(sorted(groups),2):
  overlap={key:len({r[key] for r in groups[a]} & {r[key] for r in groups[b]}) for key in ['paciente','imagen','sha_imagen','sha_pixeles','sha_archivo']}
  pairs.append({'a':a,'b':b,'coincidencias':overlap})
 duplicates={}
 for split,rs in groups.items():
  c=collections.Counter(r['sha_pixeles'] for r in rs);duplicates[split]={'grupos_pixeles_duplicados':sum(n>1 for n in c.values()),'copias_adicionales':sum(n-1 for n in c.values())}
 return {'fuente':Path(path).name,'manifiesto_sha256':hashlib.sha256(raw).hexdigest(),'n_filas':len(rows),'archivos_train_validacion_verificados':verified,'particiones':{k:{'n':len(v),'pacientes':len({r['paciente'] for r in v}),'campos':len({r['imagen'] for r in v})} for k,v in groups.items()},'cruces':pairs,'duplicados_internos':duplicates,'alcance':'Hash de bytes, píxeles RGB, dimensiones, identidad de pacientes y campos. Reserva candidata: solo metadatos del manifiesto; no se evalúa ni se utiliza para selección.','limites':['No detecta duplicados aproximados, identidad incorrecta del paciente ni errores de anotación.','Separación nominal no demuestra ausencia de fuga por decisiones previas; no certifica una prueba confirmatoria intacta.']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('zip');a=p.parse_args();r=audit(a.zip)
 out=Path(__file__).resolve().parents[1]/'data/diagnosticos/auditoria_particiones.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
