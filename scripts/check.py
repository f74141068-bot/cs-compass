"""Validate reproducible outputs, layout contract, and local URL targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from build import ROOT, load, build

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.urls=[]; self.h1=0; self.cards=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate HTML ID {a["id"]}'
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        for key in ('href','src'):
            if key in a: self.urls.append(a[key])
        if 'note-card' in a.get('class','').split(): self.cards.append(a['data-category'])

notes=load()
expected={ROOT/'index.html',ROOT/'workflow.html',*(ROOT/'notes'/f'{n["id"]}.html' for n in notes)}
actual=set(ROOT.glob('*.html'))|set((ROOT/'notes').glob('*.html'))
assert actual==expected, 'Unexpected or missing HTML files'
snapshot={p:p.read_bytes() for p in expected}
build()
assert all(p.read_bytes()==v for p,v in snapshot.items()), 'Generated HTML was stale; rebuild and commit it'
pages={}
for p in expected:
    obj=Page(); obj.feed(p.read_text(encoding='utf-8')); pages[p]=obj
    assert obj.h1==1, p
    if p.parent.name=='notes': assert {'concept','example','complexity','mistake','quiz'} <= obj.ids, p
home=pages[ROOT/'index.html']
assert home.cards==[n['category'] for n in notes]
assert all(f'notes/{n["id"]}.html' in home.urls for n in notes)
links=0
for p,obj in pages.items():
    for url in obj.urls:
        u=urlsplit(url)
        assert not u.scheme and not u.netloc and not u.path.startswith('/'), (p,url)
        dest=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert dest.is_relative_to(ROOT) and dest.is_file(), (p,url)
        if u.fragment: assert dest in pages and unquote(u.fragment) in pages[dest].ids, (p,url)
        links+=1
print(f'PASS: {len(notes)} notes, {len(pages)} reproducible HTML pages, {links} relative links/anchors; schema and required sections valid.')
