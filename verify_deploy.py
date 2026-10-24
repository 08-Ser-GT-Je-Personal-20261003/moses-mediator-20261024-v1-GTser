from pathlib import Path
import urllib.request,json,concurrent.futures
P=Path(__file__).parent
bases=['https://08-ser-gt-je-personal-20261003.github.io/moses-mediator-20261024-v1-GTser/','https://moses-mediator-20261024-v1-gtser.surge.sh/']
jobs=[(b,f)for b in bases for f in ['index.html','apostles.html','nicene.html','athanasian.html','style.css','app.js']]
def check(job):
 b,f=job
 for attempt in range(3):
  try:
   request=urllib.request.Request(b+f,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(request,timeout=10)as r:data=r.read();status=r.status
   return {'url':b+f,'status':status,'matches_local':data.decode('utf-8').replace('\r\n','\n')==(P/'dist'/f).read_text(encoding='utf-8'),'comparison':'UTF-8 text; platform newline differences normalized'}
  except Exception as e:error=str(e)
 return {'url':b+f,'status':None,'matches_local':False,'error':error}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(check,jobs))
(P/'qa/deployment.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
assert all(x['status']==200 and x['matches_local']for x in results),results
print('PASS: both public deployments; all four HTML pages and both asset files match local outputs.')
