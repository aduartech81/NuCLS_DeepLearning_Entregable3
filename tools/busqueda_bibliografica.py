"""Búsqueda exploratoria trazable de antecedentes. No declara exhaustividad ni novedad."""
from pathlib import Path
import requests,json,hashlib,datetime,concurrent.futures as cf,csv,re,time
ROOT=Path(__file__).resolve().parents[1]
QUERIES=['histopathology rotation invariant group equivariant convolution','histopathology nuclei center surround context classification','neural network bounded residual context gating','orientation disagreement uncertainty neural networks','selective kernel attention context histology']
def search(db):
 out=[]
 for i,q in enumerate(QUERIES,1):
  if db=='Europe PMC':url='https://www.ebi.ac.uk/europepmc/webservices/rest/search';params={'query':q,'format':'json','pageSize':10,'resultType':'core'}
  elif db=='Crossref':url='https://api.crossref.org/works';params={'query.bibliographic':q,'rows':10}
  else:url='https://api.openalex.org/works';params={'search':q,'per-page':10}
  rec={'base':db,'cadena':i,'consulta':q,'fecha_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limite':10,'orden':'relevancia predeterminada; primera página'}
  try:
   rec['intentos']=[]
   for attempt in range(3):
    r=requests.get(url,params=params,timeout=20,headers={'User-Agent':'NuCLEA-academic-literature-audit/1.0'});rec['intentos'].append(r.status_code)
    if r.status_code!=429:break
    wait=r.headers.get('Retry-After','5')
    if not wait.isdigit() or int(wait)>30:break
    time.sleep(max(5,int(wait)))
   rec.update(url=r.url,http=r.status_code)
   r.raise_for_status();j=r.json();rec['respuesta_sha256']=hashlib.sha256(r.content).hexdigest()
   if db=='Europe PMC':total=j['hitCount'];items=j['resultList']['result'];parsed=[{'titulo':x.get('title'),'doi':x.get('doi',''),'id':x.get('id'),'url':'https://europepmc.org/article/'+x.get('source','MED')+'/'+x.get('id',''),'abstract_disponible':bool(x.get('abstractText'))} for x in items]
   elif db=='Crossref':total=j['message']['total-results'];items=j['message']['items'];parsed=[{'titulo':x.get('title',[''])[0],'doi':x.get('DOI',''),'id':x.get('DOI',''),'url':x.get('URL'),'abstract_disponible':bool(x.get('abstract'))} for x in items]
   else:total=j['meta']['count'];items=j['results'];parsed=[{'titulo':x.get('display_name'),'doi':(x.get('doi') or '').replace('https://doi.org/',''),'id':x.get('id'),'url':x.get('doi') or x.get('id'),'abstract_disponible':bool(x.get('abstract_inverted_index'))} for x in items]
   rec.update(total_declarado=total,registros=parsed)
  except Exception as e:rec['error']=type(e).__name__;rec['registros']=[]
  out.append(rec)
  if db=='Crossref':time.sleep(2)
 return out
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=3) as ex:logs=[r for batch in ex.map(search,['Europe PMC','Crossref','OpenAlex']) for r in batch]
 unique={}
 for q in logs:
  for r in q['registros']:
   key=r['doi'].lower() or re.sub(r'\W','',r['titulo'].lower())
   if key not in unique:unique[key]={**r,'fuentes':[],'decision':'PENDIENTE cribado y texto completo'}
   unique[key]['fuentes'].append(q['base']+':'+str(q['cadena']))
 result={'objetivo':'Antecedentes del mecanismo CICO; búsqueda exploratoria posterior al piloto. No preregistro retrospectivo.','consultas':logs,'recuperados':sum(len(q['registros']) for q in logs),'unicos':len(unique),'deduplicacion':'DOI normalizado; si falta, título sin signos ni espacios','registros_unicos':list(unique.values()),'limites':['Solo diez primeros resultados por consulta; cobertura truncada y no exhaustiva.','Crossref ordena consultas bibliográficas, no equivale a búsqueda booleana.','Cero artículos se marcan como revisados por haber recuperado metadatos.','Pendientes cribado, textos completos, snowballing y adjudicación independiente.']}
 out=ROOT/'data/diagnosticos/busqueda_antecedentes.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2));print({k:result[k] for k in ['recuperados','unicos']});print([(q['base'],q['cadena'],q.get('http'),len(q['registros'])) for q in logs])
