from pathlib import Path
from html.parser import HTMLParser
import json,re
P=Path(__file__).parent
class Check(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.hrefs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if 'href'in a:self.hrefs.append(a['href'])
checks=[]
for file in (P/'dist').glob('*.html'):
 h=Check();text=file.read_text(encoding='utf-8');h.feed(text)
 assert len(h.ids)==len(set(h.ids)),f'duplicate IDs in {file}'
 for link in h.hrefs:
  if link.startswith('#'):assert link[1:]in h.ids,(file,link)
  elif not re.match(r'https?://',link):assert (file.parent/link.split('#')[0]).exists(),(file,link)
 assert 'name="viewport"'in text
 checks.append({'page':file.name,'anchors':len(h.ids),'links':len(h.hrefs)})
study=json.loads((P/'study.json').read_text(encoding='utf-8'))
assert len(study['discussions'])==12
content=json.loads((P/'content.json').read_text(encoding='utf-8'))
assert len(content['sermon'])==3
assert all(len(x['paragraphs'])>=6 for x in content['sermon'])
print(json.dumps({'static_validation':'PASS','pages':checks,'discussion_count':12},ensure_ascii=False))
