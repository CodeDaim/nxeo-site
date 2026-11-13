"""Static site build for nxeo.io

  python3 build.py            -> dist/ with absolute URLs (/nl/prijzen/), for the real host
  python3 build.py preview    -> dist-preview/ with relative URLs, for the artifact preview

Content lives in content/<lang>/<page>.html, strings and slugs in i18n/<lang>.json.
A new language is a new content folder plus a json file; nothing here changes.
"""
import os,re,json,sys,shutil,html,datetime
S=os.path.dirname(os.path.abspath(__file__))+'/'
MODE=sys.argv[1] if len(sys.argv)>1 else 'prod'
OUT=S+('dist-preview/' if MODE=='preview' else 'dist/')
DOMAIN='https://nxeo.io'
LANGS=[l for l in ['nl','en','de'] if os.path.exists(S+'i18n/%s.json'%l) and os.path.isdir(S+'content/%s'%l)]
DEFAULT='nl'
PAGES=['home','over','prijzen','contact','sales','aanvraag','nulmeting','faq','blog','privacy']
I18N={l:json.load(open(S+'i18n/%s.json'%l)) for l in LANGS}
TODAY=datetime.date.today().isoformat()

def page_dir(lang,page):
    slug=I18N[lang]['pages'][page]['slug']
    return lang+'/'+(slug+'/' if slug else '')

def abs_url(lang,page):  # canonical, always the real domain
    return DOMAIN+'/'+page_dir(lang,page)

def rel(from_dir,to_path):
    """relative path from a directory (e.g. 'nl/prijzen/') to a file or dir path"""
    up='../'*from_dir.count('/')
    return (up+to_path) if (up+to_path) else './'

def href(from_dir,lang,page,frag=''):
    if MODE=='prod': return '/'+page_dir(lang,page)+frag
    d=page_dir(lang,page)
    r=rel(from_dir,d+'index.html')
    return r+frag

import hashlib
def ver(path):
    try: return '?v='+hashlib.md5(open(S+'assets/'+path,'rb').read()).hexdigest()[:8]
    except OSError: return ''
def asset(from_dir,path):
    q=ver(path) if path.endswith(('.css','.js')) else ''
    return (('/assets/'+path) if MODE=='prod' else rel(from_dir,'assets/'+path))+q

def read(lang,name): return open(S+'content/%s/%s.html'%(lang,name)).read()

def rewrite_links(h,lang,from_dir):
    def fix_tag(m):
        tag=m.group(0)
        if ' data-link-jump' in tag:
            mm=re.search(r'href="#([\w-]+)"',tag)
            if mm: tag=tag.replace(mm.group(0),'href="%s"'%href(from_dir,lang,'home','#'+mm.group(1)))
        elif re.search(r' data-link(?=[\s>])',tag):
            mm=re.search(r'href="#(\w+)"',tag)
            if mm and mm.group(1) in PAGES: tag=tag.replace(mm.group(0),'href="%s"'%href(from_dir,lang,mm.group(1)))
        return tag
    return re.sub(r'<a\b[^>]*>',fix_tag,h)

def strip_tags(s): return html.unescape(re.sub(r'<[^>]+>','',s)).strip()

def faq_schema(h):
    items=re.findall(r'<details(?: open)?><summary>(.*?)</summary>(.*?)</details>',h,re.S)
    q=[]
    for s,a in items:
        q.append({"@type":"Question","name":strip_tags(re.sub(r'<span class="chev".*?</span>','',s,flags=re.S)),
                  "acceptedAnswer":{"@type":"Answer","text":strip_tags(a)}})
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":q}

def org_schema(lang):
    t=I18N[lang]
    return {"@context":"https://schema.org","@type":"Organization","name":"NXEO","url":DOMAIN+'/',
            "logo":DOMAIN+'/assets/img/nxeo.png',"description":t['org_description'],
            "email":"hello@nxeo.io","sameAs":["https://www.linkedin.com/"],
            "parentOrganization":[{"@type":"Organization","name":"IQ Script","url":"https://iqscript.com/"},{"@type":"Organization","name":"The AI Doctor","url":"https://theaidoctor.nl/"}]}

def breadcrumb(lang,page):
    t=I18N[lang]
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":t['breadcrumb_home'],"item":abs_url(lang,'home')},
        {"@type":"ListItem","position":2,"name":t['pages'][page]['title'].split('|')[0].strip(),"item":abs_url(lang,page)}]}

def head(lang,page,from_dir,extra_schema):
    t=I18N[lang]; p=t['pages'][page]
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(l,abs_url(l,page)) for l in LANGS)
    alts+='<link rel="alternate" hreflang="x-default" href="%s">\n'%abs_url(DEFAULT,page)
    schemas=[org_schema(lang)]+([breadcrumb(lang,page)] if page!='home' else [{"@context":"https://schema.org","@type":"WebSite","name":"NXEO","url":DOMAIN+'/',"inLanguage":lang}])+extra_schema
    ld=''.join('<script type="application/ld+json">%s</script>\n'%json.dumps(s,ensure_ascii=False) for s in schemas)
    return ('<!doctype html>\n<html lang="%s" data-i18n-fpnote="%s" data-i18n-pct="%s">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n'
            '<link rel="canonical" href="%s">\n%s'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="NXEO">\n<meta property="og:locale" content="%s">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s/assets/img/nxeo.png">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="theme-color" content="#002EFE">\n<link rel="icon" href="%s" type="image/png" sizes="192x192">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700;800&display=swap">\n'
            '<link rel="stylesheet" href="%s">\n<script>(function(){var h=document.documentElement;addEventListener("pagereveal",function(e){if(e.viewTransition){h.classList.add("vt");e.viewTransition.finished.finally(function(){h.classList.remove("vt")})}else{h.classList.remove("vt")}});addEventListener("pageswap",function(e){if(e.viewTransition)h.classList.add("vt")})})()</script>\n<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/assets/*"}}]},"eagerness":"moderate"}]}</script>\n%s</head>\n<body>\n')%(
            lang,html.escape(t['fpnote']),html.escape(t['pct']),html.escape(p['title']),html.escape(p['description']),abs_url(lang,page),alts,
            t['locale'],html.escape(p['title']),html.escape(p['description']),abs_url(lang,page),DOMAIN,asset(from_dir,'img/favicon.png'),asset(from_dir,'style.css'),ld)

def chrome(lang,page,from_dir):
    t=I18N[lang]
    hdr=read(lang,'header'); ftr=read(lang,'footer')
    others=[l for l in LANGS if l!=lang]
    o=others[0] if others else lang
    sub={'langhref':href(from_dir,o,page),'langcode':o,'langaria':I18N[o]['switch_aria'],'langlabel':I18N[o]['switch_label'],'langswitch':I18N[o]['switch_text']}
    for k,v in sub.items(): hdr=hdr.replace('{{%s}}'%k,v); ftr=ftr.replace('{{%s}}'%k,v)
    # footer language select: one option per language, pointing at the same page
    opts=''.join('<option value="%s"%s>%s</option>'%(href(from_dir,l,page),' selected' if l==lang else '',I18N[l]['name']) for l in LANGS)
    ftr=re.sub(r'(<select id="langsel"[^>]*>).*?(</select>)',lambda m:m.group(1)+opts+m.group(2),ftr,flags=re.S)
    hdr=re.sub(r'data-nav="(\w+)"',lambda m:m.group(0)+(' aria-current="page"' if m.group(1)==page else ''),hdr)
    return hdr,ftr

def build_page(lang,page):
    d=page_dir(lang,page)
    body=read(lang,page)
    if '<div data-fp>' in body: body=body.replace('<div data-fp></div>',read(lang,'fp')).replace('<div data-fp>','').replace('</div><!--/fp-->','')
    body=re.sub(r'<section class="page" id="page-\w+">','<section class="page is-active" id="page-%s">'%page,body,count=1)
    extra=[faq_schema(body)] if page=='faq' else []
    hdr,ftr=chrome(lang,page,d)
    doc=head(lang,page,d,extra)+hdr+'\n\n<main>\n'+body+'\n</main>\n\n'+ftr+'\n\n<script src="%s" defer></script>\n</body>\n</html>\n'%asset(d,'script.js')
    doc=rewrite_links(doc,lang,d)
    doc=re.sub(r'{{(\w+)}}',lambda m:asset(d,'img/%s.png'%m.group(1)),doc)
    assert '{{' not in doc
    os.makedirs(OUT+d,exist_ok=True)
    open(OUT+d+'index.html','w').write(doc)
    return doc

def root_redirect():
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(l,abs_url(l,'home')) for l in LANGS)
    links=' · '.join('<a href="/%s/">%s</a>'%(l,I18N[l]['name']) for l in LANGS)
    js="var l=(navigator.languages||[navigator.language||'nl']).map(function(x){return x.slice(0,2).toLowerCase()});var s=%s;for(var i=0;i<l.length;i++){if(s.indexOf(l[i])>=0){location.replace('/'+l[i]+'/');return;}}location.replace('/%s/');"%(json.dumps(LANGS),DEFAULT)
    return ('<!doctype html>\n<html lang="nl">\n<head>\n<meta charset="utf-8">\n<title>NXEO</title>\n<meta name="robots" content="noindex">\n'
            '<link rel="canonical" href="%s/%s/">\n%s<link rel="alternate" hreflang="x-default" href="%s/">\n'
            '<meta http-equiv="refresh" content="1; url=/%s/">\n<script>(function(){%s})();</script>\n'
            '<style>body{font-family:"Rethink Sans",system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;background:#fff;color:#1A2332}a{color:#002EFE}</style>\n'
            '</head>\n<body><p>NXEO · %s</p></body>\n</html>\n')%(DOMAIN,DEFAULT,alts,DOMAIN,DEFAULT,js,links)

def sitemap():
    rows=[]
    for p in PAGES:
        for l in LANGS:
            alts=''.join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n'%(a,abs_url(a,p)) for a in LANGS)
            alts+='    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n'%abs_url(DEFAULT,p)
            pri='1.0' if p=='home' else ('0.9' if p in ('prijzen','aanvraag','nulmeting') else ('0.3' if p=='privacy' else '0.7'))
            rows.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>\n%s  </url>'%(abs_url(l,p),TODAY,pri,alts))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(rows)+'\n</urlset>\n'

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT+'assets/img',exist_ok=True)
    shutil.copy(S+'assets/style.css',OUT+'assets/style.css')
    js=open(S+'assets/script.js').read()
    js=js.replace("'__FPNOTE__'","document.documentElement.getAttribute('data-i18n-fpnote')").replace("'__PCT__'","document.documentElement.getAttribute('data-i18n-pct')")
    open(OUT+'assets/script.js','w').write(js)
    for f in os.listdir(S+'assets/img'): shutil.copy(S+'assets/img/'+f,OUT+'assets/img/'+f)
    n=0
    for l in LANGS:
        for p in PAGES: build_page(l,p); n+=1
    if MODE=='prod':
        open(OUT+'index.html','w').write(root_redirect())
        open(OUT+'sitemap.xml','w').write(sitemap())
        open(OUT+'robots.txt','w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n'%DOMAIN)
        # a simple 404 in the default language, pointing home
        nf=build_page(DEFAULT,'home')
        open(OUT+'404.html','w').write(nf.replace('<main>','<main>\n<div class="wrap" style="padding:3rem 0 0"><p class="eyebrow">404</p><h1 style="font-size:2rem">Deze pagina bestaat niet (meer).</h1><p class="lead">Hieronder gewoon de homepage.</p></div>',1).replace('<link rel="canonical"','<meta name="robots" content="noindex">\n<link rel="canonical"',1))
    else:
        # preview: the artifact root is the Dutch home page
        d=''
        hdr,ftr=chrome(DEFAULT,'home',d)
        body=read(DEFAULT,'home'); body=re.sub(r'<section class="page" id="page-\w+">','<section class="page is-active" id="page-home">',body,count=1)
        doc=head(DEFAULT,'home',d,[])+hdr+'\n\n<main>\n'+body+'\n</main>\n\n'+ftr+'\n\n<script src="%s" defer></script>\n</body>\n</html>\n'%asset(d,'script.js')
        doc=rewrite_links(doc,DEFAULT,d); doc=re.sub(r'{{(\w+)}}',lambda m:asset(d,'img/%s.png'%m.group(1)),doc)
        open(OUT+'index.html','w').write(doc)
    print(MODE,n,'pages ->',OUT)

main()
