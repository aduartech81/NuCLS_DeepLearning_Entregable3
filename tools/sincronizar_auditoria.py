"""Renderiza estados y matrices desde las mismas fuentes usadas por NuCLEA."""
import json,csv,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
def render_estado():
 e=read('data/estado_entrega.json')
 text='# Estado de entrega: evidencia y pendientes\n\n'+e['corte']+'\n\n'+e['alcance']+'\n\n'+e['plazo']+'\n\n[Auditoría detallada E2/E3](17_auditoria_cierre.md).\n'
 for x in e['items']:
  text+=f"\n## {x['etapa']} · {x['componente']}\n\n**Estado:** {x['estado']}.\n\n**Evidencia:** {x['evidencia']}\n\n**Pendiente:** {x['falta']}\n\n**Dependencia:** {x['dependencia']}\n"
 return text

def render_auditoria():
 a=read('data/auditoria_cierre.json');p=read('data/pcam_estado.json')
 text='# Auditoría contra las guías originales E2 y E3\n\n'+a['corte']+'. No es calificación oficial ni certificado de cumplimiento.\n\n'+a['alcance']+'\n\n'
 text+='## Fuentes y alcance\n\n'
 for f in a['fuentes']:text+=f"- {f['documento']} ({f['paginas']} páginas), SHA-256 `{f['sha256']}`.\n"
 text+='\nLas 15 ablaciones y el piloto están verificados. No sustituyen el benchmark final ni demuestran superioridad. Las 65 evaluaciones de reserva y las 66 corridas de desarrollo son cortes diferentes. No se repiten por esta revisión. E1 y el ZIP entregado se conservan.\n\n## PCam: respaldo y continuación\n\n'+p['estado']+'\n\n'+p['continuacion']+'\n\n'
 for etapa in ['E2','E3']:
  text+=f'## Matriz {etapa}\n\n| ID | Requisito | Guía | Estado y condición de cierre |\n|---|---|---|---|\n'
  for x in a['filas']:
   if x['entregable']==etapa:text+='| '+' | '.join(str(x[k]).replace('|','/') for k in ['id','requisito','guia'])+' | '+x['estado']+'. '+x['falta_o_condicion'].replace('|','/')+' |\n'
 text+='\n## Decisiones de cierre\n\n1. Recibir el próximo respaldo PCam y verificarlo antes de actualizar resultados. El último inventario no es seguimiento en vivo.\n2. Congelar protocolo, partición independiente y datos externos antes de nuevas evaluaciones confirmatorias. La reserva histórica expuesta no puede volver a sellarse.\n3. Completar revisión humana de errores, literatura, licencia, autoría y reproducción por tercero. Estos pendientes no se solucionan con GPU.\n4. Validar controles, estadísticas, exportaciones y demostración; generar una nueva entrega con hashes sin reemplazar el ZIP anterior.\n\n[Resultados de ablaciones](15_ablaciones_y_transicion.md) · [Estado resumido](14_estado_entrega.md) · [Análisis CPU](18_cierre_cpu.md).\n'
 return text

def render_maestra():
 rows=list(csv.DictReader((ROOT/'data/tabla_maestra_disponible.csv').open()))
 text='# Tabla maestra de resultados disponibles\n\nLa misma tabla alimenta NuCLEA. Media y desviación estándar entre semillas; no son intervalos por paciente. Las poblaciones de cada corte son diferentes: no se ordenan conjuntamente como prueba de superioridad. PCam y el benchmark confirmatorio no se incorporan sin artefactos verificados.\n\n| Corte | Modelo | Semillas | Macro-F1 medio | DE entre semillas |\n|---|---|---:|---:|---:|\n'
 for r in rows:text+=f"| {r['etapa']} | {r['modelo']} | {r['semillas']} | {float(r['macro_f1']):.6f} | {float(r['sd_semillas']):.6f} |\n"
 return text

def synchronize():
 (ROOT/'book/14_estado_entrega.md').write_text(render_estado())
 (ROOT/'book/17_auditoria_cierre.md').write_text(render_auditoria())
 (ROOT/'book/21_tabla_maestra.md').write_text(render_maestra())
if __name__=='__main__':synchronize()
