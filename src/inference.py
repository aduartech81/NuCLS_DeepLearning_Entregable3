"""CPU-only inference. Uploaded images are decoded in memory, never written to disk."""
import base64,binascii,hashlib,io,json,threading
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,UnidentifiedImageError
ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=2*1024*1024
LOCK=threading.Lock()

def decode_upload(contents):
 if not isinstance(contents,str) or len(contents)>MAX_BYTES*4//3+128:raise ValueError('El archivo supera el límite de 2 MB.')
 try:
  header,encoded=contents.split(',',1)
  if header not in ('data:image/png;base64','data:image/jpeg;base64'):raise ValueError('Solo se aceptan PNG o JPEG.')
  raw=base64.b64decode(encoded,validate=True)
  if not raw or len(raw)>MAX_BYTES:raise ValueError('Tamaño de archivo inválido.')
  with Image.open(io.BytesIO(raw)) as im:
   if im.format not in ('PNG','JPEG') or im.mode!='RGB' or im.size!=(128,128) or getattr(im,'n_frames',1)!=1:raise ValueError('Usa un recorte RGB de 128 × 128 píxeles, sin transparencia ni animación. No se redimensiona automáticamente.')
   im.load();a=np.asarray(im,dtype=np.float32)/255.
 except (binascii.Error,UnidentifiedImageError,OSError,Image.DecompressionBombError) as e:raise ValueError('No se pudo leer una imagen válida.') from e
 return a

@lru_cache(maxsize=1)
def engine():
 import onnxruntime as ort
 meta=json.loads((ROOT/'models/cico_6101.json').read_text());p=ROOT/'models/cico_6101.onnx'
 if meta.get('verified') is not True or hashlib.sha256(p.read_bytes()).hexdigest()!=meta['sha256']:raise RuntimeError('Artefacto no verificado.')
 if meta['input_shape']!=[1,3,128,128] or len(meta['classes'])!=3:raise RuntimeError('Contrato de entrada inválido.')
 mean=np.asarray(meta['mean'],dtype=np.float32);std=np.asarray(meta['std'],dtype=np.float32)
 if mean.shape!=(3,) or std.shape!=(3,) or not np.isfinite(mean).all() or not np.isfinite(std).all() or (std<=0).any():raise RuntimeError('Normalización inválida.')
 opt=ort.SessionOptions();opt.intra_op_num_threads=2;opt.inter_op_num_threads=1
 session=ort.InferenceSession(str(p),sess_options=opt,providers=['CPUExecutionProvider'])
 if session.get_inputs()[0].shape!=[1,3,128,128]:raise RuntimeError('Dimensiones del modelo incompatibles.')
 return session,meta

def predict(contents):
 a=decode_upload(contents);session,meta=engine()
 x=np.ascontiguousarray(((a-np.asarray(meta['mean'],np.float32))/np.asarray(meta['std'],np.float32)).transpose(2,0,1)[None])
 with LOCK:logits=session.run(['logits'],{'image':x})[0][0]
 if logits.shape!=(3,) or not np.isfinite(logits).all():raise RuntimeError('Salida inválida del modelo.')
 p=np.exp(logits-logits.max());p/=p.sum()
 return dict(seed=meta['seed'],labels=meta['labels_es'],probabilities=p.tolist(),prediction=meta['labels_es'][int(p.argmax())])
