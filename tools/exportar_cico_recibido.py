from pathlib import Path
import sys,json,zipfile,io,hashlib,time,platform,statistics
import torch,numpy as np,onnx,onnxruntime as ort
import argparse
ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);args=ap.parse_args()
r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r))
from src.original_model import ContextoAcotado
torch.set_num_threads(2)
archive=args.archive
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='fe2ac1e3abcfbdca81f8f86b85f03a28c5c5cb037160057fb71192c8895dd2ba'
with zipfile.ZipFile(archive) as z:
 assert z.read('codigo/src/original_model.py')==(r/'src/original_model.py').read_bytes()
 cfgbytes=z.read('codigo/experiments/piloto_v1.json');cfg=json.loads(cfgbytes)
 results=[json.loads(z.read(f'resultados/{s}/resultado.json')) for s in cfg['seeds']]
 result=max(results,key=lambda x:(x['val_macro_f1'],-x['semilla']));seed=result['semilla']
 b=z.read(f'resultados/{seed}/mejor.pt');assert hashlib.sha256(b).hexdigest()==result['checkpoint_sha256']
 pred=json.loads(z.read(f'resultados/{seed}/predicciones.json'))
 c=torch.load(io.BytesIO(b),map_location='cpu',weights_only=True)
assert c['trained'] and c['protocol_sha256']==hashlib.sha256(cfgbytes).hexdigest()
assert c['model_config']==cfg['model_config']
m=ContextoAcotado(**c['model_config']).eval();m.load_state_dict(c['model'],strict=True)
x=c['verification_inputs'].float().contiguous();assert x.shape==(2,3,128,128)
with torch.no_grad():ref=m(x).numpy()
probs=np.exp(ref-ref.max(1,keepdims=True));probs/=probs.sum(1,keepdims=True)
gpuerror=float(np.max(np.abs(probs-np.array([p['probabilidades'] for p in pred[:2]]))))
assert gpuerror<=1e-4,gpuerror
out=r/'models';out.mkdir(exist_ok=True);modelpath=out/'cico_6101.onnx'
torch.onnx.export(m,x[:1],str(modelpath),opset_version=17,dynamo=False,input_names=['image'],output_names=['logits'])
onnx.checker.check_model(onnx.load(str(modelpath)))
opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
sess=ort.InferenceSession(str(modelpath),sess_options=opts,providers=['CPUExecutionProvider'])
g=torch.Generator().manual_seed(20261121);stress=torch.randn(16,3,128,128,generator=g);samples=torch.cat([x,stress])
with torch.no_grad():expected=m(samples).numpy()
actual=np.concatenate([sess.run(None,{'image':a[None].numpy()})[0] for a in samples]);error=float(np.max(np.abs(actual-expected)));assert error<=1e-4,error
for _ in range(5):sess.run(None,{'image':x[:1].numpy()})
times=[]
for _ in range(30):
 begin=time.perf_counter();sess.run(None,{'image':x[:1].numpy()});times.append((time.perf_counter()-begin)*1000)
meta=dict(schema_version=1,verified=True,seed=seed,sha256=hashlib.sha256(modelpath.read_bytes()).hexdigest(),checkpoint_sha256=result['checkpoint_sha256'],protocol_sha256=c['protocol_sha256'],archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),classes=cfg['classes'],labels_es=cfg['class_labels_es'],mean=cfg['mean'],std=cfg['std'],input_shape=[1,3,128,128],selection='Mayor macro-F1 de validación entre cinco semillas; empates menor semilla. Demostración exploratoria, no selección final confirmatoria.',validation_macro_f1=result['val_macro_f1'],max_absolute_logit_error=error,max_probability_error_vs_runpod=gpuerror,verification_samples=dict(real_validation=2,synthetic_equivalence_stress=16),latency_cpu_local=dict(median_ms=statistics.median(times),p95_ms=float(np.percentile(times,95)),runs=30,warmup=5,threads=2,platform=platform.platform(),not_render_measurement=True),versions=dict(torch=torch.__version__,onnx=onnx.__version__,onnxruntime=ort.__version__,numpy=np.__version__))
(out/'cico_6101.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
# Save a small golden input/output for numerical verification after deployment; no original image file.
np.savez_compressed(out/'verification.npz',image=x[:1].numpy(),logits=actual[:1])
print(json.dumps(meta,indent=2));print('BYTES',modelpath.stat().st_size)
