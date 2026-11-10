(function(){
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const L = document.documentElement.lang==='ar' ? 'ar' : 'en', AR = L==='ar';
const LOC = AR ? 'ar-AE-u-nu-latn' : 'en-GB';
const S = {
  en:{seats:n=>n===1?'1 seat left':n+' seats left', full:'Full', few:'Few seats left', book:'Book this trip', perPerson:'per person', child:'child',
      noTrips:'No trips scheduled this month.', nextTrips:'See next month', allMonth:'All trips this month', selDay:'Trips on ', loading:'Loading trips…',
      loadErr:'Trips could not be loaded. Check your connection and refresh the page.', adult:'Adult', childN:'Child', name:'Full name', age:'Age', parentMobile:"Parent's mobile",
      years:'years', copy:'Copy', copied:'Copied', total:'Total to transfer', calc:(a,c,p,cp)=>[a?`${a} adult${a>1?'s':''} × ${p} AED`:'',c?`${c} ${c>1?'children':'child'} × ${cp} AED`:''].filter(Boolean).join(' + '),
      sending:'Uploading receipt…', saving:'Saving your registration…', submit:'Submit registration', from:'From',
      e:{name:'Add your full name.', mobile:'Add a mobile number we can reach you on.', email:'Enter a valid email address.', count:'Add at least one participant.',
         max:n=>`Only ${n} seat${n===1?'':'s'} left on this trip.`, pname:'Add a name for every participant.', page:'Choose an age for every child.', pmobile:"Add a parent's mobile for every child.",
         allergy:'Tell us whether anyone has allergies.', allergyDetails:'Describe the allergies so we can prepare.', photo:'Choose whether you agree to appear in photos.',
         rules:'Please agree to the trip rules to continue.', receipt:'Upload your payment receipt.', receiptSize:'The receipt must be under 10 MB.', receiptType:'Upload the receipt as an image or PDF.',
         not_enough_seats:'Sorry, there are not enough seats left. Reduce the number of participants or choose another date.', trip_closed:'This trip is no longer taking registrations.',
         trip_not_found:'This trip is no longer available. Please choose another date.', generic:'Your registration could not be sent. Check your connection and try again; your details are still here.'},
      demo:'Preview mode: these are example dates and nothing is saved to Maryam\'s bookings until the site is connected to its database.'},
  ar:{seats:n=>n===1?'مقعد واحد متبقٍ':n+' مقاعد متبقية', full:'مكتملة', few:'مقاعد قليلة متبقية', book:'احجز هذه الرحلة', perPerson:'للشخص', child:'للطفل',
      noTrips:'لا توجد رحلات مجدولة هذا الشهر.', nextTrips:'الشهر التالي', allMonth:'كل رحلات الشهر', selDay:'رحلات يوم ', loading:'جارٍ تحميل الرحلات…',
      loadErr:'تعذّر تحميل الرحلات. تحقّق من الاتصال وأعد تحميل الصفحة.', adult:'بالغ', childN:'طفل', name:'الاسم الكامل', age:'العمر', parentMobile:'جوال ولي الأمر',
      years:'سنوات', copy:'نسخ', copied:'تم النسخ', total:'المبلغ المطلوب تحويله', calc:(a,c,p,cp)=>[a?`${a} بالغ × ${p} درهم`:'',c?`${c} طفل × ${cp} درهم`:''].filter(Boolean).join(' + '),
      sending:'جارٍ رفع الإيصال…', saving:'جارٍ حفظ التسجيل…', submit:'إرسال التسجيل', from:'من',
      e:{name:'أضف اسمك الكامل.', mobile:'أضف رقم جوال يمكن التواصل معك عليه.', email:'أدخل بريداً إلكترونياً صحيحاً.', count:'أضف مشاركاً واحداً على الأقل.',
         max:n=>`المتبقي في هذه الرحلة ${n} مقاعد فقط.`, pname:'أضف اسماً لكل مشارك.', page:'اختر عمر كل طفل.', pmobile:'أضف جوال ولي الأمر لكل طفل.',
         allergy:'أخبرنا إن كان لدى أحد المشاركين حساسية.', allergyDetails:'اذكر نوع الحساسية لنستعد لها.', photo:'اختر إن كنت توافق على الظهور في الصور.',
         rules:'يرجى الموافقة على تعليمات الرحلة للمتابعة.', receipt:'ارفع إيصال الدفع.', receiptSize:'يجب أن يكون حجم الإيصال أقل من 10 ميغابايت.', receiptType:'ارفع الإيصال كصورة أو ملف PDF.',
         not_enough_seats:'عذراً، لا توجد مقاعد كافية. قلّل عدد المشاركين أو اختر موعداً آخر.', trip_closed:'هذه الرحلة لم تعد تستقبل تسجيلات.',
         trip_not_found:'هذه الرحلة لم تعد متاحة. يرجى اختيار موعد آخر.', generic:'تعذّر إرسال التسجيل. تحقّق من الاتصال وحاول مجدداً، بياناتك ما زالت محفوظة هنا.'},
      demo:'وضع المعاينة: هذه مواعيد تجريبية، ولن تُحفظ أي حجوزات قبل ربط الموقع بقاعدة البيانات.'}
}[L];

const fmtDate = (d, o) => new Intl.DateTimeFormat(LOC, o).format(new Date(d+'T00:00:00'));
const fmtTime = t => { if(!t) return ''; const [h,m]=t.split(':'); const d=new Date(2000,0,1,+h,+m); return new Intl.DateTimeFormat(LOC,{hour:'numeric',minute:'2-digit'}).format(d); };
const tt = (o,k) => (AR ? (o[k+'_ar']||o[k+'_en']) : o[k+'_en']) || '';
const money = n => (+n).toLocaleString(LOC,{maximumFractionDigits:2});
const esc = s => String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

let trips=[], settings={}, month=null, selDay=null, trip=null;
const today = new Date(); today.setHours(0,0,0,0);
const todayIso = MBM.iso(today);

/* ---------- calendar ---------- */
function renderCal(){
  const y=month.getFullYear(), m=month.getMonth();
  $('#calTitle').textContent = new Intl.DateTimeFormat(LOC,{month:'long',year:'numeric'}).format(month);
  const first = new Date(y,m,1), lead=(first.getDay()+6)%7, days=new Date(y,m+1,0).getDate();
  const byDay = {}; trips.forEach(t=>{(byDay[t.trip_date]=byDay[t.trip_date]||[]).push(t)});
  let h='';
  for(let i=0;i<lead;i++) h+='<span class="cd pad" aria-hidden="true"></span>';
  for(let d=1; d<=days; d++){
    const key=MBM.iso(new Date(y,m,d)), list=byDay[key]||[], past=key<todayIso;
    const open=list.some(t=>t.seats_left>0), cls=['cd'];
    if(past) cls.push('past'); if(list.length) cls.push(open?'has':'full'); if(key===selDay) cls.push('sel'); if(key===todayIso) cls.push('today');
    const label = fmtDate(key,{weekday:'long',day:'numeric',month:'long'}) + (list.length? ' · '+list.map(t=>tt(t,'title')).join(', ') : '');
    h += list.length && !past
      ? `<button type="button" class="${cls.join(' ')}" data-day="${key}" aria-pressed="${key===selDay}" aria-label="${esc(label)}"><span>${d}</span><i></i></button>`
      : `<span class="${cls.join(' ')}" aria-label="${esc(label)}"><span>${d}</span></span>`;
  }
  $('#calGrid').innerHTML=h;
  const minMonth=new Date(today.getFullYear(),today.getMonth(),1);
  $('#calPrev').disabled = month<=minMonth;
  renderSlots();
}
function renderSlots(){
  const y=month.getFullYear(), m=month.getMonth();
  let list = trips.filter(t=>{const d=new Date(t.trip_date+'T00:00:00');return d.getFullYear()===y&&d.getMonth()===m && t.trip_date>=todayIso});
  if(selDay) list=list.filter(t=>t.trip_date===selDay);
  $('#slotsHead').textContent = selDay ? S.selDay + fmtDate(selDay,{day:'numeric',month:'long'}) : S.allMonth;
  $('#slotsAll').hidden = !selDay;
  if(!list.length){
    const later = trips.find(t=>t.trip_date>MBM.iso(new Date(y,m+1,0)));
    $('#slots').innerHTML = `<p class="empty">${S.noTrips}</p>` + (later?`<button type="button" class="tlink" id="jumpNext">${S.nextTrips} <span class="arrow">→</span></button>`:'');
    const j=$('#jumpNext'); if(j) j.onclick=()=>{const d=new Date(later.trip_date+'T00:00:00');month=new Date(d.getFullYear(),d.getMonth(),1);selDay=null;renderCal()};
    return;
  }
  $('#slots').innerHTML = list.map(t=>{
    const full=t.seats_left<=0, few=!full&&t.seats_left<=3;
    const price = t.child_price_aed!=null && +t.child_price_aed!==+t.price_aed
      ? `${money(t.price_aed)} AED <small>${S.perPerson}</small> · ${money(t.child_price_aed)} AED <small>${S.child}</small>`
      : `${money(t.price_aed)} AED <small>${S.perPerson}</small>`;
    return `<article class="slot${full?' is-full':''}">
      <div class="slot-date"><b>${fmtDate(t.trip_date,{day:'numeric'})}</b><span>${fmtDate(t.trip_date,{month:'short'})}</span><span>${fmtDate(t.trip_date,{weekday:'short'})}</span></div>
      <div class="slot-body">
        <h3>${esc(tt(t,'title'))}</h3>
        <p class="slot-meta">${fmtTime(t.start_time)}${t.end_time?' – '+fmtTime(t.end_time):''} · ${esc(tt(t,'location'))}</p>
        <p class="slot-price">${price}</p>
        <p class="seat ${full?'s-full':few?'s-few':'s-ok'}">${full?S.full:S.seats(t.seats_left)}</p>
      </div>
      ${full?'':`<button type="button" class="btn solid" data-trip="${t.id}">${S.book} <span class="arrow">→</span></button>`}
    </article>`}).join('');
}

/* ---------- booking form ---------- */
function bankHTML(){
  const b=settings.bank||{}, rows=[
    [AR?'اسم البنك':'Bank name', b.bank_name], [AR?'اسم صاحب الحساب':'Account holder', b.account_holder], [AR?'رقم الحساب':'Account number', b.account_number],
    ['IBAN', b.iban, (b.iban||'').replace(/\s+/g,'').replace(/(.{4})/g,'$1 ').trim()], ['SWIFT', b.swift], [AR?'العملة':'Currency', b.currency]].filter(r=>r[1]);
  return rows.map(([k,v,show])=>`<div class="bank-row"><dt>${k}</dt><dd><span class="v">${esc(show||v)}</span><button type="button" class="copy" data-copyv="${esc(String(v).replace(/\s+/g,''))}">${S.copy}</button></dd></div>`).join('');
}
function openTrip(id, scroll=true){
  trip = trips.find(t=>t.id===id); if(!trip) return;
  $('#bfTitle').textContent = `${tt(trip,'title')} | ${fmtDate(trip.trip_date,{day:'numeric',month:'long',year:'numeric'})} · ${fmtTime(trip.start_time)}`;
  $('#bfMeta').innerHTML = `<span>${esc(fmtDate(trip.trip_date,{weekday:'long'}))}, ${fmtTime(trip.start_time)}${trip.end_time?' – '+fmtTime(trip.end_time):''}</span><span>${esc(tt(trip,'location'))}${trip.map_url?` · <a href="${esc(trip.map_url)}" target="_blank" rel="noopener">${AR?'الخريطة':'Map'}</a>`:''}</span><span class="seat ${trip.seats_left<=3?'s-few':'s-ok'}">${S.seats(trip.seats_left)}</span>`;
  const note = settings.booking_note ? (settings.booking_note[L]||settings.booking_note.en) : '';
  const fee = trip.child_price_aed!=null && +trip.child_price_aed!==+trip.price_aed
    ? (AR?`رسوم الرحلة ${money(trip.price_aed)} درهم للبالغ و${money(trip.child_price_aed)} درهم للطفل، وتشمل:`:`The trip fee is ${money(trip.price_aed)} AED per adult and ${money(trip.child_price_aed)} AED per child, and includes:`)
    : (AR?`رسوم الرحلة ${money(trip.price_aed)} درهم للشخص، وتشمل:`:`The trip fee is ${money(trip.price_aed)} AED per person and includes:`);
  $('#bfIntro').innerHTML = (note?`<p>${esc(note)}</p>`:'') + (tt(trip,'description')?`<p class="muted">${esc(tt(trip,'description'))}</p>`:'') + `<p>${fee}</p>`;
  const inc = AR ? (trip.includes_ar&&trip.includes_ar.length?trip.includes_ar:trip.includes_en) : trip.includes_en;
  $('#bfIncludes').innerHTML = (inc||[]).map(i=>`<li>${esc(i)}</li>`).join('');
  $('#bfRules').textContent = tt(trip,'rules') || (AR?'ألتزم باحترام الطبيعة والحفاظ على نظافة المكان واتباع أنظمة موقع الرحلة، وأدرك أن كل مشارك مسؤول عن سلامته الشخصية.':'I commit to respecting nature, keeping the area clean and following the rules of the trip location, and I understand that each participant is responsible for their own safety.');
  $('#bank').innerHTML = bankHTML();
  $('#bookWrap').hidden=false; $('#done').hidden=true; $('#bookForm').hidden=false;
  setCount('adults', Math.min(+$('#f-adults').value||1, trip.seats_left));
  setCount('children', Math.min(+$('#f-children').value||0, Math.max(0,trip.seats_left - (+$('#f-adults').value))));
  try{history.replaceState(null,'','#trip-'+trip.id)}catch(e){}
  if(scroll) $('#bookWrap').scrollIntoView({behavior:'smooth',block:'start'});
}

/* participants */
const people = {adults:[], children:[]};
function setCount(kind, n){
  n=Math.max(0, Math.min(n, 30)); $('#f-'+kind).value=n; $('#'+kind+'Out').textContent=n;
  renderPeople(); updateTotal();
}
function harvest(){
  $$('#people [data-p]').forEach(el=>{const [k,i,f]=el.dataset.p.split('.');(people[k][+i]=people[k][+i]||{})[f]=el.value});
}
function renderPeople(){
  harvest();
  const a=+$('#f-adults').value, c=+$('#f-children').value, mob=$('#f-mobile').value, nm=$('#f-name').value;
  let h='';
  for(let i=0;i<a;i++){
    const p=people.adults[i]||{}; const v = p.name!=null ? p.name : (i===0?nm:'');
    h+=`<fieldset class="person"><legend>${S.adult} ${i+1}</legend><div class="field"><label for="pa-${i}">${S.name} *</label><input id="pa-${i}" type="text" data-p="adults.${i}.name" value="${esc(v)}" autocomplete="${i===0?'name':'off'}"></div></fieldset>`;
  }
  for(let i=0;i<c;i++){
    const p=people.children[i]||{};
    const ages=['<option value="">—</option>'].concat(Array.from({length:17},(_,k)=>`<option value="${k+1}"${String(k+1)===String(p.age)?' selected':''}>${k+1}</option>`)).join('');
    h+=`<fieldset class="person kid"><legend>${S.childN} ${i+1}</legend><div class="kid-grid">
      <div class="field"><label for="pc-${i}-n">${S.name} *</label><input id="pc-${i}-n" type="text" data-p="children.${i}.name" value="${esc(p.name||'')}" autocomplete="off"></div>
      <div class="field"><label for="pc-${i}-a">${S.age} *</label><select id="pc-${i}-a" data-p="children.${i}.age">${ages}</select></div>
      <div class="field"><label for="pc-${i}-m">${S.parentMobile} *</label><input id="pc-${i}-m" type="tel" dir="ltr" data-p="children.${i}.parent_mobile" value="${esc(p.parent_mobile!=null?p.parent_mobile:mob)}" autocomplete="off"></div>
    </div></fieldset>`;
  }
  $('#people').innerHTML=h;
  $('#adultsDec').disabled=a<=0; $('#childrenDec').disabled=c<=0;
  const left = trip ? trip.seats_left : 30;
  $('#adultsInc').disabled = $('#childrenInc').disabled = a+c>=left;
}
function updateTotal(){
  if(!trip) return;
  const a=+$('#f-adults').value, c=+$('#f-children').value, cp=trip.child_price_aed!=null?+trip.child_price_aed:+trip.price_aed;
  const total=a*trip.price_aed + c*cp;
  $('#bfTotal').textContent = money(total)+' AED';
  $('#bfCalc').textContent = a+c ? S.calc(a,c,money(trip.price_aed),money(cp)) : '';
}

/* ---------- validation + submit ---------- */
function fail(msg, el){ const e=$('#bfErr'); e.textContent=msg; e.hidden=false; if(el){el.focus({preventScroll:true}); el.scrollIntoView({block:'center',behavior:'smooth'});} return false; }
function validate(){
  $('#bfErr').hidden=true;
  const f=$('#bookForm'), a=+f.adults.value, c=+f.children.value;
  if(!f.contact_name.value.trim()) return fail(S.e.name, f.contact_name);
  if(f.mobile.value.replace(/\D/g,'').length<7) return fail(S.e.mobile, f.mobile);
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value.trim())) return fail(S.e.email, f.email);
  if(a+c<1) return fail(S.e.count, $('#adultsInc'));
  if(a+c>trip.seats_left) return fail(S.e.max(trip.seats_left), $('#adultsDec'));
  for(const el of $$('#people [data-p]')){
    const f2=el.dataset.p.split('.')[2];
    if(!el.value.trim()) return fail(f2==='age'?S.e.page:f2==='parent_mobile'?S.e.pmobile:S.e.pname, el);
  }
  const al=f.querySelector('input[name=allergies]:checked'); if(!al) return fail(S.e.allergy, f.querySelector('input[name=allergies]'));
  if(al.value==='yes' && !f.allergy_details.value.trim()) return fail(S.e.allergyDetails, f.allergy_details);
  if(!f.querySelector('input[name=photo]:checked')) return fail(S.e.photo, f.querySelector('input[name=photo]'));
  if(!f.rules.checked) return fail(S.e.rules, f.rules);
  const file=f.receipt.files[0];
  if(!file) return fail(S.e.receipt, f.receipt);
  if(file.size>10*1024*1024) return fail(S.e.receiptSize, f.receipt);
  if(!/^(image\/|application\/pdf)/.test(file.type||'') && !/\.(jpe?g|png|webp|heic|heif|pdf)$/i.test(file.name)) return fail(S.e.receiptType, f.receipt);
  return true;
}
async function submit(e){
  e.preventDefault(); if(!trip || !validate()) return;
  harvest();
  const f=$('#bookForm'), a=+f.adults.value, c=+f.children.value, btn=$('#bfSubmit');
  const participants = people.adults.slice(0,a).map(p=>({type:'adult', name:(p.name||'').trim()}))
    .concat(people.children.slice(0,c).map(p=>({type:'child', name:(p.name||'').trim(), age:+p.age, parent_mobile:(p.parent_mobile||'').trim()})));
  btn.disabled=true; const label=btn.innerHTML;
  try{
    btn.textContent=S.sending;
    const path = await MBM.uploadReceipt(f.receipt.files[0], trip.id);
    btn.textContent=S.saving;
    const res = await MBM.book({trip_id:trip.id, contact_name:f.contact_name.value.trim(), mobile:f.mobile.value.trim(), email:f.email.value.trim(),
      adults:a, children:c, participants, allergies:f.allergies.value==='yes', allergy_details:f.allergies.value==='yes'?f.allergy_details.value.trim():'',
      photo_consent:f.photo.value==='yes', rules_agreed:f.rules.checked, receipt_path:path, lang:L});
    showDone(res, a, c);
  }catch(err){
    fail(S.e[err.code] || S.e.generic);
    if(err.code==='not_enough_seats'||err.code==='trip_closed'||err.code==='trip_not_found') load(false);
  }finally{ btn.disabled=false; btn.innerHTML=label; }
}
function showDone(res, a, c){
  $('#bookForm').hidden=true; const d=$('#done'); d.hidden=false;
  $('#doneRef').textContent=res.ref;
  $('#doneSum').textContent = `${tt(trip,'title')} · ${fmtDate(trip.trip_date,{weekday:'long',day:'numeric',month:'long'})} · ${fmtTime(trip.start_time)} · ${a+c} ${AR?'مشارك':'participant'+(a+c>1?'s':'')} · ${money(res.total_aed)} AED`;
  d.scrollIntoView({behavior:'smooth',block:'start'}); d.focus({preventScroll:true});
  load(false);
}

/* ---------- load ---------- */
async function load(first=true){
  if(first) $('#slots').innerHTML=`<p class="empty">${S.loading}</p>`;
  try{
    const to=new Date(today); to.setDate(to.getDate()+400);
    [trips, settings] = await Promise.all([MBM.trips(todayIso, MBM.iso(to)), first?MBM.settings():Promise.resolve(settings)]);
  }catch(e){ $('#slots').innerHTML=`<p class="empty">${S.loadErr}</p>`; return; }
  if(first){
    const m=location.hash.match(/^#trip-([\w-]+)$/), deep=m&&trips.find(t=>t.id===m[1]);
    const start = deep || trips.find(t=>t.seats_left>0) || null;
    const d = start ? new Date(start.trip_date+'T00:00:00') : today;
    month = new Date(d.getFullYear(), d.getMonth(), 1);
    if(deep) openTrip(deep.id);
    const c = settings.contact; if(c){ $$('[data-contact=email]').forEach(e=>e.textContent=c.email||e.textContent); }
  } else if(trip){ trip = trips.find(t=>t.id===trip.id) || trip; renderPeople(); }
  renderCal();
}

if(!MBM.live){ const n=$('#demoNote'); n.textContent=S.demo; n.hidden=false; }
$('#calPrev').onclick=()=>{month=new Date(month.getFullYear(),month.getMonth()-1,1);selDay=null;renderCal()};
$('#calNext').onclick=()=>{month=new Date(month.getFullYear(),month.getMonth()+1,1);selDay=null;renderCal()};
$('#calGrid').addEventListener('click',e=>{const b=e.target.closest('[data-day]');if(!b)return;selDay=selDay===b.dataset.day?null:b.dataset.day;renderCal();$('#slots').scrollIntoView({behavior:'smooth',block:'nearest'})});
$('#slotsAll').onclick=()=>{selDay=null;renderCal()};
$('#slots').addEventListener('click',e=>{const b=e.target.closest('[data-trip]');if(b)openTrip(b.dataset.trip)});
$('#bfChange').onclick=()=>{$('#bookWrap').hidden=true;$('#cal').scrollIntoView({behavior:'smooth'})};
['adults','children'].forEach(k=>{
  $('#'+k+'Inc').onclick=()=>setCount(k, +$('#f-'+k).value+1);
  $('#'+k+'Dec').onclick=()=>setCount(k, +$('#f-'+k).value-1);
});
$('#f-name').addEventListener('input',()=>{const el=$('#pa-0'); if(el && (people.adults[0]==null||people.adults[0].auto!==false)){el.value=$('#f-name').value}});
$('#people').addEventListener('input',e=>{if(e.target.id==='pa-0'){(people.adults[0]=people.adults[0]||{}).auto=false}});
$('#f-mobile').addEventListener('input',()=>{$$('#people [data-p$=".parent_mobile"]').forEach(el=>{if(!el.dataset.touched)el.value=$('#f-mobile').value})});
$('#people').addEventListener('input',e=>{if(e.target.matches('[data-p$=".parent_mobile"]'))e.target.dataset.touched='1'});
$$('input[name=allergies]').forEach(r=>r.addEventListener('change',()=>{$('#allergyBox').hidden=$('#bookForm').allergies.value!=='yes'}));
$('#f-receipt').addEventListener('change',e=>{const f=e.target.files[0];$('#receiptName').textContent=f?`${f.name} · ${(f.size/1048576).toFixed(1)} MB`:''});
document.addEventListener('click',e=>{const b=e.target.closest('[data-copyv]');if(!b)return;const done=()=>{b.textContent=S.copied;setTimeout(()=>b.textContent=S.copy,1500)};
  try{navigator.clipboard.writeText(b.dataset.copyv).then(done,()=>{const r=document.createRange();r.selectNodeContents(b.previousElementSibling);getSelection().removeAllRanges();getSelection().addRange(r)})}catch(_){}});
$('#bookForm').addEventListener('submit',submit);
$('#doneAgain').onclick=()=>{$('#bookForm').reset();people.adults=[];people.children=[];$('#receiptName').textContent='';$('#allergyBox').hidden=true;setCount('adults',1);$('#done').hidden=true;$('#bookWrap').hidden=true;$('#cal').scrollIntoView({behavior:'smooth'})};
setCount('adults',1);
load();
})();
