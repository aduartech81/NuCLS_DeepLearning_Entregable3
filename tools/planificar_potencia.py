"""Planificación aproximada, no potencia observada ni tamaño confirmatorio certificado."""
import json,math,statistics
from pathlib import Path
from statistics import NormalDist
R=Path(__file__).resolve().parents[1]
def calculate():
 a=json.loads((R/'data/ablaciones_verificadas.json').read_text());base={x['semilla']:x['macro_f1'] for x in a['corridas'] if x['variante']=='cico_completo'};rows=[]
 for v in ['sin_contraste','sin_amortiguacion','sin_contexto']:
  d=[x['macro_f1']-base[x['semilla']] for x in a['corridas'] if x['variante']==v];sd=statistics.stdev(d)
  z=NormalDist().inv_cdf(1-.05/(2*3))+NormalDist().inv_cdf(.90)
  rows.append(dict(variante=v,sd_diferencias=sd,n_piloto=5,mde90_n10=z*sd/math.sqrt(10),escenarios=[dict(delta=delta,n_normal_aprox=math.ceil((z*sd/delta)**2),n_con_piso_guia=max(10,math.ceil((z*sd/delta)**2))) for delta in [.01,.02,.03,.05]]))
 out=dict(alfa_familiar=.05,contrastes=3,potencia_objetivo_individual=.9,formula='n ≈ ((z(1−α/(2m)) + z(0,90)) × s_d / Δ)^2',alcance='Sensibilidad de planificación basada en cinco diferencias pareadas del piloto y aproximación normal bilateral con Bonferroni m=3. No es potencia conjunta, análisis de potencia del test exacto, preregistro ni garantía del tamaño final. La varianza es inestable con n=5. La familia final puede tener más contrastes: debe recalcularse antes de congelar el protocolo. Los deltas son escenarios, no márgenes elegidos tras ver resultados.',filas=rows)
 (R/'data/diagnosticos/planificacion_potencia.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 return out
if __name__=='__main__':calculate()
