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
PAGES=['home','over','prijzen','contact','sales','aanvraag','nulmeting','faq','blog','privacy','pagemap','meekijken','koppelingen','cms_wordpress','cms_webflow','cms_shopify','cms_wix','cms_framer','cms_websitebouwers','cms_code','cms_ai','cms_maatwerk']
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
            if mm and (mm.group(1) in PAGES or mm.group(1) in I18N[lang]['pages']): tag=tag.replace(mm.group(0),'href="%s"'%href(from_dir,lang,mm.group(1)))
        return tag
    return re.sub(r'<a\b[^>]*>',fix_tag,h)

def strip_tags(s): return html.unescape(re.sub(r'<[^>]+>','',s)).strip()

def imgfile(n):
    for e in ('png','jpg','webp'):
        if os.path.exists(os.path.join(S,'assets','img',n+'.'+e)): return 'img/%s.%s'%(n,e)
    raise SystemExit('missing image '+n)

def faq_schema(h):
    items=re.findall(r'<details(?: open)?><summary>(.*?)</summary>(.*?)</details>',h,re.S)
    q=[]
    for s,a in items:
        q.append({"@type":"Question","name":strip_tags(re.sub(r'<span class="chev".*?</span>','',s,flags=re.S)),
                  "acceptedAnswer":{"@type":"Answer","text":strip_tags(a)}})
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":q}

FOUNDERS=[("Tim Huijsmans","https://www.linkedin.com/in/tim-huijsmans-88b9761a7/"),("Damian Zoetemelk","https://www.linkedin.com/in/damian-zoetemelk-8524091a1/"),("Thimo van Soldt","https://www.linkedin.com/in/thimo-van-soldt-37118b220/")]
ORG_REF={"@type":"Organization","@id":DOMAIN+'/#organization',"name":"NXEO","url":DOMAIN+'/'}
def org_schema(lang):
    t=I18N[lang]
    return {"@context":"https://schema.org","@type":"Organization","@id":DOMAIN+'/#organization',"name":"NXEO","url":DOMAIN+'/',
            "logo":{"@type":"ImageObject","url":DOMAIN+'/assets/img/nxeo_icon.png'},"image":DOMAIN+'/assets/img/og.png',"description":t['org_description'],
            "email":"hello@nxeo.io","foundingDate":"2026","areaServed":[{"@type":"Country","name":"Netherlands"},{"@type":"Country","name":"Belgium"}],
            "knowsAbout":["Generative engine optimization","Search engine optimization","AI visibility","ChatGPT","Gemini","Claude","Perplexity","Google AI Overviews"],
            "founder":[{"@type":"Person","name":n,"jobTitle":"Founder","sameAs":[u],"worksFor":{"@id":DOMAIN+'/#organization'}} for n,u in FOUNDERS],
            "contactPoint":[{"@type":"ContactPoint","contactType":"sales","email":"sales@nxeo.io","availableLanguage":["Dutch","English"]},
                            {"@type":"ContactPoint","contactType":"customer support","email":"support@nxeo.io","availableLanguage":["Dutch","English"]}],
            "parentOrganization":[{"@type":"Organization","name":"IQ Script","url":"https://iqscript.com/"},{"@type":"Organization","name":"The AI Doctor","url":"https://theaidoctor.nl/"}]}

def product_schema(lang):
    names=[('Launch',99),('Groei' if lang=='nl' else 'Growth',179),('Schaal' if lang=='nl' else 'Scale',299)]
    return {"@context":"https://schema.org","@type":"SoftwareApplication","name":"NXEO","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":abs_url(lang,'prijzen'),
            "description":I18N[lang]['org_description'],"provider":ORG_REF,
            "offers":[{"@type":"Offer","name":n,"price":str(p),"priceCurrency":"EUR","url":abs_url(lang,'aanvraag'),"availability":"https://schema.org/InStock",
                       "priceSpecification":{"@type":"UnitPriceSpecification","price":str(p),"priceCurrency":"EUR","unitText":"MONTH","valueAddedTaxIncluded":False}} for n,p in names]}

def service_schema(lang,page):
    p=I18N[lang]['pages'][page]
    return {"@context":"https://schema.org","@type":"Service","name":p['title'].split('|')[0].strip(),"description":p['description'],"url":abs_url(lang,page),
            "serviceType":"AI visibility and website content","provider":ORG_REF,"areaServed":[{"@type":"Country","name":"Netherlands"},{"@type":"Country","name":"Belgium"}],
            "offers":{"@type":"Offer","price":"99","priceCurrency":"EUR","url":abs_url(lang,'prijzen')}}


# ---------- articles: markdown files in articles/<lang>/<slug>.md ----------
MONTHS={'nl':['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'],'en':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}
ATXT={'nl':dict(back='Alle artikelen',min='min lezen',more='Lees ook',read='Lees artikel',new='Nieuwste',by='Door NXEO',toc='In dit artikel',kort='In het kort',ch='Benieuwd hoe AI jouw bedrijf nu noemt?',cp='Vul je website in. Binnen 48 uur heb je het rapport in je mail, gratis.',ph='jouwwebsite.nl',aria='Je website',btn='Check mijn zichtbaarheid'),
      'en':dict(back='All articles',min='min read',more='Read next',read='Read article',new='Latest',by='By NXEO',toc='In this article',kort='In short',ch='Curious how AI mentions your company today?',cp='Enter your website. Within 48 hours the report is in your inbox, free.',ph='yourwebsite.com',aria='Your website',btn='Check my visibility')}
ARTSVG=open(S+'articles/_art.html').read().split('\n<!--split-->\n')
def md_inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    def link(m):
        txt,u=m.group(1),m.group(2)
        if u.startswith('#'): return '<a href="%s" data-link>%s</a>'%(u,txt)
        return '<a href="%s" target="_blank" rel="noopener">%s</a>'%(u,txt)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,t)
def md(text):
    out=[];toc=[];para=[];lst=None
    def flush():
        nonlocal para,lst
        if para: out.append('<p>%s</p>'%md_inline(' '.join(para))); para=[]
        if lst: out.append('<%s>%s</%s>'%(lst[0],''.join('<li>%s</li>'%md_inline(i) for i in lst[1]),lst[0])); lst=None
    for line in text.strip().split('\n'):
        s=line.strip()
        if not s: flush(); continue
        m=re.match(r'(#{2,3}) (.+)',s)
        if m:
            flush(); h=m.group(2); hid=re.sub(r'[^a-z0-9]+','-',h.lower()).strip('-')
            if len(m.group(1))==2: toc.append((hid,h)); out.append('<h2 id="%s">%s</h2>'%(hid,md_inline(h)))
            else: out.append('<h3>%s</h3>'%md_inline(h))
            continue
        m=re.match(r'(?:[-*]|(\d+)\.) (.+)',s)
        if m:
            kind='ol' if m.group(1) else 'ul'
            if para: out.append('<p>%s</p>'%md_inline(' '.join(para))); para=[]
            if not lst or lst[0]!=kind: flush(); lst=[kind,[]]
            lst[1].append(m.group(2)); continue
        if s.startswith('> '): flush(); out.append('<blockquote>%s</blockquote>'%md_inline(s[2:])); continue
        if lst: flush()
        para.append(s)
    flush()
    return '\n'.join(out),toc
def load_articles(lang):
    d=S+'articles/%s/'%lang; arts=[]
    if not os.path.isdir(d): return arts
    for f in sorted(os.listdir(d)):
        if not f.endswith('.md'): continue
        raw=open(d+f).read(); _,fm,body=raw.split('---',2)
        meta=dict((k.strip(),v.strip()) for k,v in (l.split(':',1) for l in fm.strip().split('\n')))
        slug=f[:-3]; y,mo,da=meta['date'].split('-')
        words=len(re.findall(r'\w+',body))
        arts.append(dict(meta,slug=slug,key='art_'+meta.get('ref',slug).replace('-','_'),body=body,words=words,mins=max(1,round(words/220)),nice='%d %s %s'%(int(da),MONTHS[lang][int(mo)-1],y)))
    arts.sort(key=lambda a:(a['date'],a['slug']),reverse=True)
    for i,a in enumerate(arts): a['svg']=ARTSVG[(len(arts)-1-i)%3]
    return arts
ARTS={l:load_articles(l) for l in LANGS}
for l in LANGS:
    for a in ARTS[l]:
        I18N[l]['pages'][a['key']]={'slug':I18N[l]['pages']['blog']['slug']+'/'+a['slug'],'title':a['title']+' | NXEO','description':a['description']}
def card(lang,a,lead=False):
    t=ATXT[lang]
    return ('<article class="bp%s" data-cat="%s"><a class="bp-pic" href="#%s" data-link tabindex="-1" aria-hidden="true">%s</a><div class="bp-b"><div class="bp-m"><b>%s</b><span>%s</span><span>%d min</span>%s</div>'
            '<h2><a href="#%s" data-link>%s</a></h2><p>%s</p><a class="bp-more" href="#%s" data-link>%s <span class="arr">→</span></a></div></article>')%(
            ' bp-lead' if lead else '',a['category'],a['key'],a['svg'].replace('<svg','<svg preserveAspectRatio="xMidYMid slice"',1) if 'preserveAspectRatio' not in a['svg'] else a['svg'],a['category'],a['nice'],a['mins'],'<i>%s</i>'%t['new'] if lead else '',a['key'],html.escape(a['title']),html.escape(a['description']),a['key'],t['read'])
def link_existing(lang,body):
    # fewer than three real articles: keep the static cards, but point a card with a matching title at the real article
    for a in ARTS[lang]:
        i=body.find(html.escape(a['title'],quote=False))
        if i<0: continue
        s=body.rfind('<article',0,i); e=body.find('</article>',i)
        body=body[:s]+body[s:e].replace('href="#blog"','href="#%s"'%a['key'])+body[e:]
    return body
def blog_overview(lang,body):
    arts=ARTS[lang]
    if len(arts)<3: return link_existing(lang,body)
    cats=[]
    for a in arts:
        if a['category'] not in cats: cats.append(a['category'])
    first=re.search(r'<button class="btn btn-sm ftab" type="button" data-bcat="" aria-selected="true">.*?</button>',body).group(0)
    tabs=first+''.join('<button class="btn btn-sm ftab" type="button" data-bcat="%s" aria-selected="false">%s</button>'%(c,c) for c in cats)
    body=re.sub(r'(<div class="faq-tabs bl-tabs" role="tablist">).*?(</div>\s*<div class="bl-grid">)',lambda m:m.group(1)+tabs+m.group(2),body,count=1,flags=re.S)
    cards=''.join(card(lang,a,i==0) for i,a in enumerate(arts))
    return re.sub(r'(<div class="bl-grid">).*?(</div>\s*<div class="np-cta bl-cta")',lambda m:m.group(1)+cards+m.group(2),body,count=1,flags=re.S)
def home_blog(lang,body):
    arts=ARTS[lang][:3]
    if len(arts)<3: return link_existing(lang,body)
    def rep(m):
        a=arts.pop(0) if arts else None
        if not a: return m.group(0)
        return ('<article class="post" data-reveal><div class="pic">%s</div><div class="pb"><div class="meta"><b>%s</b><span>·</span><span>%s</span><span>·</span><span>%d min</span></div><h4>%s</h4><p>%s</p><a class="more" href="#%s" data-link>%s <span class="arr">→</span></a></div></article>')%(a['svg'],a['category'],a['nice'],a['mins'],html.escape(a['title']),html.escape(a['description']),a['key'],ATXT[lang]['read'])
    return re.sub(r'<article class="post" data-reveal>.*?</article>',rep,body,flags=re.S)
def article_body(lang,page):
    t=ATXT[lang]; arts=ARTS[lang]; a=[x for x in arts if x['key']==page][0]
    body,toc=md(a['body'])
    rel=[x for x in arts if x is not a and x['category']==a['category']]+[x for x in arts if x is not a and x['category']!=a['category']]
    more=''.join(card(lang,x) for x in rel[:3])
    tocl=''.join('<li><a href="#%s">%s</a></li>'%(i,html.escape(h)) for i,h in toc)
    globe='<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg></span>'
    cta='<div class="np-cta bl-cta ar-cta"><div><h3>%s</h3><p>%s</p></div><form class="combo audit-combo np-form" data-baseline novalidate>%s<input name="site" type="url" placeholder="%s" required autocomplete="url" aria-label="%s"><button class="btn btn-blue" type="submit">%s <span class="arr">→</span></button></form></div>'%(t['ch'],t['cp'],globe,t['ph'],t['aria'],t['btn'])
    side=('<aside class="ar-side"><nav class="ar-toc" aria-label="%s"><b>%s</b><ol>%s</ol></nav>'
          '<div class="ar-mini"><b>%s</b><p>%s</p><a class="btn btn-blue btn-block" href="#nulmeting" data-link>%s <span class="arr">→</span></a></div></aside>')%(t['toc'],t['toc'],tocl,t['ch'],t['cp'],t['btn'])
    kort=[k.strip() for k in a.get('kort','').split('|') if k.strip()]
    kort_html=('<div class="ar-kort"><b>%s</b><ul>%s</ul></div>'%(t['kort'],''.join('<li>%s</li>'%md_inline(k) for k in kort))) if kort else ''
    return ('<section class="page" id="page-%s">\n<div class="ar-bar" aria-hidden="true"><i></i></div>\n<article class="ar2">\n'
            '<header class="hero hero-c ar-hero"><div class="hero-stack">'
            '<div class="bubble bubble-blue">%s · %d %s</div>'
            '<h1>%s<span class="cursor" aria-hidden="true"></span></h1><p class="def">%s</p>'
            '<div class="ar-by"><img src="{{nxeo_icon}}" alt=""><span>%s · %s</span></div></div></header>\n'
            '<div class="wrap ar-grid"><div class="ar-body">%s%s\n%s</div>%s</div>\n</article>\n'
            '%s</section>\n')%(page,a['category'],a['mins'],t['min'],html.escape(a['title']),html.escape(a['description']),t['by'],a['nice'],kort_html,body,cta,side,
            ('<div class="sec ar-more"><div class="wrap"><h2>%s</h2><div class="bl-grid is-filtered">%s</div></div></div>\n'%(t['more'],more)) if more else '')
def about_schema(lang):
    return {"@context":"https://schema.org","@type":"AboutPage","url":abs_url(lang,'over'),"name":I18N[lang]['pages']['over']['title'].split('|')[0].strip(),"inLanguage":lang,
            "mainEntity":{"@id":DOMAIN+'/#organization'},
            "about":[{"@type":"Person","name":n,"jobTitle":"Founder","sameAs":[u],"worksFor":{"@id":DOMAIN+'/#organization'}} for n,u in FOUNDERS]}

def list_schema(lang,keys,name):
    return {"@context":"https://schema.org","@type":"ItemList","name":name,"numberOfItems":len(keys),
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":I18N[lang]['pages'][k]['title'].split('|')[0].strip(),"url":abs_url(lang,k)} for i,k in enumerate(keys)]}

def blog_schema(lang):
    arts=sorted(ARTS[lang],key=lambda a:a['date'],reverse=True)
    return {"@context":"https://schema.org","@type":"Blog","name":I18N[lang]['pages']['blog']['title'].split('|')[0].strip(),"url":abs_url(lang,'blog'),"inLanguage":lang,"publisher":{"@id":DOMAIN+'/#organization'},
            "blogPost":[{"@type":"BlogPosting","headline":a['title'],"url":abs_url(lang,a['key']),"datePublished":a['date']} for a in arts]}

def howto_schema(lang,page,body):
    a=[x for x in ARTS[lang] if x['key']==page][0]
    steps=[]
    for m in re.finditer(r'<h2 id="[^"]*">(\d+)\. (.*?)</h2>(.*?)(?=<h2 )',body,re.S):
        txt=strip_tags(re.split(r'</p>',m.group(3))[0]+' '+' '.join(re.findall(r'<p><strong>(?:Wat je doet|What to do):</strong>(.*?)</p>',m.group(3),re.S)))
        steps.append({"@type":"HowToStep","position":int(m.group(1)),"name":strip_tags(m.group(2)),"text":' '.join(txt.split())})
    return {"@context":"https://schema.org","@type":"HowTo","name":a['title'],"description":a['description'],"inLanguage":lang,"totalTime":"PT10M","step":steps}

def article_schema(lang,page):
    a=[x for x in ARTS[lang] if x['key']==page][0]
    return {"@context":"https://schema.org","@type":"Article","headline":a['title'],"description":a['description'],"datePublished":a['date'],"dateModified":a['date'],"inLanguage":lang,"wordCount":a['words'],
            "mainEntityOfPage":abs_url(lang,page),"image":DOMAIN+'/assets/img/og.png',"author":ORG_REF,"publisher":{"@type":"Organization","@id":DOMAIN+'/#organization',"name":"NXEO","logo":{"@type":"ImageObject","url":DOMAIN+'/assets/img/nxeo_icon.png'}}}

def breadcrumb(lang,page):
    t=I18N[lang]
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":t['breadcrumb_home'],"item":abs_url(lang,'home')},
        ]+([{"@type":"ListItem","position":2,"name":t['pages']['blog']['title'].split('|')[0].strip(),"item":abs_url(lang,'blog')},{"@type":"ListItem","position":3,"name":t['pages'][page]['title'].split('|')[0].strip(),"item":abs_url(lang,page)}] if page.startswith('art_') else [{"@type":"ListItem","position":2,"name":t['pages'][page]['title'].split('|')[0].strip(),"item":abs_url(lang,page)}])}

def fit_title(s):
    s=s.strip()
    if len(s)>60 and s.endswith(' | NXEO'): s=s[:-7]
    if len(s)>62 and '. ' in s[:62]: s=s[:s.index('. ')+1]
    return s
def fit_desc(s,n=158):
    s=s.strip()
    if len(s)<=n: return s
    cut=s[:n+1]; i=max(cut.rfind('. '),cut.rfind('? '),cut.rfind('! '))
    if i>=70: return cut[:i+1]
    return cut[:cut.rfind(' ')].rstrip(',;:')+'.'

def head(lang,page,from_dir,extra_schema):
    t=I18N[lang]; p=t['pages'][page]
    have=[l for l in LANGS if page in I18N[l]['pages']]
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(l,abs_url(l,page)) for l in have)
    alts+='<link rel="alternate" hreflang="x-default" href="%s">\n'%abs_url(DEFAULT if DEFAULT in have else have[0],page)
    schemas=[org_schema(lang)]+([breadcrumb(lang,page)] if page!='home' else [{"@context":"https://schema.org","@type":"WebSite","name":"NXEO","url":DOMAIN+'/',"inLanguage":lang}])+extra_schema
    ld=''.join('<script type="application/ld+json">%s</script>\n'%json.dumps(s,ensure_ascii=False) for s in schemas)
    return ('<!doctype html>\n<html lang="%s" data-i18n-fpnote="%s" data-i18n-pct="%s">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n'
            '<link rel="canonical" href="%s">\n%s'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="NXEO">\n<meta property="og:locale" content="%s">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s/assets/img/og.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="theme-color" content="#002EFE">\n<meta name="google-site-verification" content="qTfyv3oxuXIxlGUtY8V4SRJZwc1Yp6CsGb1dBl-M5Hg">\n<link rel="icon" href="%s" type="image/png" sizes="192x192">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700;800&display=swap">\n'
            '<link rel="stylesheet" href="%s">\n<script>(function(){var h=document.documentElement;addEventListener("pagereveal",function(e){if(e.viewTransition){h.classList.add("vt");e.viewTransition.finished.finally(function(){h.classList.remove("vt")})}else{h.classList.remove("vt")}});addEventListener("pageswap",function(e){if(e.viewTransition)h.classList.add("vt")})})()</script>\n<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/assets/*"}}]},"eagerness":"moderate"}]}</script>\n%s</head>\n<body>\n')%(
            lang,html.escape(t['fpnote']),html.escape(t['pct']),html.escape(fit_title(p['title'])),html.escape(fit_desc(p['description'])),abs_url(lang,page),alts,
            t['locale'],html.escape(fit_title(p['title'])),html.escape(fit_desc(p['description'])),abs_url(lang,page),DOMAIN,asset(from_dir,'img/favicon.png'),asset(from_dir,'style.css'),ld)

def chrome(lang,page,from_dir):
    t=I18N[lang]
    hdr=read(lang,'header'); ftr=read(lang,'footer')
    others=[l for l in LANGS if l!=lang]
    o=others[0] if others else lang
    op=page if page in I18N[o]['pages'] else 'blog'
    sub={'langhref':href(from_dir,o,op),'langcode':o,'langaria':I18N[o]['switch_aria'],'langlabel':I18N[o]['switch_label'],'langswitch':I18N[o]['switch_text']}
    for k,v in sub.items(): hdr=hdr.replace('{{%s}}'%k,v); ftr=ftr.replace('{{%s}}'%k,v)
    # footer language select: one option per language, pointing at the same page
    opts=''.join('<option value="%s"%s>%s</option>'%(href(from_dir,l,page if page in I18N[l]['pages'] else 'blog'),' selected' if l==lang else '',I18N[l]['name']) for l in LANGS)
    ftr=re.sub(r'(<select id="langsel"[^>]*>).*?(</select>)',lambda m:m.group(1)+opts+m.group(2),ftr,flags=re.S)
    hdr=re.sub(r'data-nav="(\w+)"',lambda m:m.group(0)+(' aria-current="page"' if m.group(1)==page else ''),hdr)
    if page in ('aanvraag','sales','meekijken'): ftr=ftr.replace('<footer class="end">','<footer class="end no-cta">',1)
    return hdr,ftr

def pagemap(lang):
    # leesbaar overzicht van alle pagina's; sitemap.xml blijft de versie voor zoekmachines
    t=I18N[lang]; nl=lang=='nl'
    name=lambda k:'Home' if k=='home' else t['pages'][k]['title'].split('|')[0].strip()
    main=[k for k in PAGES if not k.startswith('cms_') and k not in ('koppelingen','pagemap','blog')]
    cms=['koppelingen']+[k for k in PAGES if k.startswith('cms_')]
    arts=sorted(ARTS[lang],key=lambda a:a['date'],reverse=True)
    def card(title,items):
        return '<div class="pm-card" data-reveal><h2>%s<span>%d</span></h2><div class="pm-rows">%s</div></div>'%(title,len(items),''.join('<a href="#%s" data-link><b>%s</b><span class="arr">→</span></a>'%(k,html.escape(n)) for k,n in items))
    total=len(main)+len(cms)+len(arts)+1
    lead=("%d pagina's, in drie groepen. Zoekmachines gebruiken <a href=\"/sitemap.xml\">sitemap.xml</a>." if nl else "%d pages, in three groups. Search engines use <a href=\"/sitemap.xml\">sitemap.xml</a>.")%total
    return ('<section class="page" id="page-pagemap">\n  <div class="faq-page">\n    <div class="wrap">\n      <div class="faq-head"><h1>%s</h1><p class="lead">%s</p></div>\n      <div class="pm-grid">%s%s%s</div>\n    </div>\n  </div>\n</section>\n')%(
        "Alle pagina's" if nl else 'All pages', lead,
        card("Pagina's" if nl else 'Pages',[(k,name(k)) for k in main]),
        card('Werkt met' if nl else 'Works with',[(k,name(k)) for k in cms]),
        card('Blog',[('blog',name('blog'))]+[(a['key'],a['title']) for a in arts]))

def build_page(lang,page):
    d=page_dir(lang,page)
    body=article_body(lang,page) if page.startswith('art_') else (pagemap(lang) if page=='pagemap' else read(lang,page))
    if page=='blog': body=blog_overview(lang,body)
    if page=='home': body=home_blog(lang,body)
    if '<div data-fp>' in body: body=body.replace('<div data-fp></div>',read(lang,'fp')).replace('<div data-fp>','').replace('</div><!--/fp-->','')
    body=re.sub(r'<section class="page" id="page-\w+">','<section class="page is-active" id="page-%s">'%page,body,count=1)
    extra=[faq_schema(body)] if page in ('faq','prijzen','nulmeting') or page.startswith('cms_') else ([article_schema(lang,page)] if page.startswith('art_') else [])
    if page=='prijzen': extra.append(product_schema(lang))
    if page=='home' and '<details' in body: extra.append(faq_schema(body))
    if page=='over': extra.append(about_schema(lang))
    if page=='koppelingen': extra.append(list_schema(lang,[k for k in PAGES if k.startswith('cms_')],I18N[lang]['pages']['koppelingen']['title'].split('|')[0].strip()))
    if page=='blog': extra.append(blog_schema(lang))
    if page.startswith('art_') and 'controlelijst' in page: extra.append(howto_schema(lang,page,body))
    if page.startswith('cms_') or page in ('nulmeting','meekijken','koppelingen'): extra.append(service_schema(lang,page))
    hdr,ftr=chrome(lang,page,d)
    doc=head(lang,page,d,extra)+hdr+'\n\n<main>\n'+body+'\n</main>\n\n'+ftr+'\n\n<script src="%s" defer></script>\n</body>\n</html>\n'%asset(d,'script.js')
    if 'class="hero hero-c' in body or 'hero-c' in body: doc=doc.replace('<html lang=','<html class="at-top" lang=',1)
    doc=rewrite_links(doc,lang,d)
    doc=re.sub(r'{{(\w+)}}',lambda m:asset(d,imgfile(m.group(1))),doc)
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
    allp=PAGES+sorted({a['key'] for l in LANGS for a in ARTS[l]})
    for p in allp:
        have=[l for l in LANGS if p in I18N[l]['pages']]
        for l in have:
            alts=''.join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n'%(a,abs_url(a,p)) for a in have)
            alts+='    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>\n'%abs_url(DEFAULT if DEFAULT in have else have[0],p)
            pri='1.0' if p=='home' else ('0.9' if p in ('prijzen','aanvraag','nulmeting') else ('0.3' if p=='privacy' else '0.7'))
            rows.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>%s</priority>\n%s  </url>'%(abs_url(l,p),TODAY,pri,alts))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(rows)+'\n</urlset>\n'

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT+'assets/img',exist_ok=True)
    css=open(S+'assets/style.css').read()
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S); css=re.sub(r'\n\s*','\n',css); css=re.sub(r'[ \t]{2,}',' ',css); css=re.sub(r'\n+','\n',css)
    open(OUT+'assets/style.css','w').write(css)
    js=open(S+'assets/script.js').read()
    js=js.replace("'__FPNOTE__'","document.documentElement.getAttribute('data-i18n-fpnote')").replace("'__PCT__'","document.documentElement.getAttribute('data-i18n-pct')")
    open(OUT+'assets/script.js','w').write(js)
    for f in os.listdir(S+'assets/img'): shutil.copy(S+'assets/img/'+f,OUT+'assets/img/'+f)
    n=0
    for l in LANGS:
        for p in PAGES+[a['key'] for a in ARTS[l]]: build_page(l,p); n+=1
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
        doc=rewrite_links(doc,DEFAULT,d); doc=re.sub(r'{{(\w+)}}',lambda m:asset(d,imgfile(m.group(1))),doc)
        open(OUT+'index.html','w').write(doc)
    print(MODE,n,'pages ->',OUT)

main()
