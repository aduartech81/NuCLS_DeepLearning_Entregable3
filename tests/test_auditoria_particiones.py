import csv,hashlib,io,zipfile
import pytest
from PIL import Image
from tools.auditar_particiones import audit

def archive(tmp_path,corrupt=False):
 p=tmp_path/'sample.zip';buf=io.BytesIO();Image.new('RGB',(128,128),(31,47,79)).save(buf,format='PNG');data=buf.getvalue()
 pixel=hashlib.sha256(Image.open(io.BytesIO(data)).tobytes()).hexdigest()
 rows=[dict(particion=s,paciente='shared',imagen='same_field',sha_imagen='same_source',sha_pixeles=pixel,sha_archivo=hashlib.sha256(data).hexdigest(),archivo=s+'/x.png') for s in ('train','validation')]
 if corrupt:rows[0]['sha_archivo']='bad_hash'
 csvfile=io.StringIO();w=csv.DictWriter(csvfile,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 with zipfile.ZipFile(p,'w') as z:
  z.writestr('manifiesto.csv',csvfile.getvalue())
  for r in rows:z.writestr(r['archivo'],data)
 return p

def test_audit_detects_actual_leakage_and_preserves_source(tmp_path):
 p=archive(tmp_path);before=p.read_bytes();result=audit(p)
 assert result['archivos_train_validacion_verificados']==2
 assert all(v==1 for v in result['cruces'][0]['coincidencias'].values())
 assert p.read_bytes()==before

def test_audit_rejects_corrupted_manifest(tmp_path):
 with pytest.raises(AssertionError):audit(archive(tmp_path,corrupt=True))
