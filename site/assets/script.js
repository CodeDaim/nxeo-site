(function(){
  // a fresh page starts at the top; back and forward keep their place
  try{var nav=performance.getEntriesByType('navigation')[0];if(nav&&nav.type==='navigate'&&!location.hash){window.scrollTo(0,0);}}catch(e){}
  var mnav=document.getElementById('mnav');
  // on a page that opens with the blue block, the bar stays invisible until you scroll
  var heroC=document.querySelector('.hero-c');
  if(heroC){
    var hdrEl=document.getElementById('hdr'),inHero=null;
    var atTop=function(){var v=heroC.getBoundingClientRect().bottom>90;if(v===inHero)return;var first=inHero===null;inHero=v;
      document.documentElement.classList.toggle('at-top',v);
      hdrEl.classList.toggle('drop',!v&&!first);};
    atTop();window.addEventListener('scroll',atTop,{passive:true});window.addEventListener('resize',atTop);
  }
  // Menu: a glass pill that glides to the item under the pointer and rests on the current page
  (function(){
    if(!window.matchMedia('(hover:hover) and (pointer:fine)').matches)return;
    function group(box,sel){
      if(!box)return;var items=box.querySelectorAll(sel);if(!items.length)return;
      var pill=document.createElement('span');pill.className='nav-pill';pill.setAttribute('aria-hidden','true');box.insertBefore(pill,box.firstChild);
      var cur=box.querySelector('a[aria-current]'),shown=false,first=true;
      function to(a){if(!a){pill.classList.remove('is-on');shown=false;return;}
        var x=a.offsetLeft,w=a.offsetWidth;
        if(!shown){pill.style.transition=first?'none':'opacity 260ms ease';pill.style.transform='translateX('+x+'px)';pill.style.width=w+'px';void pill.offsetWidth;pill.style.transition='';}
        else{pill.style.transform='translateX('+x+'px)';pill.style.width=w+'px';}
        pill.classList.add('is-on');shown=true;if(first){void pill.offsetWidth;pill.style.transition='';first=false;}}
      box.querySelectorAll('a').forEach(function(a){var on=a.matches(sel);a.addEventListener('mouseenter',function(){to(on?a:cur);});a.addEventListener('focus',function(){to(on?a:cur);});});
      box.addEventListener('mouseleave',function(){to(cur);});box.addEventListener('focusout',function(e){if(!box.contains(e.relatedTarget))to(cur);});
      if(cur){if(document.fonts&&document.fonts.ready){document.fonts.ready.then(function(){shown=false;to(cur);});}to(cur);window.addEventListener('resize',function(){shown=false;to(cur);});}
    }
    group(document.querySelector('.site-header .nav'),'a');
    group(document.querySelector('.site-header .hdr-actions'),'.lang,.hdr-contact');
  })();
  // Buttons: wrap the label so the button and its text can spring separately
  document.querySelectorAll('.btn:not(.hdr-contact)').forEach(function(b){
    if(b.querySelector(':scope>.bt'))return;var w=document.createElement('span');w.className='bt';while(b.firstChild)w.appendChild(b.firstChild);b.appendChild(w);
  });
  // Pricing: remember the package and term someone clicked, so the start page opens on it
  document.querySelectorAll('[data-pick]').forEach(function(a){a.addEventListener('click',function(){try{sessionStorage.setItem('nxeo-pkg',a.getAttribute('data-pick'));var t=document.querySelector('[data-price][aria-pressed="true"]');sessionStorage.setItem('nxeo-term',t&&t.getAttribute('data-price')==='fp'?'year':'month');}catch(e){}});});
  function closeMenu(){mnav.classList.remove('is-open');}

  // In page jumps; links to a section on another page are plain links
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-jump],[data-link-jump]');if(!a)return;
    var href=a.getAttribute('href'),i=href.indexOf('#');if(i<0)return;
    var t=document.getElementById(href.slice(i+1));if(!t)return;
    e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});history.replaceState(null,'',href.slice(i));
  });

  document.getElementById('burger').addEventListener('click',function(){mnav.classList.add('is-open');});
  document.getElementById('mclose').addEventListener('click',closeMenu);

  // Language select in footer
  var ls=document.getElementById('langsel');
  if(ls)ls.addEventListener('change',function(){location.href=ls.value;});

  // Sliding thumb for segmented controls (pricing toggle, value switch)
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function placeThumb(c,animate){
    var on=c.querySelector('button[aria-pressed="true"],button[aria-selected="true"]');var th=c.querySelector('.thumb');if(!on||!th)return;
    var cr=c.getBoundingClientRect(),br=on.getBoundingClientRect();
    if(!animate){th.style.transition='none';}
    th.style.width=br.width+'px';th.style.transform='translateX('+(br.left-cr.left-c.clientLeft)+'px)';if(c.classList.contains('tabs')||c.classList.contains('faq-tabs')){th.style.top=(br.top-cr.top-c.clientTop)+'px';th.style.height=br.height+'px';}
    if(!animate){void th.offsetWidth;th.style.transition='';}
  }
  var segs=Array.prototype.slice.call(document.querySelectorAll('.toggle,.seg,.demo .tabs,.chat .tabs,.faq-tabs'));
  segs.forEach(function(c){
    var th=document.createElement('i');th.className='thumb';th.setAttribute('aria-hidden','true');c.insertBefore(th,c.firstChild);c.classList.add('has-thumb');
    placeThumb(c,false);
  });
  window.addEventListener('resize',function(){segs.forEach(function(c){placeThumb(c,false);});});

  // Hero demo tabs (blur masked crossfade)
  document.querySelectorAll('[data-demo]').forEach(function(t){
    t.addEventListener('click',function(){
      var k=t.getAttribute('data-demo');
      if(t.getAttribute('aria-selected')==='true')return;
      document.querySelectorAll('[data-demo]').forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false');});
      placeThumb(t.parentNode,true);
      var panes=document.querySelector('.demo .panes, .chat .panes');
      panes.classList.add('is-switching');
      setTimeout(function(){
        document.querySelectorAll('[data-demo-pane]').forEach(function(p){p.classList.toggle('is-on',p.getAttribute('data-demo-pane')===k);});
        var sc=document.querySelector('[data-demo-score]');if(sc)sc.innerHTML=k==='after'?'Presence score <b>74</b><span class="d">↑ +62</span>':'Presence score <b>12</b>';
        panes.classList.remove('is-switching');
      },260);
    });
  });

  // Channel tabs
  document.querySelectorAll('[data-chan]').forEach(function(t){
    t.addEventListener('click',function(){
      var k=t.getAttribute('data-chan');
      document.querySelectorAll('[data-chan]').forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false');});
      document.querySelectorAll('[data-chan-pane]').forEach(function(p){p.classList.toggle('is-on',p.getAttribute('data-chan-pane')===k);});
    });
  });

  // Value toggle
  document.querySelectorAll('[data-val]').forEach(function(b){
    b.addEventListener('click',function(){
      var k=b.getAttribute('data-val');
      if(b.getAttribute('aria-pressed')==='true')return;
      document.querySelectorAll('[data-val]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      placeThumb(b.parentNode,true);
      var g=document.querySelector('.vgrid');g.classList.add('is-switching');
      setTimeout(function(){
        g.querySelectorAll('.s').forEach(function(s){
          var txt=s.getAttribute('data-'+k);
          s.innerHTML=(k==='nxeo'?'<i class="ok">✓</i>':'<i class="no">✕</i>')+'<span>'+txt+'</span>';
        });
        g.classList.remove('is-switching');
      },140);
    });
  });

  // Pricing toggle: thumb glides, the amounts count to their new value
  var dec=document.documentElement.lang==='nl'?',':'.';
  function money(v,frac){return '€'+(frac?v.toFixed(2).replace('.',dec):String(Math.round(v)));}
  function countTo(el,to,dur){
    var from=parseFloat(el.textContent.replace(/[^\d.,]/g,'').replace(',','.'))||0;var frac=Math.abs(to-Math.round(to))>0.001;
    if(from===to||reduce){el.textContent=money(to,frac);return;}
    var t0=performance.now();
    function frame(now){var p=Math.min(1,(now-t0)/dur);var e=1-Math.pow(1-p,4);el.textContent=money(from+(to-from)*e,frac);if(p<1)requestAnimationFrame(frame);}
    requestAnimationFrame(frame);
  }
  document.querySelectorAll('[data-price]').forEach(function(b){
    b.addEventListener('click',function(){
      if(b.getAttribute('aria-pressed')==='true')return;
      var fp=b.getAttribute('data-price')==='fp';
      document.querySelectorAll('[data-price]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      placeThumb(b.parentNode,true);
      document.querySelectorAll('[data-n]').forEach(function(s){countTo(s,parseFloat((fp?s.getAttribute('data-f'):s.getAttribute('data-n')).replace(',','.')),640);});
      document.querySelectorAll('[data-fpnote]').forEach(function(n){n.textContent=fp?(n.getAttribute('data-ynote')||''):'';});
    });
  });

  // Field messages in our own words and style, instead of the browser's
  var NL=document.documentElement.lang==='nl';
  var VMSG=NL?{name:'Vul je naam in.',company:'Vul je bedrijfsnaam in.',site:'Vul je website in.',siteBad:'Dit lijkt geen website. Probeer bijvoorbeeld jouwwebsite.nl.',email:'Vul je e-mailadres in.',emailBad:'Dit e-mailadres klopt niet helemaal.',any:'Vul dit veld in.'}
    :{name:'Enter your name.',company:'Enter your company name.',site:'Enter your website.',siteBad:'This does not look like a website. Try yourwebsite.com.',email:'Enter your email address.',emailBad:'This email address is not quite right.',any:'Fill in this field.'};
  function vMsg(f){var v=f.value.trim(),n=f.name;
    if(!v)return f.required?(VMSG[n]||VMSG.any):'';
    if(n==='site'&&!/^(https?:\/\/)?[^\s.\/]+(\.[^\s.\/]+)+(\/\S*)?$/i.test(v))return VMSG.siteBad;
    if(n==='email'&&!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v))return VMSG.emailBad;
    return '';}
  function vBox(f){return f.closest('.combo')||f.parentNode;}
  function vClear(f){var b=vBox(f);b.classList.remove('is-err');f.removeAttribute('aria-invalid');var e=b.classList.contains('combo')?b.nextElementSibling:b.querySelector('.f-err');if(e&&e.classList.contains('f-err'))e.remove();}
  function vCheck(f,focus){vClear(f);var m=vMsg(f);if(!m)return true;
    var b=vBox(f);b.classList.add('is-err');f.setAttribute('aria-invalid','true');
    var e=document.createElement('p');e.className='f-err';e.setAttribute('role','alert');e.textContent=m;
    if(b.classList.contains('combo')){b.parentNode.insertBefore(e,b.nextSibling);}else{b.appendChild(e);}
    if(!f.dataset.v){f.dataset.v='1';f.addEventListener('input',function(){if(f.getAttribute('aria-invalid'))vCheck(f,false);});}
    if(focus)f.focus();return false;}
  function vForm(form){var ok=true,first=null;Array.prototype.forEach.call(form.querySelectorAll('input:not([type=hidden]):not([type=radio]),textarea'),function(f){f.value=f.value.trim();if(!vCheck(f,false)){ok=false;if(!first)first=f;}});if(first)first.focus();return ok;}

  // Versturen naar /api/lead. Lukt het niet, dan zeggen we dat eerlijk en blijft het formulier staan.
  function sendLead(form,type,extra,done){
    var btn=form.querySelector('button[type=submit]');if(btn&&btn.disabled)return;
    var old=form.querySelector('.f-send');if(old)old.remove();
    var data={type:type,lang:(document.documentElement.lang||'nl').slice(0,2),page:location.pathname};
    Array.prototype.forEach.call(form.elements,function(el){if(!el.name||el.type==='submit')return;if((el.type==='radio'||el.type==='checkbox')&&!el.checked)return;data[el.name]=el.value;});
    for(var k in extra){data[k]=extra[k];}
    if(btn){btn.disabled=true;btn.classList.add('is-busy');}
    var fail=function(){
      if(btn){btn.disabled=false;btn.classList.remove('is-busy');}
      var p=document.createElement('p');p.className='f-err f-send';p.setAttribute('role','alert');
      p.innerHTML='<span>'+(data.lang==='en'?'Sending did not work just now. Please email us at <a href="mailto:sales@nxeo.io">sales@nxeo.io</a>.':'Versturen lukt nu niet. Mail ons op <a href="mailto:sales@nxeo.io">sales@nxeo.io</a>.')+'</span>';
      (btn&&btn.parentNode===form?form:(btn?btn.parentNode:form)).appendChild(p);
    };
    fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.ok?r.json():Promise.reject();})
      .then(function(j){if(!j||!j.ok)return Promise.reject();if(btn){btn.disabled=false;btn.classList.remove('is-busy');}try{if(window.gtag)gtag('event','generate_lead',{form_type:type});}catch(e){}done();})
      .catch(fail);
  }

  // Call request form
  var sf=document.getElementById('form-sales');
  if(sf)sf.addEventListener('submit',function(e){
    e.preventDefault();
    if(!vForm(sf))return;
    sendLead(sf,document.getElementById('page-meekijken')?'doorloop':'gesprek',{},function(){
    var d=document.querySelector('[data-sl-done]');
    var first=sf.elements.name.value.split(/\s+/)[0];var h=d.querySelector('[data-sw="hello"]');h.textContent=h.getAttribute('data-hello')+(first?', '+first:'');
    d.querySelector('[data-sw="email"]').textContent=sf.elements.email.value;
    var sec=sf.closest('.so-sec');sf.hidden=true;sec.querySelector('.so-head').hidden=true;d.hidden=false;sec.classList.add('is-done');window.scrollTo(0,0);
    });
  });

  // Rotating AI names in the hero headline
  var rot=document.querySelector('.rot');
  if(rot&&!reduce){
    var items=Array.prototype.slice.call(rot.querySelectorAll('.rot-item')),ri=0;
    function fit(it){rot.style.width=it.getBoundingClientRect().width+'px';}
    if(rot.classList.contains('rot-inline')){fit(items[0]);window.addEventListener('resize',function(){rot.style.width='';fit(items[ri]);});}
    setInterval(function(){
      var cur=items[ri];ri=(ri+1)%items.length;var nxt=items[ri];
      if(rot.classList.contains('rot-inline')){rot.style.width='';var w=nxt.getBoundingClientRect().width;rot.style.width=cur.getBoundingClientRect().width+'px';void rot.offsetWidth;rot.style.width=w+'px';}
      cur.classList.remove('is-on');cur.classList.add('is-out');
      nxt.classList.remove('is-out');nxt.classList.add('is-on');
      setTimeout(function(){cur.classList.remove('is-out');},700);
    },2600);
  }

  // Baseline: any website form opens the dialog that asks for the email
  var nm=document.getElementById('nulmodal');
  if(nm){
    var nmf=document.getElementById('form-nul'),nmok=nm.querySelector('[data-nm-ok]'),nmSite=nm.querySelector('[data-nm-site]');
    function openNm(site){
      nmf.hidden=false;nmok.hidden=true;nmf.elements.site.value=site;nmSite.textContent=site.replace(/^https?:\/\//,'').replace(/\/$/,'');
      var y=window.scrollY;document.documentElement.classList.add('nm-open');
      if(typeof nm.showModal==='function'){nm.showModal();}else{nm.setAttribute('open','');}
      window.scrollTo(0,y);
      setTimeout(function(){nmf.elements.email.focus({preventScroll:true});window.scrollTo(0,y);},reduce?0:380);
    }
    document.querySelectorAll('form[data-baseline]').forEach(function(f){
      f.addEventListener('submit',function(e){
        e.preventDefault();
        var inp=f.querySelector('input[name=site]');
        var v=inp.value.trim();if(v&&!/^https?:\/\//i.test(v)){inp.value='https://'+v;}
        if(!vCheck(inp,true))return;
        openNm(inp.value.trim());
      });
    });
    nmf.addEventListener('submit',function(e){
      e.preventDefault();
      if(!vForm(nmf))return;
      sendLead(nmf,'nulmeting',{},function(){
      nmf.hidden=true;nmok.hidden=false;
      setTimeout(function(){if(nm.open)nm.close();},2600);
      });
    });
    nm.addEventListener('click',function(e){if(e.target===nm)nm.close();});
    nm.addEventListener('close',function(){document.documentElement.classList.remove('nm-open');document.querySelectorAll('form[data-baseline] input[name=site]').forEach(function(i){if(!nmok.hidden)i.value='';});});
  }

  // Start: one page order form with a live summary
  var so=document.getElementById('form-start');
  if(so){
    var soOut={};so.querySelectorAll('[data-so]').forEach(function(d){soOut[d.getAttribute('data-so')]=d;});
    var thou=function(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,dec===','?'.':',');};
    var soSync=function(){
      var p=so.querySelector('input[name=pkg]:checked'),y=so.querySelector('input[name=term]:checked').value==='year';
      var m=parseInt(p.getAttribute('data-price'),10);
      soOut.pkg.textContent=p.value;soOut.term.textContent=so.getAttribute(y?'data-tyr':'data-tmo');
      var sl=so.querySelector('[data-so-save-l]');sl.hidden=!y;soOut.save.hidden=!y;soOut.save.textContent='€'+m;soOut.price.textContent=y?'€'+thou(m*11)+so.getAttribute('data-pyr'):'€'+m+so.getAttribute('data-pmo');
      so.querySelectorAll('.so-plan').forEach(function(l){var i=l.querySelector('input'),v=parseInt(i.getAttribute('data-price'),10);l.querySelector('[data-so-price]').textContent=money(y?v*11/12:v,y);});
    };
    try{var pk=sessionStorage.getItem('nxeo-pkg'),tm=sessionStorage.getItem('nxeo-term');
      if(pk){var r=so.querySelector('input[name=pkg][value="'+pk+'"]');if(r)r.checked=true;}
      if(tm){var r2=so.querySelector('input[name=term][value="'+tm+'"]');if(r2)r2.checked=true;}}catch(e){}
    so.addEventListener('change',soSync);soSync();
    so.addEventListener('submit',function(e){
      e.preventDefault();
      var site=so.elements.site;site.value=site.value.trim();
      if(!vForm(so))return;
      sendLead(so,'start',{pkg:soOut.pkg.textContent,term:soOut.term.textContent,price:soOut.price.textContent},function(){
      var d=document.querySelector('[data-so-done]');
      var w=function(k){return d.querySelector('[data-won="'+k+'"]');};
      var first=so.elements.name.value.trim().split(/\s+/)[0];var h=w('hello');h.textContent=h.getAttribute('data-hello')+(first?', '+first:'');
      w('pkg').textContent=soOut.pkg.textContent;w('pkg2').textContent=soOut.pkg.textContent;w('term').textContent=soOut.term.textContent;w('price').textContent=soOut.price.textContent;w('email').textContent=so.elements.email.value.trim();
      so.hidden=true;document.querySelector('.so-head').hidden=true;d.hidden=false;document.querySelector('.so-sec').classList.add('is-done');window.scrollTo(0,0);
      });
    });
  }

  // Blog: filter by category
  document.querySelectorAll('[data-bcat]').forEach(function(b){
    b.addEventListener('click',function(){
      var k=b.getAttribute('data-bcat');
      document.querySelectorAll('[data-bcat]').forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false');});
      placeThumb(b.parentNode,true);
      var grid=document.querySelector('.bl-grid');grid.classList.toggle('is-filtered',!!k);
      grid.querySelectorAll('.bp').forEach(function(a){a.hidden=!!k&&a.getAttribute('data-cat')!==k;});
    });
  });

  // Article: reading progress and the active item in the table of contents
  (function(){
    var body=document.querySelector('.ar-body');if(!body)return;
    var bar=document.querySelector('.ar-bar i'),links=document.querySelectorAll('.ar-toc a'),heads=body.querySelectorAll('h2[id]'),tick=false;
    function upd(){tick=false;var r=body.getBoundingClientRect(),vh=window.innerHeight;
      var p=Math.min(1,Math.max(0,(vh*0.3-r.top)/(r.height-vh*0.4)));if(bar)bar.style.transform='scaleX('+p+')';
      var cur=-1;for(var i=0;i<heads.length;i++){if(heads[i].getBoundingClientRect().top<140)cur=i;}
      for(var k=0;k<links.length;k++){links[k].classList.toggle('on',k===cur);}}
    function q(){if(!tick){tick=true;requestAnimationFrame(upd);}}
    upd();window.addEventListener('scroll',q,{passive:true});window.addEventListener('resize',q);
    Array.prototype.forEach.call(links,function(a){a.addEventListener('click',function(e){var h=document.getElementById(a.getAttribute('href').slice(1));if(!h)return;e.preventDefault();h.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});history.replaceState(null,'',a.getAttribute('href'));});});
  })();

  // FAQ topic tabs
  document.querySelectorAll('[data-faqtab]').forEach(function(b){
    b.addEventListener('click',function(){
      var k=b.getAttribute('data-faqtab');
      document.querySelectorAll('[data-faqtab]').forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false');});
      placeThumb(b.parentNode,true);
      document.querySelectorAll('.faq-list .faq-group').forEach(function(g){g.classList.toggle('is-on',g.id===k);});
    });
  });

  // FAQ accordion: one open at a time per list, the others glide shut
  (function(){
    var EASE='cubic-bezier(.32,.72,0,1)';
    function shut(d){var body=d.querySelector('.body');if(!d.open||d.dataset.busy)return;
      if(reduce||!body||!body.animate){d.open=false;return;}
      d.dataset.busy='1';var h=body.offsetHeight;
      body.animate([{height:h+'px',opacity:1},{height:'0px',opacity:0}],{duration:480,easing:EASE}).onfinish=function(){d.open=false;delete d.dataset.busy;};}
    function show(d){var body=d.querySelector('.body');
      if(reduce||!body.animate){d.open=true;return;}
      d.dataset.busy='1';d.open=true;var h=body.offsetHeight;
      body.animate([{height:'0px',opacity:0},{height:h+'px',opacity:1}],{duration:620,easing:EASE}).onfinish=function(){delete d.dataset.busy;};}
    document.querySelectorAll('.faq details').forEach(function(d){
      var s=d.querySelector('summary');
      var body=document.createElement('div');body.className='body';
      while(s.nextSibling)body.appendChild(s.nextSibling);
      d.appendChild(body);
      s.addEventListener('click',function(e){
        e.preventDefault();
        if(d.dataset.busy)return;
        if(d.open){shut(d);return;}
        var box=d.parentNode;
        Array.prototype.forEach.call(box.children,function(o){if(o!==d&&o.tagName==='DETAILS')shut(o);});
        show(d);
      });
    });
  })();

  // Scroll reveal: only elements below the first viewport are hidden, so the first frame is complete
  var io=null;
  function setupReveal(){
    if(reduce||!('IntersectionObserver' in window))return;
    if(io)io.disconnect();
    io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
    },{rootMargin:'0px 0px -8% 0px',threshold:.05});
    var vh=window.innerHeight;
    document.querySelectorAll('main [data-reveal]').forEach(function(el){
      el.classList.remove('in');
      var r=el.getBoundingClientRect();
      if(r.top>vh){el.classList.add('pre');io.observe(el);}else{el.classList.remove('pre');}
    });
  }
  setupReveal();

  // Cookie bar
  var ck=document.getElementById('cookie');
  // Google Analytics: wordt pas geladen nadat iemand cookies accepteert
  var gaOn=false;
  function ga(){
    if(gaOn||!/(^|\.)nxeo\.io$/.test(location.hostname))return;gaOn=true;
    window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};
    gtag('js',new Date());gtag('config','G-GFLTYYVEXP',{anonymize_ip:true});
    var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-GFLTYYVEXP';document.head.appendChild(s);
  }
  try{var cv=localStorage.getItem('nxeo-cookie');if(cv)ck.hidden=true;if(cv==='yes')ga();}catch(err){}
  ck.addEventListener('click',function(e){
    var b=e.target.closest('[data-cookie]');if(!b)return;
    try{localStorage.setItem('nxeo-cookie',b.getAttribute('data-cookie'));}catch(err){}
    if(b.getAttribute('data-cookie')==='yes')ga();
    ck.classList.add('is-leaving');setTimeout(function(){ck.hidden=true;},160);
  });
})();
