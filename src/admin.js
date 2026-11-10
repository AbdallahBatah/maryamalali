(function(){
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const A = MBM.admin;
const esc = s => String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const LOC='en-GB';
const fmtDate=(d,o={day:'numeric',month:'short',year:'numeric'})=>new Intl.DateTimeFormat(LOC,o).format(new Date(d+'T00:00:00'));
const fmtTime=t=>{if(!t)return'';const[h,m]=t.split(':');return new Intl.DateTimeFormat(LOC,{hour:'numeric',minute:'2-digit'}).format(new Date(2000,0,1,+h,+m))};
const fmtWhen=s=>new Intl.DateTimeFormat(LOC,{day:'numeric',month:'short',hour:'numeric',minute:'2-digit'}).format(new Date(s));
const money=n=>(+n).toLocaleString('en',{maximumFractionDigits:2});
const todayIso=MBM.iso(new Date());
const KINDS={macro_walk:'Macro walk',night_walk:'Night walk',kids_trip:"Children's trip",workshop:'Photography workshop',exhibition:'Exhibition'};
const CATS={butterflies:'Butterflies & moths',bees:'Bees & wasps',spiders:'Spiders',other:'Other insects'};

let trips=[], bookings=[], month=new Date(new Date().getFullYear(),new Date().getMonth(),1);
const view = { status:'all', trip:'upcoming', q:'' };

/* ---------- toast + drawer ---------- */
function toast(msg, bad){const t=$('#toast');t.textContent=msg;t.className='toast'+(bad?' bad':'');t.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(()=>t.hidden=true,3200)}
function openDrawer(html){const d=$('#drawer');$('#drawerBody').innerHTML=html;d.hidden=false;document.body.style.overflow='hidden';setTimeout(()=>{const f=d.querySelector('input,select,textarea,button:not(#drawerClose)');f&&f.focus()},50)}
function closeDrawer(){$('#drawer').hidden=true;document.body.style.overflow=''}
$('#drawerClose').onclick=closeDrawer;
$('#drawer').addEventListener('click',e=>{if(e.target.id==='drawer')closeDrawer()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('#drawer').hidden)closeDrawer()});
const errMsg = e => ({trip_has_bookings:'This trip has bookings. Hide it from the website instead of deleting it.'}[e.code]) ||
  (/foreign key|violates/.test(e.message||'')?'This trip has bookings. Hide it from the website instead of deleting it.':
  'Could not save. Check your connection and try again. ('+(e.message||e.code||'error')+')');

/* two-step delete button */
function armDelete(btn, run){btn.addEventListener('click',async()=>{if(btn.dataset.armed){btn.disabled=true;try{await run()}catch(e){toast(errMsg(e),1);btn.disabled=false}return}
  btn.dataset.armed='1';const o=btn.textContent;btn.textContent='Click again to delete';btn.classList.add('armed');setTimeout(()=>{delete btn.dataset.armed;btn.textContent=o;btn.classList.remove('armed')},4000)})}

const seatsTaken = id => bookings.filter(b=>b.trip_id===id&&b.status!=='cancelled').reduce((s,b)=>s+b.adults+b.children,0);
const tripOf = id => trips.find(t=>t.id===id);
const tripLabel = t => t ? `${t.title_en} · ${fmtDate(t.trip_date,{day:'numeric',month:'short'})} ${fmtTime(t.start_time)}` : 'Deleted trip';

/* ---------- routing ---------- */
const VIEWS=['overview','calendar','bookings','payment','contact','faq','gallery'];
async function route(){
  const v=VIEWS.includes(location.hash.slice(1))?location.hash.slice(1):'overview';
  $$('.a-nav a').forEach(a=>a.getAttribute('href')==='#'+v?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current'));
  $$('[data-view]').forEach(s=>s.hidden=s.dataset.view!==v);
  ({overview:renderOverview,calendar:renderCalendar,bookings:renderBookings,payment:renderPayment,contact:renderContact,faq:renderFaq,gallery:renderGallery})[v]();
}
async function refresh(){ [trips, bookings] = await Promise.all([A.trips(), A.bookings()]); $('#pendingBadge').textContent = bookings.filter(b=>b.status==='pending').length || ''; }

/* ---------- overview ---------- */
function renderOverview(){
  const up=trips.filter(t=>t.trip_date>=todayIso), pending=bookings.filter(b=>b.status==='pending');
  const next=up.filter(t=>t.published).slice(0,5);
  const people=bookings.filter(b=>b.status!=='cancelled'&&up.some(t=>t.id===b.trip_id)).reduce((s,b)=>s+b.adults+b.children,0);
  $('#ovTiles').innerHTML=`
    <a class="tile${pending.length?' attn':''}" href="#bookings" data-status="pending"><span>Bookings to check</span><b>${pending.length}</b><small>Pending payment confirmation</small></a>
    <a class="tile" href="#calendar"><span>Upcoming trips</span><b>${up.length}</b><small>${up.filter(t=>!t.published).length} hidden from the website</small></a>
    <div class="tile"><span>People booked</span><b>${people}</b><small>Across upcoming trips</small></div>`;
  $('#ovTrips').innerHTML = next.length ? next.map(t=>{const taken=seatsTaken(t.id),pct=Math.min(100,Math.round(taken/t.capacity*100));
    return `<button type="button" class="ov-trip" data-edit="${t.id}"><span class="ov-date">${fmtDate(t.trip_date,{day:'numeric',month:'short'})}<small>${fmtTime(t.start_time)}</small></span>
      <span class="ov-main"><b>${esc(t.title_en)}</b><span class="bar"><i style="width:${pct}%"></i></span><small>${taken} / ${t.capacity} booked</small></span></button>`}).join('')
    : `<p class="empty">No upcoming published trips. <a href="#calendar">Add one in the calendar.</a></p>`;
  $('#ovBookings').innerHTML = bookings.length ? bookingRows(bookings.slice(0,6)) : `<p class="empty">No bookings yet.</p>`;
}
document.addEventListener('click',e=>{const a=e.target.closest('[data-status]');if(a&&a.classList.contains('tile')){view.status=a.dataset.status}});

/* ---------- calendar ---------- */
function renderCalendar(){
  const y=month.getFullYear(),m=month.getMonth(),lead=(new Date(y,m,1).getDay()+6)%7,days=new Date(y,m+1,0).getDate();
  $('#acTitle').textContent=new Intl.DateTimeFormat(LOC,{month:'long',year:'numeric'}).format(month);
  let h=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map(d=>`<span class="ac-dow">${d}</span>`).join('');
  for(let i=0;i<lead;i++)h+='<span class="ac-cell pad"></span>';
  for(let d=1;d<=days;d++){
    const key=MBM.iso(new Date(y,m,d)), list=trips.filter(t=>t.trip_date===key);
    h+=`<div class="ac-cell${key<todayIso?' past':''}${key===todayIso?' today':''}"><div class="ac-top"><span>${d}</span>${key>=todayIso?`<button type="button" class="ac-add" data-new="${key}" aria-label="Add trip on ${fmtDate(key)}">+</button>`:''}</div>
      ${list.map(t=>`<button type="button" class="ac-trip k-${t.kind}${t.published?'':' draft'}" data-edit="${t.id}"><b>${fmtTime(t.start_time)}</b> ${esc(t.title_en)}<small>${seatsTaken(t.id)}/${t.capacity}${t.published?'':' · hidden'}</small></button>`).join('')}</div>`;
  }
  $('#acGrid').innerHTML=h;
  const inMonth=trips.filter(t=>{const d=new Date(t.trip_date+'T00:00:00');return d.getFullYear()===y&&d.getMonth()===m});
  $('#acList').innerHTML = inMonth.length ? `<table class="tbl"><thead><tr><th>Date</th><th>Trip</th><th>Price</th><th>Booked</th><th>Website</th></tr></thead><tbody>${inMonth.map(t=>`
    <tr data-edit="${t.id}" tabindex="0"><td>${fmtDate(t.trip_date,{weekday:'short',day:'numeric',month:'short'})} · ${fmtTime(t.start_time)}</td><td>${esc(t.title_en)}<small>${esc(t.location_en)}</small></td>
    <td class="num">${money(t.price_aed)} AED</td><td class="num">${seatsTaken(t.id)} / ${t.capacity}</td><td>${t.published?'<span class="pill ok">Visible</span>':'<span class="pill">Hidden</span>'}</td></tr>`).join('')}</tbody></table>`
    : `<p class="empty">No trips this month. Use + on a day or “New trip”.</p>`;
}
$('#acPrev').onclick=()=>{month=new Date(month.getFullYear(),month.getMonth()-1,1);renderCalendar()};
$('#acNext').onclick=()=>{month=new Date(month.getFullYear(),month.getMonth()+1,1);renderCalendar()};
$('#acNew').onclick=()=>tripForm(null, todayIso);
document.addEventListener('click',e=>{
  const ed=e.target.closest('[data-edit]'); if(ed){tripForm(tripOf(ed.dataset.edit));return}
  const nw=e.target.closest('[data-new]'); if(nw){tripForm(null,nw.dataset.new)}
});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches('tr[data-edit],tr[data-booking]'))e.target.click()});

const TEMPLATE = {kind:'macro_walk', title_en:'Macro Walk', title_ar:'جولة ماكرو', start_time:'09:00', end_time:'11:30', location_en:'Mushrif Park, Dubai', location_ar:'حديقة مشرف، دبي',
  price_aed:150, child_price_aed:null, capacity:15, map_url:'',
  description_en:'', description_ar:'',
  includes_en:["Macro photos for learning & discussion before the walk","Interactive exploration challenge during the walk","Drinks & snacks","Headlamps","Full trip guidance experience"],
  includes_ar:["صور ماكرو للتعلّم والنقاش قبل الجولة","تحدٍّ استكشافي تفاعلي خلال الجولة","مشروبات ووجبات خفيفة","مصابيح رأس","تجربة إرشاد كاملة طوال الرحلة"],
  rules_en:'I commit to respecting nature, keeping the area clean and following Mushrif Park rules, and I understand that each participant is responsible for their own safety during the walk.',
  rules_ar:'ألتزم باحترام الطبيعة والحفاظ على نظافة المكان واتباع أنظمة حديقة مشرف، وأدرك أن كل مشارك مسؤول عن سلامته الشخصية خلال الجولة.', published:true};

function tripForm(t, date){
  const isNew=!t; t = t || Object.assign({}, TEMPLATE, {trip_date:date});
  const taken = isNew?0:seatsTaken(t.id);
  const opt=Object.entries(KINDS).map(([k,v])=>`<option value="${k}"${t.kind===k?' selected':''}>${v}</option>`).join('');
  openDrawer(`
  <form id="tripForm" class="aform" novalidate>
    <p class="eyebrow">${isNew?'New trip':'Edit trip'}</p>
    <h2>${isNew?'Add a trip to the calendar':esc(t.title_en)}</h2>
    ${isNew?'':`<p class="muted small">${taken} of ${t.capacity} seats booked · <a href="#bookings" data-filter-trip="${t.id}">See bookings</a></p>`}
    <label class="switch"><input type="checkbox" name="published" ${t.published?'checked':''}><span>Visible on the website and open for booking</span></label>
    <div class="g2">
      <div class="field"><label for="t-kind">Type</label><select id="t-kind" name="kind">${opt}</select></div>
      <div class="field"><label for="t-cap">Seats (capacity)</label><input id="t-cap" name="capacity" type="number" min="1" value="${t.capacity}"></div>
    </div>
    <div class="g2">
      <div class="field"><label for="t-ten">Title (English)</label><input id="t-ten" name="title_en" value="${esc(t.title_en)}"></div>
      <div class="field" dir="rtl"><label for="t-tar">العنوان (عربي)</label><input id="t-tar" name="title_ar" value="${esc(t.title_ar)}"></div>
    </div>
    <div class="g3">
      <div class="field"><label for="t-date">Date</label><input id="t-date" name="trip_date" type="date" value="${t.trip_date}"></div>
      <div class="field"><label for="t-st">Starts</label><input id="t-st" name="start_time" type="time" value="${(t.start_time||'').slice(0,5)}"></div>
      <div class="field"><label for="t-et">Ends</label><input id="t-et" name="end_time" type="time" value="${(t.end_time||'').slice(0,5)}"></div>
    </div>
    <div class="g2">
      <div class="field"><label for="t-len">Location (English)</label><input id="t-len" name="location_en" value="${esc(t.location_en)}"></div>
      <div class="field" dir="rtl"><label for="t-lar">الموقع (عربي)</label><input id="t-lar" name="location_ar" value="${esc(t.location_ar)}"></div>
    </div>
    <div class="field"><label for="t-map">Map link (optional)</label><input id="t-map" name="map_url" type="url" value="${esc(t.map_url||'')}" placeholder="https://maps.google.com/…"></div>
    <div class="g2">
      <div class="field"><label for="t-pr">Price per person (AED)</label><input id="t-pr" name="price_aed" type="number" min="0" step="1" value="${t.price_aed}"></div>
      <div class="field"><label for="t-cp">Child price (AED, leave empty if same)</label><input id="t-cp" name="child_price_aed" type="number" min="0" step="1" value="${t.child_price_aed??''}"></div>
    </div>
    <div class="g2">
      <div class="field"><label for="t-den">Description (English)</label><textarea id="t-den" name="description_en" rows="3">${esc(t.description_en)}</textarea></div>
      <div class="field" dir="rtl"><label for="t-dar">الوصف (عربي)</label><textarea id="t-dar" name="description_ar" rows="3">${esc(t.description_ar)}</textarea></div>
    </div>
    <div class="g2">
      <div class="field"><label for="t-ien">What's included (one per line)</label><textarea id="t-ien" name="includes_en" rows="5">${esc((t.includes_en||[]).join('\n'))}</textarea></div>
      <div class="field" dir="rtl"><label for="t-iar">ما تشمله الرحلة (سطر لكل بند)</label><textarea id="t-iar" name="includes_ar" rows="5">${esc((t.includes_ar||[]).join('\n'))}</textarea></div>
    </div>
    <div class="g2">
      <div class="field"><label for="t-ren">Rules participants agree to</label><textarea id="t-ren" name="rules_en" rows="4">${esc(t.rules_en)}</textarea></div>
      <div class="field" dir="rtl"><label for="t-rar">التعليمات التي يوافق عليها المشارك</label><textarea id="t-rar" name="rules_ar" rows="4">${esc(t.rules_ar)}</textarea></div>
    </div>
    <p class="err" id="tErr" hidden></p>
    <div class="a-actions">
      <button class="btn solid" type="submit">${isNew?'Add trip':'Save changes'}</button>
      ${isNew?'':`<span class="dup"><input id="t-dup" type="date" aria-label="Duplicate to date" value="${t.trip_date}"><button class="btn" type="button" id="dupBtn">Duplicate to this date</button></span>
      <button class="btn" type="button" id="copyLink">Copy booking link</button>
      <button class="btn danger" type="button" id="delTrip">Delete</button>`}
    </div>
  </form>`);
  const f=$('#tripForm');
  const read=()=>({ id:t.id, kind:f.kind.value, title_en:f.title_en.value.trim(), title_ar:f.title_ar.value.trim(), trip_date:f.trip_date.value,
    start_time:f.start_time.value, end_time:f.end_time.value||null, location_en:f.location_en.value.trim(), location_ar:f.location_ar.value.trim(),
    map_url:f.map_url.value.trim()||null, price_aed:+f.price_aed.value||0, child_price_aed:f.child_price_aed.value===''?null:+f.child_price_aed.value,
    capacity:Math.max(1,+f.capacity.value||1), description_en:f.description_en.value.trim(), description_ar:f.description_ar.value.trim(),
    includes_en:f.includes_en.value.split('\n').map(s=>s.trim()).filter(Boolean), includes_ar:f.includes_ar.value.split('\n').map(s=>s.trim()).filter(Boolean),
    rules_en:f.rules_en.value.trim(), rules_ar:f.rules_ar.value.trim(), published:f.published.checked });
  const check=r=>{ if(!r.title_en) return 'Add an English title.'; if(!r.trip_date) return 'Choose a date.'; if(!r.start_time) return 'Add a start time.';
    if(!isNew && r.capacity<taken) return `Capacity can't be lower than the ${taken} seats already booked.`; return ''; };
  f.addEventListener('submit',async e=>{e.preventDefault();const r=read(),p=check(r);const er=$('#tErr');er.hidden=!p;er.textContent=p;if(p)return;
    try{await A.saveTrip(r);await refresh();closeDrawer();toast(isNew?'Trip added':'Trip saved');route()}catch(x){er.textContent=errMsg(x);er.hidden=false}});
  if(!isNew){
    $('#dupBtn').onclick=async()=>{const r=read();delete r.id;r.trip_date=$('#t-dup').value;if(!r.trip_date)return;
      try{await A.saveTrip(r);await refresh();closeDrawer();toast('Trip duplicated to '+fmtDate(r.trip_date));route()}catch(x){toast(errMsg(x),1)}};
    $('#copyLink').onclick=()=>{const u=new URL('book.html#trip-'+t.id, location.href).href;try{navigator.clipboard.writeText(u).then(()=>toast('Booking link copied'),()=>toast(u))}catch(_){toast(u)}};
    armDelete($('#delTrip'),async()=>{await A.deleteTrip(t.id);await refresh();closeDrawer();toast('Trip deleted');route()});
  }
}

/* ---------- bookings ---------- */
function bookingRows(list){
  return `<table class="tbl"><thead><tr><th>Ref</th><th>Received</th><th>Trip</th><th>Contact</th><th class="num">People</th><th class="num">Total</th><th>Status</th></tr></thead><tbody>${
    list.map(b=>`<tr data-booking="${b.id}" tabindex="0"><td class="mono">${esc(b.ref)}</td><td>${fmtWhen(b.created_at)}</td><td>${esc(tripLabel(tripOf(b.trip_id)))}</td>
    <td>${esc(b.contact_name)}<small dir="ltr">${esc(b.mobile)}</small></td><td class="num">${b.adults}A · ${b.children}C${b.allergies?' <span class="pill warn" title="Allergies">!</span>':''}</td>
    <td class="num">${money(b.total_aed)} AED</td><td><span class="pill ${b.status==='confirmed'?'ok':b.status==='cancelled'?'off':'warn'}">${b.status}</span></td></tr>`).join('')}</tbody></table>`;
}
function filtered(){
  return bookings.filter(b=>{
    const t=tripOf(b.trip_id);
    if(view.status!=='all'&&b.status!==view.status) return false;
    if(view.trip==='upcoming'&&!(t&&t.trip_date>=todayIso)) return false;
    if(view.trip!=='upcoming'&&view.trip!=='all'&&b.trip_id!==view.trip) return false;
    if(view.q){const q=view.q.toLowerCase();if(![b.ref,b.contact_name,b.mobile,b.email].join(' ').toLowerCase().includes(q))return false}
    return true;
  });
}
function renderBookings(){
  const opts=[['upcoming','Upcoming trips'],['all','All trips']].concat(trips.slice().reverse().map(t=>[t.id,tripLabel(t)]));
  $('#bkTrip').innerHTML=opts.map(([v,l])=>`<option value="${v}"${view.trip===v?' selected':''}>${esc(l)}</option>`).join('');
  $$('#bkStatus button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===view.status));
  $('#bkSearch').value=view.q;
  const list=filtered();
  const t=tripOf(view.trip);
  if(t){const act=bookings.filter(b=>b.trip_id===t.id&&b.status!=='cancelled');const ad=act.reduce((s,b)=>s+b.adults,0),ch=act.reduce((s,b)=>s+b.children,0);
    $('#bkRoster').innerHTML=`<b>${esc(t.title_en)}</b> · ${fmtDate(t.trip_date,{weekday:'long',day:'numeric',month:'long'})} · ${ad} adults, ${ch} children · ${Math.max(0,t.capacity-ad-ch)} seats left`;$('#bkRoster').hidden=false}
  else $('#bkRoster').hidden=true;
  $('#bkTable').innerHTML = list.length ? bookingRows(list) : `<p class="empty">No bookings match these filters.</p>`;
}
$('#bkTrip').onchange=e=>{view.trip=e.target.value;renderBookings()};
$('#bkStatus').addEventListener('click',e=>{const b=e.target.closest('[data-s]');if(b){view.status=b.dataset.s;renderBookings()}});
$('#bkSearch').addEventListener('input',e=>{view.q=e.target.value.trim();renderBookings()});
document.addEventListener('click',e=>{const a=e.target.closest('[data-filter-trip]');if(a){view.trip=a.dataset.filterTrip;view.status='all';closeDrawer()}});
document.addEventListener('click',e=>{const r=e.target.closest('[data-booking]');if(r)bookingDetail(bookings.find(b=>b.id===r.dataset.booking))});
$('#bkExport').onclick=()=>{
  const rows=[['Ref','Received','Trip','Trip date','Contact','Mobile','Email','Adults','Children','Participants','Allergies','Allergy details','Photo consent','Total AED','Status','Note']];
  filtered().forEach(b=>{const t=tripOf(b.trip_id);rows.push([b.ref,b.created_at,t?t.title_en:'',t?t.trip_date:'',b.contact_name,b.mobile,b.email,b.adults,b.children,
    (b.participants||[]).map(p=>p.type==='child'?`${p.name} (child, ${p.age}, parent ${p.parent_mobile})`:`${p.name} (adult)`).join('; '),
    b.allergies?'Yes':'No',b.allergy_details||'',b.photo_consent?'Yes':'No',b.total_aed,b.status,b.admin_note||''])});
  const csv='﻿'+rows.map(r=>r.map(v=>`"${String(v??'').replace(/"/g,'""')}"`).join(',')).join('\r\n');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='bookings-'+todayIso+'.csv';document.body.appendChild(a);a.click();a.remove();
};

async function bookingDetail(b){
  const t=tripOf(b.trip_id), wa=b.mobile.replace(/[^\d]/g,'');
  const ppl=(b.participants||[]).map((p,i)=>`<tr><td>${i+1}</td><td>${esc(p.name)}</td><td>${p.type==='child'?'Child':'Adult'}</td><td class="num">${p.type==='child'?esc(p.age):''}</td><td dir="ltr">${p.type==='child'?esc(p.parent_mobile):''}</td></tr>`).join('');
  openDrawer(`
    <p class="eyebrow">Booking ${esc(b.ref)}</p>
    <h2>${esc(b.contact_name)}</h2>
    <p class="muted small">${esc(tripLabel(t))} · received ${fmtWhen(b.created_at)} · ${b.lang==='ar'?'Arabic':'English'} form</p>
    <div class="statusbar" role="group" aria-label="Booking status">
      ${['pending','confirmed','cancelled'].map(s=>`<button type="button" class="btn${b.status===s?' solid':''}" data-set="${s}" aria-pressed="${b.status===s}">${s==='pending'?'Pending':s==='confirmed'?'Confirm payment':'Cancel booking'}</button>`).join('')}
    </div>
    <dl class="kv">
      <div><dt>Mobile</dt><dd dir="ltr">${esc(b.mobile)} · <a href="https://wa.me/${wa}" target="_blank" rel="noopener">WhatsApp</a></dd></div>
      <div><dt>Email</dt><dd>${esc(b.email)}</dd></div>
      <div><dt>Total</dt><dd>${money(b.total_aed)} AED · ${b.adults} adult${b.adults===1?'':'s'}, ${b.children} child${b.children===1?'':'ren'}</dd></div>
      <div><dt>Allergies</dt><dd>${b.allergies?`<span class="pill warn">Yes</span> ${esc(b.allergy_details)}`:'None'}</dd></div>
      <div><dt>Photo consent</dt><dd>${b.photo_consent?'Agrees to appear in photos':'<span class="pill warn">Does not agree</span> to appear in photos'}</dd></div>
      <div><dt>Rules</dt><dd>${b.rules_agreed?'Agreed':'Not agreed'}</dd></div>
    </dl>
    <h3 class="sub">Participants</h3>
    <table class="tbl compact"><thead><tr><th>#</th><th>Name</th><th>Type</th><th class="num">Age</th><th>Parent mobile</th></tr></thead><tbody>${ppl}</tbody></table>
    <h3 class="sub">Payment receipt</h3>
    <div id="receipt" class="receipt"><p class="muted small">Loading receipt…</p></div>
    <div class="field"><label for="b-note">Private note</label><textarea id="b-note" rows="3">${esc(b.admin_note||'')}</textarea></div>
    <div class="a-actions"><button class="btn" type="button" id="saveNote">Save note</button></div>`);
  $$('[data-set]').forEach(btn=>btn.onclick=async()=>{try{const r=await A.updateBooking(b.id,{status:btn.dataset.set});Object.assign(b,r);await refresh();toast('Booking marked '+btn.dataset.set);bookingDetail(b);route()}catch(x){toast(errMsg(x),1)}});
  $('#saveNote').onclick=async()=>{try{await A.updateBooking(b.id,{admin_note:$('#b-note').value});b.admin_note=$('#b-note').value;toast('Note saved')}catch(x){toast(errMsg(x),1)}};
  try{
    const u=await A.receiptUrl(b.receipt_path), box=$('#receipt');
    if(!u){box.innerHTML=`<p class="muted small">${b.example?'Example booking: no receipt file.':'Receipt file not available.'}</p>`;return}
    box.innerHTML = /\.pdf($|\?)/i.test(b.receipt_path) ? `<a class="btn" href="${esc(u)}" target="_blank" rel="noopener">Open PDF receipt</a>`
      : `<a href="${esc(u)}" target="_blank" rel="noopener"><img src="${esc(u)}" alt="Payment receipt uploaded by ${esc(b.contact_name)}"></a><a class="tlink" href="${esc(u)}" target="_blank" rel="noopener">Open full size</a>`;
  }catch(x){$('#receipt').innerHTML='<p class="err">Could not load the receipt.</p>'}
}

/* ---------- payment + contact ---------- */
async function settingsForm(sel, key, fields, extra){
  const s=await MBM.settings(), v=s[key]||{};
  $(sel).innerHTML = `<form class="aform narrow" id="f-${key}">${fields.map(([k,l,attrs])=>`<div class="field"${attrs&&attrs.includes('rtl')?' dir="rtl"':''}><label for="s-${key}-${k}">${l}</label>${
    attrs&&attrs.includes('area')?`<textarea id="s-${key}-${k}" name="${k}" rows="3">${esc(v[k]||'')}</textarea>`:`<input id="s-${key}-${k}" name="${k}" value="${esc(v[k]||'')}">`}</div>`).join('')}
    <div class="a-actions"><button class="btn solid" type="submit">Save</button></div></form>${extra||''}`;
  $('#f-'+key).addEventListener('submit',async e=>{e.preventDefault();const o={};fields.forEach(([k])=>o[k]=e.target[k].value.trim());
    try{await A.saveSetting(key,o);toast('Saved. The website shows the new details now.')}catch(x){toast(errMsg(x),1)}});
}
function renderPayment(){
  settingsForm('#payForm','bank',[['bank_name','Bank name'],['account_holder','Account holder'],['account_number','Account number'],['iban','IBAN'],['swift','SWIFT / BIC'],['currency','Currency']]);
  settingsForm('#noteForm','booking_note',[['en','Message at the top of the booking form (English)',['area']],['ar','الرسالة أعلى نموذج الحجز (عربي)',['area','rtl']]]);
}
function renderContact(){
  settingsForm('#contactForm','contact',[['email','Email'],['phone','Phone / WhatsApp (with country code)'],['instagram','Instagram username (without @)']]);
}

/* ---------- FAQ ---------- */
async function renderFaq(){
  const list=await A.list('faqs');
  $('#faqList').innerHTML = list.length ? list.map((q,i)=>`<div class="frow"><div class="frow-main"><small>${esc(q.group_en)}</small><b>${esc(q.q_en)}</b><span dir="rtl">${esc(q.q_ar)}</span></div>
    <div class="frow-act">${q.published?'':'<span class="pill">Hidden</span>'}<button type="button" class="ib" data-fmove="${q.id}" data-dir="-1" ${i===0?'disabled':''} aria-label="Move up">↑</button><button type="button" class="ib" data-fmove="${q.id}" data-dir="1" ${i===list.length-1?'disabled':''} aria-label="Move down">↓</button><button type="button" class="btn" data-fedit="${q.id}">Edit</button></div></div>`).join('')
    : `<p class="empty">No questions yet. ${MBM.live?'Run seed.sql to load the questions from the website, or add one.':'Add a question to see how it works.'}</p>`;
  $('#faqList').onclick=async e=>{
    const ed=e.target.closest('[data-fedit]'); if(ed){faqForm(list.find(q=>q.id===ed.dataset.fedit), list);return}
    const mv=e.target.closest('[data-fmove]'); if(mv){const i=list.findIndex(q=>q.id===mv.dataset.fmove),j=i+(+mv.dataset.dir);
      [list[i].sort,list[j].sort]=[j,i];list.forEach((q,k)=>{if(k!==i&&k!==j)q.sort=k});
      try{await Promise.all([A.save('faqs',{id:list[i].id,sort:list[i].sort}),A.save('faqs',{id:list[j].id,sort:list[j].sort})]);renderFaq()}catch(x){toast(errMsg(x),1)}}
  };
}
$('#faqNew').onclick=async()=>{const l=await A.list('faqs');faqForm(null,l)};
function faqForm(q,list){
  const isNew=!q; q=q||{group_en:list.length?list[list.length-1].group_en:'Trips and workshops',group_ar:list.length?list[list.length-1].group_ar:'الرحلات والورش',q_en:'',q_ar:'',a_en:'',a_ar:'',sort:list.length,published:true};
  openDrawer(`<form id="faqForm" class="aform" novalidate><p class="eyebrow">${isNew?'New question':'Edit question'}</p><h2>${isNew?'Add a question':esc(q.q_en)}</h2>
    <label class="switch"><input type="checkbox" name="published" ${q.published?'checked':''}><span>Show on the website</span></label>
    <div class="g2"><div class="field"><label for="q-ge">Section (English)</label><input id="q-ge" name="group_en" value="${esc(q.group_en)}"></div><div class="field" dir="rtl"><label for="q-ga">القسم (عربي)</label><input id="q-ga" name="group_ar" value="${esc(q.group_ar)}"></div></div>
    <div class="g2"><div class="field"><label for="q-qe">Question (English)</label><input id="q-qe" name="q_en" value="${esc(q.q_en)}"></div><div class="field" dir="rtl"><label for="q-qa">السؤال (عربي)</label><input id="q-qa" name="q_ar" value="${esc(q.q_ar)}"></div></div>
    <div class="g2"><div class="field"><label for="q-ae">Answer (English)</label><textarea id="q-ae" name="a_en" rows="6">${esc(q.a_en)}</textarea></div><div class="field" dir="rtl"><label for="q-aa">الإجابة (عربي)</label><textarea id="q-aa" name="a_ar" rows="6">${esc(q.a_ar)}</textarea></div></div>
    <p class="err" id="qErr" hidden></p>
    <div class="a-actions"><button class="btn solid" type="submit">${isNew?'Add question':'Save'}</button>${isNew?'':'<button class="btn danger" type="button" id="qDel">Delete</button>'}</div></form>`);
  const f=$('#faqForm');
  f.addEventListener('submit',async e=>{e.preventDefault();const r={id:q.id,sort:q.sort,published:f.published.checked};['group_en','group_ar','q_en','q_ar','a_en','a_ar'].forEach(k=>r[k]=f[k].value.trim());
    if(!r.q_en||!r.a_en||!r.q_ar||!r.a_ar){$('#qErr').textContent='Fill in the question and answer in both languages.';$('#qErr').hidden=false;return}
    try{await A.save('faqs',r);closeDrawer();toast('Question saved');renderFaq()}catch(x){$('#qErr').textContent=errMsg(x);$('#qErr').hidden=false}});
  if(!isNew) armDelete($('#qDel'),async()=>{await A.remove('faqs',q.id);closeDrawer();toast('Question deleted');renderFaq()});
}

/* ---------- gallery ---------- */
const siteUrl = u => /^(https?:|blob:|data:)/.test(u) ? u : u;  // admin.html sits at the site root
async function renderGallery(){
  const list=await A.list('gallery');
  $('#galGrid').innerHTML = list.length ? list.map((g,i)=>`<figure class="gcard${g.published?'':' draft'}"><img src="${esc(siteUrl(g.thumb_url))}" alt="${esc(g.alt_en)}" loading="lazy">
    <figcaption><b>${esc(g.name_en)}</b><small>${CATS[g.category]||g.category} · ${esc(g.taxon)}${g.published?'':' · hidden'}</small>
    <span class="gact"><button type="button" class="ib" data-gmove="${g.id}" data-dir="-1" ${i===0?'disabled':''} aria-label="Move earlier">←</button><button type="button" class="ib" data-gmove="${g.id}" data-dir="1" ${i===list.length-1?'disabled':''} aria-label="Move later">→</button><button type="button" class="btn" data-gedit="${g.id}">Edit</button></span></figcaption></figure>`).join('')
    : `<p class="empty">No photographs yet. ${MBM.live?'Run seed.sql to load the current gallery, or upload one.':'Upload a photograph to see how it works.'}</p>`;
  $('#galGrid').onclick=async e=>{
    const ed=e.target.closest('[data-gedit]'); if(ed){galForm(list.find(g=>g.id===ed.dataset.gedit),list);return}
    const mv=e.target.closest('[data-gmove]'); if(mv){const i=list.findIndex(g=>g.id===mv.dataset.gmove),j=i+(+mv.dataset.dir);
      try{await Promise.all([A.save('gallery',{id:list[i].id,sort:j}),A.save('gallery',{id:list[j].id,sort:i})]);renderGallery()}catch(x){toast(errMsg(x),1)}}
  };
}
$('#galNew').onclick=async()=>{const l=await A.list('gallery');galForm(null,l)};
function resize(file, max){return new Promise((res,rej)=>{const img=new Image();img.onload=()=>{const s=Math.min(1,max/Math.max(img.width,img.height));
  const c=document.createElement('canvas');c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);
  c.toBlob(b=>b?res(b):rej(new Error('resize_failed')),'image/jpeg',.85)};img.onerror=()=>rej(new Error('image_unreadable'));img.src=URL.createObjectURL(file)})}
function galForm(g,list){
  const isNew=!g; g=g||{name_en:'',name_ar:'',taxon:'',taxon_italic:false,category:'other',alt_en:'',alt_ar:'',sort:list.length,published:true,image_url:'',thumb_url:''};
  openDrawer(`<form id="galForm" class="aform" novalidate><p class="eyebrow">${isNew?'New photograph':'Edit photograph'}</p><h2>${isNew?'Upload a photograph':esc(g.name_en)}</h2>
    ${g.thumb_url?`<img class="gprev" src="${esc(siteUrl(g.thumb_url))}" alt="">`:''}
    <div class="field"><label for="g-file">${isNew?'Photograph (JPG or PNG)':'Replace photograph (optional)'}</label><input id="g-file" name="file" type="file" accept="image/jpeg,image/png,image/webp"></div>
    <label class="switch"><input type="checkbox" name="published" ${g.published?'checked':''}><span>Show in the gallery</span></label>
    <div class="g2"><div class="field"><label for="g-ne">Common name (English)</label><input id="g-ne" name="name_en" value="${esc(g.name_en)}"></div><div class="field" dir="rtl"><label for="g-na">الاسم الشائع (عربي)</label><input id="g-na" name="name_ar" value="${esc(g.name_ar)}"></div></div>
    <div class="g3"><div class="field"><label for="g-tx">Scientific group</label><input id="g-tx" name="taxon" value="${esc(g.taxon)}" placeholder="e.g. Salticidae"></div>
      <div class="field"><label for="g-cat">Gallery section</label><select id="g-cat" name="category">${Object.entries(CATS).map(([k,v])=>`<option value="${k}"${g.category===k?' selected':''}>${v}</option>`).join('')}</select></div>
      <label class="switch small"><input type="checkbox" name="taxon_italic" ${g.taxon_italic?'checked':''}><span>Italic (genus or species name)</span></label></div>
    <div class="g2"><div class="field"><label for="g-ae">Alt text for search engines (English)</label><textarea id="g-ae" name="alt_en" rows="3" placeholder="What the photo shows, + Maryam Aalali + UAE">${esc(g.alt_en)}</textarea></div>
      <div class="field" dir="rtl"><label for="g-aa">النص البديل (عربي)</label><textarea id="g-aa" name="alt_ar" rows="3">${esc(g.alt_ar)}</textarea></div></div>
    <p class="err" id="gErr" hidden></p>
    <div class="a-actions"><button class="btn solid" type="submit" id="gSave">${isNew?'Upload and add':'Save'}</button>${isNew?'':'<button class="btn danger" type="button" id="gDel">Delete</button>'}</div></form>`);
  const f=$('#galForm'), er=$('#gErr');
  f.addEventListener('submit',async e=>{e.preventDefault();er.hidden=true;
    const r={id:g.id,sort:g.sort,published:f.published.checked,taxon_italic:f.taxon_italic.checked,category:f.category.value};['name_en','name_ar','taxon','alt_en','alt_ar'].forEach(k=>r[k]=f[k].value.trim());
    const file=f.file.files[0];
    if(isNew&&!file){er.textContent='Choose a photograph to upload.';er.hidden=false;return}
    if(!r.name_en||!r.name_ar){er.textContent='Add the name in both languages.';er.hidden=false;return}
    if(!r.alt_en||!r.alt_ar){er.textContent='Add alt text in both languages; it helps the photo appear in image search.';er.hidden=false;return}
    const btn=$('#gSave');btn.disabled=true;btn.textContent='Uploading…';
    try{
      if(file){const base=r.name_en.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')+'-macro-uae';
        r.image_url=await A.uploadGalleryImage(await resize(file,1800),base+'.jpg');r.thumb_url=await A.uploadGalleryImage(await resize(file,900),base+'-thumb.jpg')}
      await A.save('gallery',r);closeDrawer();toast('Gallery updated');renderGallery()
    }catch(x){er.textContent=errMsg(x);er.hidden=false;btn.disabled=false;btn.textContent='Save'}});
  if(!isNew) armDelete($('#gDel'),async()=>{await A.remove('gallery',g.id);closeDrawer();toast('Photograph removed from the gallery');renderGallery()});
}

/* ---------- auth + boot ---------- */
async function enter(){
  $('#login').hidden=true;$('#app').hidden=false;
  $('#modeBadge').textContent=MBM.live?'Live':'Preview';$('#modeBadge').className='pill '+(MBM.live?'ok':'warn');
  $('#demoBar').hidden=MBM.live;
  try{await refresh()}catch(x){toast(errMsg(x),1)}
  route();
}
window.addEventListener('hashchange',()=>{if(!$('#app').hidden)route()});
$('#signOut').onclick=async()=>{await A.signOut();location.hash='';location.reload()};
$('#resetDemo').onclick=async()=>{A.resetDemo();await refresh();route();toast('Preview data reset')};
$('#loginForm').addEventListener('submit',async e=>{
  e.preventDefault();const er=$('#lErr');er.hidden=true;const btn=e.target.querySelector('button');btn.disabled=true;
  try{await A.signIn(e.target.email.value.trim(),e.target.password.value);
    if(!(await A.isAdmin())){await A.signOut();throw new Error('not_admin')}
    enter();
  }catch(x){er.textContent=x.message==='not_admin'?'This account is signed in but is not an admin. Add it to the admins table in Supabase (see the setup guide).':
    /invalid/i.test(x.message||'')?'Email or password is incorrect.':'Could not sign in. Check your connection and try again.';er.hidden=false}
  finally{btn.disabled=false}
});
(async()=>{
  if(!MBM.live){$('#loginLive').hidden=true;$('#loginDemo').hidden=false;$('#enterDemo').onclick=enter;return}
  try{const s=await A.session(); if(s&&await A.isAdmin()) enter();}catch(_){}
})();
})();
