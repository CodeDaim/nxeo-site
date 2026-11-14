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

  // Call request form
  var sf=document.getElementById('form-sales');
  if(sf)sf.addEventListener('submit',function(e){
    e.preventDefault();
    var f=sf.querySelectorAll('[required]');for(var k=0;k<f.length;k++){f[k].value=f[k].value.trim();if(!f[k].checkValidity()){f[k].reportValidity();return;}}
    var d=document.querySelector('[data-sl-done]');
    var first=sf.elements.name.value.split(/\s+/)[0];var h=d.querySelector('[data-sw="hello"]');h.textContent=h.getAttribute('data-hello')+(first?', '+first:'');
    d.querySelector('[data-sw="email"]').textContent=sf.elements.email.value;
    sf.hidden=true;document.querySelector('#page-sales .so-head').hidden=true;d.hidden=false;document.querySelector('#page-sales .so-sec').classList.add('is-done');window.scrollTo(0,0);
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
        if(!inp.checkValidity()){inp.reportValidity();return;}
        openNm(inp.value.trim());
      });
    });
    nmf.addEventListener('submit',function(e){
      e.preventDefault();
      if(!nmf.checkValidity()){nmf.reportValidity();return;}
      nmf.hidden=true;nmok.hidden=false;
      setTimeout(function(){if(nm.open)nm.close();},2600);
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
      soOut.price.textContent=y?'€'+thou(m*11)+so.getAttribute('data-pyr'):'€'+m+so.getAttribute('data-pmo');
      so.querySelectorAll('.so-plan').forEach(function(l){var i=l.querySelector('input'),v=parseInt(i.getAttribute('data-price'),10);l.querySelector('[data-so-price]').textContent=money(y?v*11/12:v,y);});
    };
    so.addEventListener('change',soSync);soSync();
    so.addEventListener('submit',function(e){
      e.preventDefault();
      var site=so.elements.site;site.value=site.value.trim();
      var f=so.querySelectorAll('input[required]');for(var k=0;k<f.length;k++){if(!f[k].checkValidity()){f[k].reportValidity();return;}}
      var d=document.querySelector('[data-so-done]');
      var w=function(k){return d.querySelector('[data-won="'+k+'"]');};
      var first=so.elements.name.value.trim().split(/\s+/)[0];var h=w('hello');h.textContent=h.getAttribute('data-hello')+(first?', '+first:'');
      w('pkg').textContent=soOut.pkg.textContent;w('pkg2').textContent=soOut.pkg.textContent;w('term').textContent=soOut.term.textContent;w('price').textContent=soOut.price.textContent;w('email').textContent=so.elements.email.value.trim();
      so.hidden=true;document.querySelector('.so-head').hidden=true;d.hidden=false;document.querySelector('.so-sec').classList.add('is-done');window.scrollTo(0,0);
    });
  }

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
  try{if(localStorage.getItem('nxeo-cookie'))ck.hidden=true;}catch(err){}
  ck.addEventListener('click',function(e){
    var b=e.target.closest('[data-cookie]');if(!b)return;
    try{localStorage.setItem('nxeo-cookie',b.getAttribute('data-cookie'));}catch(err){}
    ck.classList.add('is-leaving');setTimeout(function(){ck.hidden=true;},160);
  });
})();
