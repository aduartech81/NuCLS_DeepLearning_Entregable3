"""Benchmark reproducible de la app WSGI local; no accede a datos privados ni entrena.
Usa únicamente los seis ejemplos públicos. Memoria RSS muestreada, no pico absoluto.
"""
import concurrent.futures as cf
import hashlib,json,os,platform,socket,statistics,subprocess,sys,tempfile,threading,time
from pathlib import Path
import requests,numpy as np
ROOT=Path(__file__).resolve().parents[1]

def run():
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 base=f'http://127.0.0.1:{port}'; stop=threading.Event();rss=[]
 env=os.environ.copy();env['PYTHONPATH']=str(ROOT)
 result={}
 with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryFile() as log:
  memory=Path(tmp)/'memory.json';config=Path(tmp)/'gunicorn_config.py'
  config.write_text("import resource,sys\ndef post_worker_init(worker):\n original=worker.wsgi\n def wrapped(environ,start_response):\n  def response(status,headers,exc_info=None):\n   value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform=='darwin' else 1024)\n   headers.append(('X-Benchmark-RSS-MiB',str(value)))\n   return start_response(status,headers,exc_info)\n  return original(environ,response)\n worker.wsgi=wrapped\n")
  process=subprocess.Popen([sys.executable,'-m','gunicorn','app:server','--config',str(config),'--bind',f'127.0.0.1:{port}','--workers','1','--threads','2','--timeout','120','--access-logfile','/dev/null'],cwd=ROOT,env=env,stdout=log,stderr=log)
  try:
   for _ in range(100):
    try:
     if requests.get(base+'/_dash-layout',timeout=2).status_code==200:break
    except requests.RequestException:pass
    if process.poll() is not None:raise RuntimeError('WSGI startup failed')
    time.sleep(.1)
   else:raise RuntimeError('WSGI unavailable')
   examples=json.loads((ROOT/'data/ejemplos.json').read_text())
   def payload(i):
    e=examples[i%len(examples)];uri='data:image/png;base64,'+(ROOT/e['png_file']).read_text().strip()
    return {'output':'..pred-result.children...pred-memory.data..','outputs':[{'id':'pred-result','property':'children'},{'id':'pred-memory','property':'data'}],'inputs':[{'id':'pred-run','property':'n_clicks','value':1},{'id':'pred-upload','property':'contents','value':uri},{'id':'pred-consent','property':'value','value':['yes']}],'state':[{'id':'pred-memory','property':'data','value':None}],'changedPropIds':['pred-run.n_clicks']}
   def request(i):
    start=time.perf_counter();r=requests.post(base+'/_dash-update-component',json=payload(i),timeout=120);r.raise_for_status();rss.append(float(r.headers['X-Benchmark-RSS-MiB']));data=r.json()['response'];assert data['pred-memory']['data']['key'];assert 'Clase con mayor puntuación' in json.dumps(data,ensure_ascii=False)
    return (time.perf_counter()-start)*1000
   cold=request(0);results=[]
   for concurrency in [1,2,4]:
    start=time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:times=list(pool.map(request,range(60)))
    elapsed=time.perf_counter()-start
    results.append({'clientes':concurrency,'solicitudes':len(times),'errores':0,'p50_ms':float(np.percentile(times,50)),'p95_ms':float(np.percentile(times,95)),'max_ms':max(times),'solicitudes_segundo':len(times)/elapsed})
   invalid=payload(0);invalid['inputs'][1]['value']='data:image/png;base64,not_valid'
   bad=requests.post(base+'/_dash-update-component',json=invalid,timeout=30);assert bad.status_code==200 and 'No se pudo leer' in json.dumps(bad.json(),ensure_ascii=False)
   oversized=requests.post(base+'/_dash-update-component',data=b'x'*(3*1024*1024+1),headers={'Content-Type':'application/json'},timeout=30);assert oversized.status_code==413
   routes={}
   for case in range(1,37):
    for mode in ['limpia','anotada']:
     path=f'/histologia-imagen/{case:02}/{mode}';r=requests.get(base+path,timeout=10);assert r.status_code==200 and '<svg' in r.text;routes[path]=r.status_code
   assert requests.get(base+'/histologia-imagen/99/limpia',timeout=10).status_code==404
   after=request(1)
   result.update({'schema':1,'fecha_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'plataforma':platform.platform(),'python':platform.python_version(),'cpu':platform.machine(),'cpu_logicas':os.cpu_count(),'protocolo':{'worker':1,'threads':2,'modelo':'CICO 6101 ONNX','muestras_publicas':6,'warm_requests_total':180,'memoria_metodo':'getrusage ru_maxrss del worker en respuestas HTTP, cabecera solo en proceso de benchmark','ambito':'WSGI local, HTTP loopback. No representa latencia ni memoria del contenedor Render.'},'modelo_sha256':hashlib.sha256((ROOT/'models/cico_6101.onnx').read_bytes()).hexdigest(),'primera_prediccion_ms':cold,'worker_peak_rss_MiB':max(rss),'carga':results,'recuperacion_tras_entradas_invalidas_ms':after,'invalidos':{'base64_invalido':'mensaje claro; HTTP 200','cuerpo_mayor_3MiB':413,'caso_inexistente':404},'rutas_histologicas':routes,'limitaciones':['RSS máximo del worker durante toda su vida; no incluye el proceso maestro.','No es medición del plan gratuito Render; no demuestra un límite de concurrencia soportado.','Se evalúa CICO; no la familia de comparadores.']})
   return result
  finally:
   process.terminate()
   try:process.wait(timeout=10)
   except subprocess.TimeoutExpired:process.kill();process.wait()
   if memory.exists():result.update(json.loads(memory.read_text()))
if __name__=='__main__':
 out=ROOT/'data/diagnosticos/benchmark_servicio_cpu.json';out.write_text(json.dumps(run(),indent=2,ensure_ascii=False));print(out)
