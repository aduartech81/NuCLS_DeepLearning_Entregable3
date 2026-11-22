import csv,json,math
from pathlib import Path
from tools.sincronizar_auditoria import render_estado,render_auditoria,render_maestra
R=Path(__file__).resolve().parents[1]
def test_book_and_dashboard_use_same_audit():
 assert (R/'book/14_estado_entrega.md').read_text()==render_estado()
 assert (R/'book/17_auditoria_cierre.md').read_text()==render_auditoria()
 a=json.loads((R/'data/auditoria_cierre.json').read_text())
 req=json.loads((R/'revision/requisitos_e3.json').read_text())
 for x in a['filas']:
  if x['entregable']=='E3':assert x['falta_o_condicion']==next(y['estado'] for y in req if y['bloque']==x['id'])
def test_master_matches_verified_ablations():
 a=json.loads((R/'data/ablaciones_verificadas.json').read_text())
 rows=list(csv.DictReader((R/'data/tabla_maestra_disponible.csv').open()))
 for x in a['resumen']:
  row=next(y for y in rows if y['modelo']==('CICO' if x['variante']=='cico_completo' else x['variante']))
  assert int(row['semillas'])==5
  assert math.isclose(float(row['macro_f1']),x['media'],abs_tol=1e-12)
  assert math.isclose(float(row['sd_semillas']),x['sd'],abs_tol=1e-12)
def test_all_histology_assets_are_real_images():
 from app import app
 import xml.etree.ElementTree as ET
 c=app.server.test_client()
 for i in range(1,37):
  for kind in ['limpia','anotada']:
   r=c.get(f'/histologia-imagen/{i:02}/{kind}')
   assert r.status_code==200
   root=ET.fromstring(r.data)
   assert root.tag.endswith('svg')
   assert any(e.tag.endswith('image') for e in root.iter())

def test_book_master_and_precomputed_examples():
 assert (R/'book/21_tabla_maestra.md').read_text()==render_maestra()
 import hashlib
 maps=json.loads((R/'data/explicaciones_ejemplos.json').read_text())
 examples=json.loads((R/'data/ejemplos.json').read_text())
 for x in examples:
  key=hashlib.sha256((R/x['png_file']).read_text().strip().encode()).hexdigest()
  assert key in maps
  assert len(maps[key]['effects'])==8
  assert all(len(row)==8 for row in maps[key]['effects'])
