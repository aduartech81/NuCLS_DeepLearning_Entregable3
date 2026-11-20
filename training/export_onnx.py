"""Export a trusted, trained checkpoint only. Never execute arbitrary pickle objects."""
import argparse, json, hashlib
from pathlib import Path
import torch
import numpy as np
import onnxruntime as ort
from src.original_model import ContextoAcotado

def export(checkpoint, output):
 c=torch.load(checkpoint,map_location='cpu',weights_only=True)
 if c.get('trained') is not True or not c.get('protocol_sha256'):
  raise ValueError('A trained checkpoint with protocol hash is required')
 m=ContextoAcotado(**c['model_config']).eval();m.load_state_dict(c['model'])
 x=c['verification_inputs'].float()
 if x.shape[0]<2: raise ValueError('At least two verification crops required')
 output=Path(output)
 if output.exists(): raise FileExistsError(output)
 output.parent.mkdir(parents=True,exist_ok=True)
 temp=output.with_suffix('.tmp.onnx')
 torch.onnx.export(m,x[:1],str(temp),opset_version=17,dynamo=False,input_names=['image'],output_names=['logits'])
 session=ort.InferenceSession(str(temp),providers=['CPUExecutionProvider'])
 with torch.no_grad(): expected=m(x).numpy()
 actual=np.concatenate([session.run(None,{'image':a[None].numpy()})[0] for a in x])
 error=float(np.max(np.abs(actual-expected)))
 if not np.isfinite(error) or error>1e-4: raise ValueError(f'Roundtrip failed: {error}')
 temp.rename(output)
 output.with_suffix('.json').write_text(json.dumps({'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'protocol_sha256':c['protocol_sha256'],'max_absolute_error':error,'preprocessing':c['preprocessing'],'model_config':c['model_config'],'input_shape':list(x[:1].shape)},indent=2))
 return error
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('checkpoint');p.add_argument('output');a=p.parse_args();print(export(a.checkpoint,a.output))
