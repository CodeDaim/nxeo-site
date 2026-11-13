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
      var cur=box.querySelector('a[aria-current]'),shown=false;
      function to(a){if(!a){pill.classList.remove('is-on');shown=false;return;}
        var x=a.offsetLeft,w=a.offsetWidth;
        if(!shown){pill.style.transition='opacity 260ms ease';pill.style.transform='translateX('+x+'px)';pill.style.width=w+'px';void pill.offsetWidth;pill.style.transition='';}
        else{pill.style.transform='translateX('+x+'px)';pill.style.width=w+'px';}
        pill.classList.add('is-on');shown=true;}
      box.querySelectorAll('a').forEach(function(a){var on=a.matches(sel);a.addEventListener('mouseenter',function(){to(on?a:cur);});a.addEventListener('focus',function(){to(on?a:cur);});});
      box.addEventListener('mouseleave',function(){to(cur);});box.addEventListener('focusout',function(e){if(!box.contains(e.relatedTarget))to(cur);});
      if(cur){if(document.fonts&&document.fonts.ready){document.fonts.ready.then(function(){shown=false;to(cur);});}to(cur);window.addEventListener('resize',function(){shown=false;to(cur);});}
    }
    group(document.querySelector('.site-header .nav'),'a');
    group(document.querySelector('.site-header .hdr-actions'),'.lang,.hdr-contact');
  })();
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

  // Sales form
  var sf=document.getElementById('form-sales');
  if(sf)sf.addEventListener('submit',function(e){
    e.preventDefault();
    if(!sf.checkValidity()){sf.reportValidity();return;}
    sf.querySelector('.form-body').hidden=true;sf.querySelector('[data-ok]').hidden=false;
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

  // Stepped founding partner form (multi field steps, live summary)
  var ff=document.getElementById('form-fp');
  if(ff){
  var qs=Array.prototype.slice.call(ff.querySelectorAll('.q'));
  var done=ff.querySelector('[data-done]');
  var prev=ff.querySelector('[data-prev]'),next=ff.querySelector('[data-next]'),sub=ff.querySelector('[data-submit]');
  var bars=ff.querySelectorAll('.steps-bar i');
  var i=0;
  function show(n){
    i=n;
    qs.forEach(function(q,k){q.classList.toggle('is-on',k===i);});
    bars.forEach(function(b,k){b.classList.toggle('done',k<i);b.classList.toggle('on',k===i);});
    prev.disabled=i===0;next.hidden=i===qs.length-1;sub.hidden=i!==qs.length-1;
    var f=qs[i].querySelector('input:not([type=radio]),textarea');if(f&&window.matchMedia('(hover:hover)').matches)f.focus();
  }
  function valid(){
    var fields=qs[i].querySelectorAll('input,textarea');
    for(var k=0;k<fields.length;k++){var f=fields[k];if(!f.checkValidity()){f.reportValidity();return false;}}
    return true;
  }
  next.addEventListener('click',function(){if(valid()&&i<qs.length-1)show(i+1);});
  prev.addEventListener('click',function(){if(i>0)show(i-1);});
  ff.addEventListener('keydown',function(e){
    if(e.key==='Enter'&&!e.shiftKey&&e.target.tagName!=='BUTTON'&&e.target.tagName!=='TEXTAREA'){e.preventDefault();if(i<qs.length-1){if(valid())show(i+1);}else ff.requestSubmit();}
  });
  ff.addEventListener('submit',function(e){
    e.preventDefault();if(!valid())return;
    ff.querySelector('.form-body').hidden=true;ff.querySelector('.steps-bar').hidden=true;done.hidden=false;
  });
  // live summary
  var outs={};document.querySelectorAll('#page-aanvraag [data-sum-out]').forEach(function(d){outs[d.getAttribute('data-sum-out')]=d;});
  function setSum(key,val){var d=outs[key];if(!d)return;if(val){d.textContent=val;}else{d.innerHTML='<i>'+d.getAttribute('data-empty')+'</i>';}}
  Object.keys(outs).forEach(function(k){outs[k].setAttribute('data-empty',outs[k].textContent);});
  function sumSector(){var s=ff.querySelector('[data-sum=sector]').value.trim(),r=ff.querySelector('[data-sum=region]').value.trim();setSum('sector',[s,r].filter(Boolean).join(', '));}
  ff.addEventListener('input',function(e){
    var k=e.target.getAttribute('data-sum');if(!k)return;
    if(k==='sector'||k==='region')sumSector();else setSum(k,e.target.value.trim());
  });
  function sumPrice(){
    var p=ff.querySelector('input[name=pkg]:checked'),tm=ff.querySelector('input[name=term]:checked');if(!p)return;
    var m=parseInt(p.getAttribute('data-price').replace(/\D/g,''),10),y=tm&&tm.getAttribute('data-term')==='year';
    var out=outs.price;if(!out)return;
    out.textContent=p.value+' · '+(y?money(m*11,false).replace(/\B(?=(\d{3})+(?!\d))/g,dec===','?'.':',')+(document.documentElement.lang==='nl'?' per jaar':' per year'):money(m,false)+(document.documentElement.lang==='nl'?' per maand':' per month'));
  }
  ff.addEventListener('change',function(e){var k=e.target.getAttribute('data-sum');if(e.target.type==='radio'&&e.target.checked&&k){setSum(k,e.target.value);sumPrice();}});
  show(0);

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

  // FAQ accordion (height has no transform equivalent; keep it short)
  document.querySelectorAll('.faq details').forEach(function(d){
    var s=d.querySelector('summary');
    var body=document.createElement('div');body.className='body';
    while(s.nextSibling)body.appendChild(s.nextSibling);
    d.appendChild(body);
    s.addEventListener('click',function(e){
      e.preventDefault();
      if(d.dataset.busy)return;
      if(reduce||!body.animate){d.open=!d.open;return;}
      d.dataset.busy='1';
      if(d.open){
        var h=body.offsetHeight;
        body.animate([{height:h+'px',opacity:1},{height:'0px',opacity:0}],{duration:360,easing:'cubic-bezier(.32,.72,0,1)'}).onfinish=function(){d.open=false;delete d.dataset.busy;};
      }else{
        d.open=true;
        var h2=body.offsetHeight;
        body.animate([{height:'0px',opacity:0},{height:h2+'px',opacity:1}],{duration:460,easing:'cubic-bezier(.32,.72,0,1)'}).onfinish=function(){delete d.dataset.busy;};
      }
    });
  });

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
