(function(){
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const root=document.documentElement, AR=root.lang==='ar';

/* ---------- menu + mega menu ---------- */
const nav=$('#nav'), mb=$('#menuBtn');
mb&&mb.addEventListener('click',()=>{const o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
$$('.mm-t').forEach(b=>b.addEventListener('click',e=>{
  e.stopPropagation();const li=b.closest('.has-mm');const o=!li.classList.contains('open');
  $$('.has-mm.open').forEach(x=>{if(x!==li){x.classList.remove('open');x.querySelector('.mm-t').setAttribute('aria-expanded','false')}});
  li.classList.toggle('open',o);b.setAttribute('aria-expanded',o);
}));
document.addEventListener('click',e=>{if(!e.target.closest('.has-mm')&&!nav.classList.contains('open'))$$('.has-mm.open').forEach(x=>{x.classList.remove('open');x.querySelector('.mm-t').setAttribute('aria-expanded','false')})});
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;
  const li=$('.has-mm.open')||(document.activeElement&&document.activeElement.closest('.has-mm'));
  if(li){li.classList.remove('open');li.querySelector('.mm-t').setAttribute('aria-expanded','false');document.activeElement.blur&&document.activeElement.blur()}});
$$('#nav a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');mb&&mb.setAttribute('aria-expanded','false')}));

/* ---------- gallery filters (#butterflies, #bees, #spiders, #other) ---------- */
const filters=$('#filters');
function applyFilter(k){
  if(!filters)return;
  if(!$$('#filters [data-f]').some(b=>b.dataset.f===k))k='all';
  $$('#filters [data-f]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.f===k));
  $$('.g-item').forEach(f=>f.hidden=!(k==='all'||f.dataset.cat===k));
}
if(filters){
  filters.addEventListener('click',e=>{const b=e.target.closest('[data-f]');if(!b)return;const k=b.dataset.f;
    applyFilter(k);try{history.replaceState(null,'',k==='all'?location.pathname:'#'+k)}catch(_){}});
  const sync=()=>applyFilter(location.hash.slice(1)||'all');
  window.addEventListener('hashchange',sync);sync();
}

/* ---------- lightbox ---------- */
const lb=$('#lb');let list=[],pos=0,lastFocus=null;
function show(){
  const b=list[pos],img=b.querySelector('img'),im=$('#lbImg');
  im.style.animation='none';im.offsetWidth;im.style.animation='';
  im.src=b.dataset.full;im.alt=img.alt;
  const cap=b.closest('figure').querySelector('figcaption');
  $('#lbLabel').innerHTML=cap?cap.innerHTML:'';
  $('#lbCount').textContent=String(pos+1).padStart(2,'0')+' / '+String(list.length).padStart(2,'0');
  const n=list[(pos+1)%list.length];if(n)new Image().src=n.dataset.full;
}
function openLB(btn){
  list=$$('.lb-open').filter(b=>!b.closest('[hidden]'));pos=Math.max(0,list.indexOf(btn));
  lastFocus=document.activeElement;lb.hidden=false;document.body.style.overflow='hidden';show();$('#lbClose').focus();
}
function closeLB(){lb.hidden=true;document.body.style.overflow='';lastFocus&&lastFocus.focus()}
const step=d=>{pos=(pos+d+list.length)%list.length;show()};
if(lb){
  document.addEventListener('click',e=>{const b=e.target.closest('.lb-open');if(b)openLB(b)});
  $('#lbClose').onclick=closeLB;$('#lbPrev').onclick=()=>step(-1);$('#lbNext').onclick=()=>step(1);
  document.addEventListener('keydown',e=>{if(lb.hidden)return;
    if(e.key==='Escape')closeLB();
    else if(e.key==='ArrowRight')step(AR?-1:1);
    else if(e.key==='ArrowLeft')step(AR?1:-1);
    else if(e.key==='Tab'){const f=[...lb.querySelectorAll('button')];const i=f.indexOf(document.activeElement);e.preventDefault();f[(i+(e.shiftKey?-1:1)+f.length)%f.length].focus()}
  });
  lb.addEventListener('click',e=>{if(e.target===lb||e.target.id==='lbStage')closeLB()});
  let sx=null;$('#lbStage').addEventListener('pointerdown',e=>{sx=e.clientX});
  $('#lbStage').addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx;sx=null;if(Math.abs(dx)>50)step((dx<0?1:-1)*(AR?-1:1))});
}

/* ---------- hero loupe ---------- */
const stage=$('#stage');
if(stage){
  const lens=$('#lens'),hero=$('#heroImg'),Z=2.5;
  lens.style.backgroundImage='url("'+hero.currentSrc+'")';
  hero.addEventListener('load',()=>lens.style.backgroundImage='url("'+hero.currentSrc+'")');
  const move=e=>{
    const r=stage.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;
    const nw=hero.naturalWidth||2200,nh=hero.naturalHeight||1375,s=Math.max(r.width/nw,r.height/nh);
    const op=getComputedStyle(hero).objectPosition.split(' ').map(v=>parseFloat(v)/100);
    const ox=(r.width-nw*s)*(isNaN(op[0])?.5:op[0]),oy=(r.height-nh*s)*(isNaN(op[1])?.5:op[1]),R=lens.offsetWidth/2;
    lens.style.left=x+'px';lens.style.top=y+'px';
    lens.style.backgroundSize=(nw*s*Z)+'px '+(nh*s*Z)+'px';
    lens.style.backgroundPosition=(R-(x-ox)*Z)+'px '+(R-(y-oy)*Z)+'px';
    lens.classList.add('on');
  };
  stage.addEventListener('pointermove',move);stage.addEventListener('pointerdown',move);
  stage.addEventListener('pointerleave',()=>lens.classList.remove('on'));
  stage.addEventListener('pointercancel',()=>lens.classList.remove('on'));
  stage.addEventListener('pointerup',e=>{if(e.pointerType!=='mouse')setTimeout(()=>lens.classList.remove('on'),900)});
}

/* ---------- copy ---------- */
function copyText(t,btn,target){
  const o=btn.innerHTML;
  const done=()=>{btn.textContent=AR?'تم النسخ':'Copied';setTimeout(()=>btn.innerHTML=o,1600)};
  const fallback=()=>{if(!target)return;const r=document.createRange();r.selectNodeContents(target);const s=getSelection();s.removeAllRanges();s.addRange(r)};
  try{navigator.clipboard.writeText(t).then(done,fallback)}catch(e){fallback()}
}
$$('[data-copy]').forEach(b=>b.addEventListener('click',()=>copyText(b.dataset.copy,b,b.parentElement.querySelector('.v'))));

/* ---------- inquiry form ---------- */
const form=$('#inq');
if(form){
  form.addEventListener('submit',e=>{
    e.preventDefault();const err=$('#err');
    const name=form.name.value.trim(),email=form.email.value.trim(),msg=form.message.value.trim(),topic=form.topic.value;
    let p='';
    if(!name)p=AR?'أضف اسمك لتعرف مريم من يراسلها.':'Add your name so Maryam knows who is writing.';
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))p=AR?'أدخل بريداً إلكترونياً صحيحاً لتصلك الإجابة.':'Enter a valid email address so you can get a reply.';
    else if(msg.length<10)p=AR?'أضف بعض التفاصيل في الرسالة.':'Add a few details to your message.';
    err.hidden=!p;err.textContent=p;if(p)return;
    const subject=topic+' · '+name;
    const body=(AR?'مرحباً مريم،':'Hello Maryam,')+'\n\n'+msg+'\n\n'+name+'\n'+email;
    $('#readyTxt').textContent=(AR?'الموضوع: ':'Subject: ')+subject+'\n\n'+body;
    $('#mailMsg').href='mailto:maryamaalali@live.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    $('#ready').hidden=false;$('#ready').scrollIntoView({block:'nearest',behavior:'smooth'});
  });
  $('#copyMsg').addEventListener('click',e=>copyText($('#readyTxt').textContent,e.currentTarget,$('#readyTxt')));
}

/* ---------- live content edited in the admin panel (only when Supabase is connected) ---------- */
if(window.MBM && MBM.live){
  const pre=AR?'../':'', src=u=>/^(https?:|blob:|data:)/.test(u)?u:pre+u;
  const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const tr=(o,k)=>AR?(o[k+'_ar']||o[k+'_en']):o[k+'_en'];
  MBM.settings().then(s=>{const c=s.contact;if(!c)return;
    const digits=(c.phone||'').replace(/[^\d]/g,''), shown=(c.phone||'').replace(/^\+?971\s?(\d{2})\s?(\d{3})\s?(\d{4})$/,'+971 $1 $2 $3');
    $$('a[href^="mailto:"]').forEach(a=>{if(a.id==='mailMsg')return;a.href='mailto:'+c.email;if(/@.+\./.test(a.textContent))a.textContent=c.email});
    $$('a[href^="https://wa.me/"]').forEach(a=>{if(digits){a.href='https://wa.me/'+digits;if(/^\+?\d[\d\s]+$/.test(a.textContent.trim()))a.textContent=shown}});
    $$('a[href*="instagram.com/"]').forEach(a=>{if(c.instagram){a.href='https://www.instagram.com/'+c.instagram+'/';if(a.textContent.trim().startsWith('@'))a.textContent='@'+c.instagram}});
    $$('[data-copy]').forEach(b=>{if(b.dataset.copy.includes('@'))b.dataset.copy=c.email;else if(digits)b.dataset.copy='+'+digits});
    $$('.mailbig').forEach(e=>e.textContent=c.email);
  }).catch(()=>{});
  const mas=$('#masonry');
  if(mas) MBM.gallery().then(rows=>{if(!rows.length)return;
    mas.innerHTML=rows.map((g,i)=>{const no=String(i+1).padStart(2,'0');
      return `<figure class="g-item" data-cat="${esc(g.category)}"><button class="lb-open" type="button" data-full="${esc(src(g.image_url))}" aria-label="${AR?'عرض الصورة: ':'View photograph: '}${esc(tr(g,'name'))}"><img src="${esc(src(g.thumb_url))}" alt="${esc(tr(g,'alt'))}" loading="lazy" decoding="async"></button><figcaption class="label"><span class="no">${AR?'رقم ':'No. '}${no}</span><span class="nm">${esc(tr(g,'name'))}</span><span class="tx${g.taxon_italic?' it':''}">${esc(g.taxon)}</span></figcaption></figure>`}).join('');
    $$('#filters [data-f]').forEach(b=>{const n=b.dataset.f==='all'?rows.length:rows.filter(r=>r.category===b.dataset.f).length;const sup=b.querySelector('sup');if(sup)sup.textContent=n});
    applyFilter(location.hash.slice(1)||'all');
  }).catch(()=>{});
  const fg=$('#faqGroups');
  if(fg) MBM.faqs().then(rows=>{if(!rows.length)return;const groups=[];
    rows.forEach(r=>{let g=groups.find(x=>x.k===r.group_en);if(!g)groups.push(g={k:r.group_en,t:tr(r,'group'),q:[]});g.q.push(r)});
    fg.innerHTML=groups.map(g=>`<section class="faq-group"><h2>${esc(g.t)}</h2><div class="faq-list">${g.q.map(q=>`<details><summary>${esc(tr(q,'q'))}</summary><div class="ans"><p>${esc(tr(q,'a'))}</p></div></details>`).join('')}</div></section>`).join('');
  }).catch(()=>{});
}
})();
