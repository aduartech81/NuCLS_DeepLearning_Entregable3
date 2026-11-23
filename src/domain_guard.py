"""Descriptive appearance-distance guard, not a clinical or semantic OOD guarantee."""
from functools import lru_cache
from pathlib import Path
import json
import numpy as np

def features(a):
 a=np.asarray(a,dtype=np.float64)
 h=np.concatenate([np.histogram(a[:,:,c],bins=8,range=(0,1))[0]/a.shape[0]/a.shape[1] for c in range(3)])
 return np.r_[h,a.mean((0,1)),a.std((0,1)),np.abs(np.diff(a,axis=0)).mean((0,1)),np.abs(np.diff(a,axis=1)).mean((0,1))]

@lru_cache(maxsize=1)
def parameters():
 return json.loads((Path(__file__).resolve().parents[1]/'models/domain_guard.json').read_text())

def assess(a, model=None):
 m=parameters() if model is None else model
 z=(features(a)-np.array(m['mean']))/np.array(m['scale'])
 score=float(np.sqrt(max(0,z @ np.array(m['precision']) @ z)))
 return dict(accepted=score<=m['threshold'],distance=score,threshold=m['threshold'],method='Distancia de apariencia RGB y textura; no identificación semántica de tejido')

def enforce(a):
 d=assess(a)
 if not d['accepted']:
  raise ValueError('Análisis retenido: la apariencia de esta imagen se aleja de la referencia NuCLS. No se emite una clase. Usa un recorte compatible; este control puede rechazar tejido válido y no detecta todas las imágenes ajenas al dominio.')
 return d
