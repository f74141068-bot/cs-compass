"""Build the static site from content/notes.json. Python 3, standard library only."""
from pathlib import Path
import json, html, re
ROOT = Path(__file__).resolve().parents[1]
E = html.escape
CATS = {'cpp':'C++ 基礎','structure':'資料結構','algorithm':'演算法'}
REQUIRED = {'id','title','category','level','summary','concepts','code','explanation','complexity','mistake','question','answer','related'}

def load():
    notes = json.loads((ROOT/'content/notes.json').read_text(encoding='utf-8'))
    ids = [n['id'] for n in notes]
    assert len(set(ids)) == len(ids), 'Duplicate IDs'
    for n in notes:
        assert set(n) == REQUIRED, n['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',n['id']), n['id']
        assert n['category'] in CATS and n['level'] in ('入門','進階')
        for k in REQUIRED-{'concepts','related'}: assert isinstance(n[k],str) and n[k].strip(), (n['id'],k)
        assert isinstance(n['concepts'],list) and len(n['concepts']) >= 2 and all(isinstance(x,str) and x.strip() for x in n['concepts'])
        assert isinstance(n['related'],list) and len(set(n['related'])) == len(n['related']) and all(x in ids and x != n['id'] for x in n['related'])
    return notes

def frame(title, body, prefix='', note=False):
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="CS Compass 資工學習知識庫"><title>{E(title)} | CS Compass</title><link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/app.js"></script></head>
<body><a class="skip" href="#main">跳至主要內容</a><header><div class="shell nav"><a class="brand" href="{prefix}index.html"><span class="logo" aria-hidden="true">✳</span> CS Compass<span class="brand-sub"> / STUDY LAB</span></a><nav aria-label="主要導覽"><a href="{prefix}index.html#library">學習筆記</a><a href="{prefix}workflow.html">AI 開發規則</a></nav></div></header><main id="main" class="shell">{body}</main><footer><div class="shell foot"><span>CS Compass · 資工學習知識庫</span><span>以知識為起點，持續累積。</span></div></footer></body></html>\n'''

def write(path, text): (ROOT/path).write_text(text,encoding='utf-8')

def build():
    notes=load(); byid={n['id']:n for n in notes}
    cards=[]
    for i,n in enumerate(notes,1):
        searchable=' '.join([n['title'],n['summary'],CATS[n['category']],*n['concepts']])
        cards.append(f'''<article class="note-card" data-category="{n['category']}" data-search="{E(searchable,quote=True)}"><div class="card-top"><span class="tag {n['category']}">{CATS[n['category']]}</span><span class="num">{i:02}</span></div><h3><a href="notes/{n['id']}.html">{E(n['title'])}</a></h3><p>{E(n['summary'])}</p><div class="card-bottom"><span>{n['level']}</span><a class="read" href="notes/{n['id']}.html" aria-label="閱讀 {E(n['title'])}">閱讀筆記 →</a></div></article>''')
    buttons=''.join(f'<button type="button" class="filter" data-filter="{key}" aria-pressed="false">{val}</button>' for key,val in CATS.items())
    home=f'''<section class="hero"><div><p class="eyebrow"><span class="dot"></span> PERSONAL KNOWLEDGE BASE / 001</p><h1>把複雜的知識，<br>變成<span class="accent">清楚的路徑。</span></h1><p class="lead">從 C++ 到資料結構與演算法，建立一套可以持續擴充的學習筆記。每一篇都從觀念、實作到自我檢核，讓理解真正留下來。</p><a class="primary" href="#library">探索學習筆記 ↓</a></div><aside class="hero-panel" aria-label="知識庫概況"><div class="panel-top"><span>KNOWLEDGE MAP</span><span class="live">● ACTIVE</span></div><div class="map"><div class="orbit o1"></div><div class="orbit o2"></div><div class="center-node">CS</div><span class="map-node node1">C++</span><span class="map-node node2">DS</span><span class="map-node node3">ALGO</span></div><div class="stats"><div><strong>{len(notes):02}</strong><span>篇筆記</span></div><div><strong>{len(CATS):02}</strong><span>大分類</span></div><div><strong>01</strong><span>套 AI 規則</span></div></div></aside></section><section id="library" class="library"><div class="section-head"><div><p class="eyebrow">01 / LIBRARY</p><h2>學習筆記</h2></div><p>找出你今天想掌握的概念。</p></div><div class="toolbar"><div class="filters" aria-label="筆記分類"><button type="button" class="filter" data-filter="all" aria-pressed="true">全部</button>{buttons}</div><label class="search"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="搜尋關鍵字，例如 stack" aria-label="搜尋學習筆記"></label></div><p id="result-count" class="result" aria-live="polite">共 {len(notes)} 篇筆記</p><div class="cards">{''.join(cards)}</div><p id="empty" hidden>沒有符合的筆記，請試試其他關鍵字或分類。</p><noscript>未啟用 JavaScript，仍可閱讀所有筆記；搜尋與篩選需啟用 JavaScript。</noscript></section><section class="callout"><div><p class="eyebrow">02 / BUILT TO GROW</p><h2>不只是網站，也是一套工作方法。</h2><p>統一資料格式、版型與驗收流程，讓下一個 AI 能接手並延續知識庫。</p></div><a class="secondary" href="workflow.html">了解 AI 開發規則 →</a></section>'''
    write('index.html',frame('首頁',home))
    for n in notes:
        related=''.join(f'<a class="related" href="{r}.html">{E(byid[r]["title"])} →</a>' for r in n['related']) or '<p>暫無相關筆記。</p>'
        body=f'''<div class="breadcrumb"><a href="../index.html#library">學習筆記</a> / {CATS[n['category']]}</div><article class="article"><div class="article-head"><span class="tag {n['category']}">{CATS[n['category']]}</span> <span class="muted">{n['level']}</span><h1>{E(n['title'])}</h1><p class="lead">{E(n['summary'])}</p></div><div class="article-grid"><aside class="toc"><p class="eyebrow">ON THIS PAGE</p><a href="#concept">01 核心觀念</a><a href="#example">02 C++ 實作</a><a href="#complexity">03 複雜度</a><a href="#mistake">04 常見錯誤</a><a href="#quiz">05 自我測驗</a></aside><div class="article-body"><section id="concept"><h2>01 / 核心觀念</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in n['concepts'])}</ul></section><section id="example"><h2>02 / C++ 實作</h2><div class="code-label">C++17 · 可獨立編譯範例</div><pre><code>{E(n['code'])}</code></pre><p>{E(n['explanation'])}</p></section><section id="complexity"><h2>03 / 複雜度</h2><p>{E(n['complexity'])}</p></section><section id="mistake"><h2>04 / 常見錯誤</h2><p class="warning">{E(n['mistake'])}</p></section><section id="quiz"><h2>05 / 自我測驗</h2><p>{E(n['question'])}</p><details><summary>展開參考答案</summary><p>{E(n['answer'])}</p></details></section><section><h2>延伸學習</h2>{related}</section></div></div></article>'''
        write(f'notes/{n["id"]}.html',frame(n['title'],body,'../',True))
    workflow='''<div class="breadcrumb"><a href="index.html">首頁</a> / AI 開發規則</div><article class="article"><div class="article-head"><p class="eyebrow">PROJECT HANDBOOK / V1.0</p><h1>讓 AI 有一套<br><span class="accent">可以遵循的工作方式。</span></h1><p class="lead">AGENTS.md 是本專案的開發手冊。把內容結構、設計限制與完成條件明文化，使不同 AI 都能依照相同方式新增筆記。</p><a class="primary" href="AGENTS.md">查看 AGENTS.md →</a></div><div class="steps"><div><span>01</span><h3>讀取規則</h3><p>先閱讀 AGENTS.md 與現有資料，確認允許修改的範圍。</p></div><div><span>02</span><h3>新增內容</h3><p>在 content/notes.json 增加唯一 ID 的筆記，填寫固定欄位。</p></div><div><span>03</span><h3>產生頁面</h3><p>執行 build.py，自動生成首頁卡片、筆記頁與導覽。</p></div><div><span>04</span><h3>驗收成果</h3><p>執行 check.py，並以瀏覽器檢查搜尋、連結及版面。</p></div></div><section class="case"><p class="eyebrow">EXTENSION CASE / 001</p><h2>擴充案例：二元搜尋 Binary Search</h2><p>在初始四篇筆記之外，依同一資料格式新增二元搜尋。重新生成後，自動出現在演算法分類，具有相同觀念、程式碼、複雜度、錯誤提醒、自我測驗及相關筆記。</p><a class="secondary" href="notes/binary-search.html">查看新增的筆記 →</a><p class="muted">操作方式、實際驗收項目及下一篇筆記的提示詞，請見專案 README。</p></section></article>'''
    write('workflow.html',frame('AI 開發規則',workflow))
    print(f'Built {len(notes)} notes + home + workflow')

if __name__=='__main__': build()
