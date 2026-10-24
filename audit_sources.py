"""Verify source URLs and exact short quotations without redistributing full texts."""
from pathlib import Path
import json,urllib.request,hashlib,re
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).parent
study=json.loads((P/'study.json').read_text(encoding='utf-8'))
base='https://ccifellowship.org/books/book-of-praise/'
quotes={base+'creeds/apostles-creed':'我信神，全能的父，创造天地的主。',base+'creeds/nicene-creed':'受生却非被造，与父同质；万物都是藉着他造的。',base+'creeds/athanasian-creed':'其位格不紊，其本质不分'}
urls=list(dict.fromkeys(list(quotes)+[x['url']for x in study['confessions']]))
def check(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25)as r:data=r.read();status=r.status
  text=data.decode('utf-8');result={'url':url,'status':status,'response_sha256':hashlib.sha256(data).hexdigest()}
  if url in quotes:result['exact_quote_verified']=quotes[url]in re.sub('<[^>]*>','',text);result['quote']=quotes[url]
  return result
 except Exception as e:return {'url':url,'error':str(e)}
with ThreadPoolExecutor(max_workers=4)as pool:results=list(pool.map(check,urls))
(P/'qa').mkdir(exist_ok=True)
(P/'qa/source-audit.json').write_text(json.dumps({'date':'2026-10-24','pages':results},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
