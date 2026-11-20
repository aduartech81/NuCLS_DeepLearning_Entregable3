"""Exploratory CICO pilot. Read-only inputs; never reads reserve images."""
import argparse,csv,hashlib,json,os,platform,random,time
from pathlib import Path
import numpy as np
import torch
import PIL
import sys
from PIL import Image
from torch.utils.data import Dataset,DataLoader
from src.original_model import ContextoAcotado

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(path,obj):
 t=path.with_suffix(path.suffix+'.tmp');torch.save(obj,t);os.replace(t,path)
def write_json(path,obj):
 t=path.with_suffix('.json.tmp');t.write_text(json.dumps(obj,indent=2,allow_nan=False));os.replace(t,path)
def audit(root,cfg):
 root=Path(root).resolve();m=root/'manifiesto.csv'
 if not m.is_file():raise ValueError('Falta manifiesto.csv; no se inicia entrenamiento')
 if sha(m)!=cfg['manifest_sha256']:raise ValueError('SHA del manifiesto distinto')
 allrows=list(csv.DictReader(m.open()));groups={s:[r for r in allrows if r['particion']==s and r['estado']=='incluida'] for s in ('train','validation')}
 for key in ['paciente','tss','sha_pixeles']:
  if {r[key] for r in groups['train']} & {r[key] for r in groups['validation']}:raise ValueError('Solapamiento '+key)
 for s,rows in groups.items():
  if len(rows)!=cfg['counts'][s] or len({r['paciente'] for r in rows})!=cfg['patients'][s]:raise ValueError('Conteos distintos '+s)
  if set(r['clase'] for r in rows)!=set(cfg['classes']):raise ValueError('Clases incompletas')
  for r in rows:
   p=(root/r['archivo']).resolve()
   if not p.is_relative_to(root):raise ValueError('Ruta fuera de datos')
   with Image.open(p) as im:
    if im.mode!='RGB' or im.size!=(128,128):raise ValueError('Formato inválido')
    if hashlib.sha256(np.asarray(im).tobytes()).hexdigest()!=r['sha_pixeles']:raise ValueError('Imagen modificada')
 return groups
class Crops(Dataset):
 def __init__(self,root,rows,cfg,augment=False):self.root,self.rows,self.cfg,self.augment=Path(root),rows,cfg,augment
 def __len__(self):return len(self.rows)
 def __getitem__(self,i):
  r=self.rows[i]
  with Image.open(self.root/r['archivo']) as im:a=np.asarray(im).copy()
  if self.augment:
   a=np.rot90(a,random.randrange(4))
   if random.random()<.5:a=a[:,::-1]
  x=torch.from_numpy(a.copy()).permute(2,0,1).float()/255
  return (x-torch.tensor(self.cfg['mean'])[:,None,None])/torch.tensor(self.cfg['std'])[:,None,None],self.cfg['classes'].index(r['clase'])
def evaluate(net,loader,device,k):
 net.eval();cm=torch.zeros(k,k,dtype=torch.int64);probs=[];diagnostics=[]
 with torch.no_grad():
  for x,y in loader:
   d=net.components(x.to(device));pr=d['logits'].softmax(1).cpu();pred=pr.argmax(1)
   cm+=torch.bincount(y*k+pred,minlength=k*k).reshape(k,k);probs.extend(pr.tolist())
   diagnostics.extend(torch.cat([d['dispersion'],d['budget'],d['delta'].norm(dim=1,keepdim=True)],1).cpu().tolist())
 den=cm.sum(0)+cm.sum(1);f1=torch.where(den>0,2*cm.diag()/den,0).mean().item()
 return f1,probs,diagnostics

def run(root,out,config,device='cuda',seeds=None):
 cfg=json.loads(Path(config).read_text());groups=audit(root,cfg)
 if device=='cuda' and not torch.cuda.is_available():raise ValueError('GPU no disponible; no se inicia en CPU automáticamente')
 out=Path(out).resolve()
 if out==Path(root).resolve() or out.is_relative_to(Path(root).resolve()):raise ValueError('Salida debe estar fuera de los datos')
 out.mkdir(parents=True,exist_ok=True)
 ident=hashlib.sha256((sha(config)+sha(__file__)+sha(Path(__file__).parents[1]/'src/original_model.py')+torch.__version__+np.__version__+PIL.__version__+sys.version+device).encode()).hexdigest()
 lock=out/'EJECUCION_ACTIVA.json'
 with lock.open('x') as f:json.dump({'pid':os.getpid(),'host':platform.node(),'time':time.time()},f)
 try:
  torch.use_deterministic_algorithms(True)
  for seed in seeds or cfg['seeds']:
   folder=out/str(seed);folder.mkdir(exist_ok=True);done=folder/'resultado.json';last=folder/'ultimo.pt';bestfile=folder/'mejor.pt'
   if done.exists():
    old=json.loads(done.read_text())
    if old['identity']!=ident or sha(bestfile)!=old['checkpoint_sha256'] or sha(folder/'predicciones.json')!=old['predictions_sha256']:raise ValueError('Corrida completa incompatible o dañada')
    print('OMITIDA COMPLETA',seed,flush=True);continue
   random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
   if torch.cuda.is_available():torch.cuda.manual_seed_all(seed)
   net=ContextoAcotado(**cfg['model_config']).to(device);opt=torch.optim.AdamW(net.parameters(),lr=cfg['lr'],weight_decay=cfg['weight_decay'])
   start,best,bestepoch,bad,history=0,-1,0,0,[]
   train=DataLoader(Crops(root,groups['train'],cfg,True),batch_size=cfg['batch'],shuffle=True,num_workers=0)
   val=DataLoader(Crops(root,groups['validation'],cfg),batch_size=cfg['batch'],shuffle=False,num_workers=0)
   if last.exists():
    state=torch.load(last,map_location='cpu',weights_only=True)
    if state['identity']!=ident:raise ValueError('Checkpoint incompatible; usar otra salida')
    net.load_state_dict(state['model']);opt.load_state_dict(state['optimizer']);start=state['epoch'];best=state['best'];bestepoch=state['bestepoch'];bad=state['bad'];history=state['history']
    random.setstate(state['python_rng']);torch.set_rng_state(state['torch_rng'])
    if device=='cuda':torch.cuda.set_rng_state_all(state['cuda_rng'])
    print('REANUDANDO',seed,'época',start+1,flush=True)
   for epoch in range(start,cfg['epochs']):
    if bad>=cfg['patience'] and start>=cfg['min_epochs']:break
    net.train();begin=time.monotonic();loss_sum=0
    for x,y in train:
     opt.zero_grad();loss=torch.nn.functional.cross_entropy(net(x.to(device)),y.to(device))
     if not torch.isfinite(loss):raise ValueError('Pérdida no finita')
     loss.backward();opt.step();loss_sum+=loss.item()*len(y)
    score,_,diag=evaluate(net,val,device,len(cfg['classes']))
    if score>best:
     best,bestepoch,bad=score,epoch+1,0
     atomic(bestfile,{'trained':True,'model':net.state_dict(),'model_config':cfg['model_config'],'protocol_sha256':sha(config),'preprocessing':{'mean':cfg['mean'],'std':cfg['std']},'verification_inputs':next(iter(val))[0][:2],'identity':ident})
    else:bad+=1
    row={'epoch':epoch+1,'loss':loss_sum/len(train.dataset),'val_macro_f1':score,'seconds':time.monotonic()-begin,'mean_V_budget_delta':np.mean(diag,axis=0).tolist()};history.append(row)
    atomic(last,dict(identity=ident,model=net.state_dict(),optimizer=opt.state_dict(),epoch=epoch+1,best=best,bestepoch=bestepoch,bad=bad,history=history,python_rng=random.getstate(),torch_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state_all() if device=='cuda' else []))
    write_json(folder/'historia.json',history);print('CICO',seed,row,flush=True)
    if epoch+1>=cfg['min_epochs'] and bad>=cfg['patience']:break
   net.load_state_dict(torch.load(bestfile,map_location=device,weights_only=True)['model']);score,probs,diag=evaluate(net,val,device,len(cfg['classes']))
   write_json(folder/'predicciones.json',[dict(archivo=r['archivo'],paciente=r['paciente'],clase=r['clase'],probabilidades=pr,V=d[0],budget=d[1],delta_norm=d[2]) for r,pr,d in zip(groups['validation'],probs,diag)])
   write_json(done,dict(identity=ident,semilla=seed,val_macro_f1=score,best_epoch=bestepoch,checkpoint_sha256=sha(bestfile),predictions_sha256=sha(folder/'predicciones.json'),scope=cfg['scope']))
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':
 os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
 p=argparse.ArgumentParser();p.add_argument('--datos',required=True);p.add_argument('--salida',required=True);p.add_argument('--config',default='experiments/piloto_v1.json');p.add_argument('--audit-only',action='store_true');a=p.parse_args()
 if a.audit_only:
  g=audit(a.datos,json.loads(Path(a.config).read_text()));print({k:len(v) for k,v in g.items()})
 else:run(a.datos,a.salida,a.config)
