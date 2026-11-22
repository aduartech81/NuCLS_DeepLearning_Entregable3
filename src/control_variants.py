"""Controles nuevos aislados: mismos parámetros; no modifica modelo ni checkpoints.
La igualdad de capacidad se refiere a parámetros almacenados, no a FLOPs activos.
"""
from .original_model import ContextoAcotado
CONFIGS={
 'base_central':dict(use_orbit=False,use_contrast=False,use_dispersion=False,use_context=False),
 'solo_orbita':dict(use_orbit=True,use_contrast=False,use_dispersion=False,use_context=False),
 'solo_contexto':dict(use_orbit=False,use_contrast=False,use_dispersion=False,use_context=True),
 'contexto_contraste':dict(use_orbit=False,use_contrast=True,use_dispersion=False,use_context=True),
 'orbita_contexto':dict(use_orbit=True,use_contrast=False,use_dispersion=False,use_context=True),
 'orbita_contexto_contraste':dict(use_orbit=True,use_contrast=True,use_dispersion=False,use_context=True),
 'cico_completo':dict(use_orbit=True,use_contrast=True,use_dispersion=True,use_context=True),
}
def build_control(name,reference=None,**kwargs):
 if name not in CONFIGS:raise ValueError('Control desconocido')
 model=ContextoAcotado(**kwargs,**CONFIGS[name])
 if reference is not None:model.load_state_dict(reference.state_dict(),strict=True)
 return model
