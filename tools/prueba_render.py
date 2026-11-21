"""HTTP functional check using only artificial pixels. Never sends patient images.
Run: python tools/prueba_render.py --url https://nucls-entregable3.onrender.com --out report.json
Measures request wall time and server-reported inference time separately.
"""
import argparse,base64,io,json,time,re,statistics,datetime,urllib.request
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--out',required=True);a=p.parse_args()
im=Image.new('RGB',(128,128));im.putdata([(x*2,y*2,(x+y)%256) for y in range(128) for x in range(128)]);buf=io.BytesIO();im.save(buf,format='PNG');contents='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
payload={'output':'pred-result.children','outputs':{'id':'pred-result','property':'children'},'changedPropIds':['pred-run.n_clicks'],'inputs':[{'id':'pred-run','property':'n_clicks','value':1}],'state':[{'id':'pred-upload','property':'contents','value':contents},{'id':'pred-consent','property':'value','value':['yes']}]}
results=[]
for i in range(6):
 req=urllib.request.Request(a.url.rstrip('/')+'/_dash-update-component',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 start=time.perf_counter()
 with urllib.request.urlopen(req,timeout=120) as response:data=response.read();status=response.status
 wall=(time.perf_counter()-start)*1000;text=data.decode();match=re.search(r'Tiempo de procesamiento en servidor: ([0-9.]+) ms',text)
 assert status==200 and 'Clase con mayor' in text and match and 'DOMINIO NO VERIFICADO' in text
 results.append({'iteration':i,'warmup':i==0,'http_status':status,'wall_ms':wall,'inference_reported_ms':float(match.group(1))})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':a.url,'input':'synthetic RGB gradient 128x128, not medical; functional test only','runs':results,'median_wall_ms_excluding_warmup':statistics.median(r['wall_ms'] for r in results[1:]),'median_server_ms_excluding_warmup':statistics.median(r['inference_reported_ms'] for r in results[1:]),'limits':'Six sequential requests, first excluded from medians; not a load test or accuracy evaluation. Wall time includes network and callback serialization. Server duration reported by application.'}
with open(a.out,'w') as f:json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
