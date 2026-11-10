/* macro by maryam · data layer
   Live mode: Supabase (fill assets/config.js). Demo mode: in-browser sample data, used when config is empty
   or Supabase is unreachable, so the calendar, booking form and admin panel can be reviewed before launch. */
(function(){
const cfg = window.MBM_CONFIG || {};
const LIVE = !!(cfg.supabaseUrl && cfg.supabaseAnonKey && window.supabase && window.supabase.createClient);
const sb = LIVE ? window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseAnonKey) : null;

const pad = n => String(n).padStart(2,'0');
const iso = d => d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : 'id-'+Date.now()+'-'+Math.random().toString(16).slice(2));
const err = (code) => { const e = new Error(code); e.code = code; return e; };
const unwrap = ({data, error}) => { if (error) throw err(error.message || 'request_failed'); return data; };

/* ---------------- demo store ---------------- */
const DEMO_KEY = 'mbm-demo-v2';
const INCLUDES_EN = ["Macro photos for learning & discussion before the walk","Interactive exploration challenge during the walk","Drinks & snacks","Headlamps","Full trip guidance experience"];
const INCLUDES_AR = ["صور ماكرو للتعلّم والنقاش قبل الجولة","تحدٍّ استكشافي تفاعلي خلال الجولة","مشروبات ووجبات خفيفة","مصابيح رأس","تجربة إرشاد كاملة طوال الرحلة"];
const RULES_EN = "I commit to respecting nature, keeping the area clean and following Mushrif Park rules, and I understand that each participant is responsible for their own safety during the walk.";
const RULES_AR = "ألتزم باحترام الطبيعة والحفاظ على نظافة المكان واتباع أنظمة حديقة مشرف، وأدرك أن كل مشارك مسؤول عن سلامته الشخصية خلال الجولة.";
function nextDow(from, dow, plusWeeks){ const d=new Date(from); d.setDate(d.getDate()+((dow-d.getDay()+7)%7||7)+7*plusWeeks); return d; }
function demoSeed(){
  const now = new Date();
  const mk = (o) => Object.assign({id:uid(), kind:'macro_walk', title_en:'Macro Walk', title_ar:'جولة ماكرو', start_time:'09:00', end_time:'11:30',
    location_en:'Mushrif Park, Dubai', location_ar:'حديقة مشرف، دبي', map_url:'', price_aed:150, child_price_aed:null, capacity:15,
    description_en:"A guided morning walk into the macro world: learn to find, observe and photograph insects and spiders in their habitat.",
    description_ar:"جولة صباحية بإرشاد في عالم الماكرو: تعلّم كيف تجد الحشرات والعناكب وتراقبها وتصوّرها في بيئتها الطبيعية.",
    includes_en:INCLUDES_EN, includes_ar:INCLUDES_AR, rules_en:RULES_EN, rules_ar:RULES_AR, published:true, example:true}, o);
  const trips = [
    mk({trip_date: iso(nextDow(now,6,0))}),
    mk({trip_date: iso(nextDow(now,5,1)), kind:'night_walk', title_en:'Night Macro Walk', title_ar:'جولة ماكرو ليلية', start_time:'19:00', end_time:'21:30',
        description_en:"After dark, with headlamps and diffused flash, we look for the species that only come out at night.",
        description_ar:"بعد حلول الظلام، ومع مصابيح الرأس والفلاش الموزّع، نبحث عن الكائنات التي لا تظهر إلا ليلاً.", capacity:12}),
    mk({trip_date: iso(nextDow(now,6,2)), kind:'kids_trip', title_en:"Little Explorers: Children's Macro Trip", title_ar:'المستكشفون الصغار: رحلة ماكرو للأطفال',
        start_time:'08:30', end_time:'10:30', price_aed:120, child_price_aed:100, capacity:20,
        description_en:"A gentle trip for children aged 6 and up with a parent: magnifiers, printed macro photos and an insect-spotting challenge.",
        description_ar:"رحلة لطيفة للأطفال من عمر 6 سنوات فما فوق برفقة أحد الوالدين: عدسات مكبّرة وصور ماكرو مطبوعة وتحدٍّ لاكتشاف الحشرات."}),
    mk({trip_date: iso(nextDow(now,6,4))}),
  ];
  const b = (t, o) => Object.assign({id:uid(), ref:Math.random().toString(16).slice(2,10).toUpperCase(), trip_id:t.id, email:'example@example.com',
    allergies:false, allergy_details:'', photo_consent:true, rules_agreed:true, receipt_path:'', lang:'en', status:'pending', admin_note:'', created_at:new Date().toISOString(), example:true}, o);
  const bookings = [
    b(trips[0], {contact_name:'Example booking (Aisha)', mobile:'+971 50 000 0001', adults:1, children:2, total_aed:450, status:'confirmed',
      participants:[{type:'adult',name:'Aisha'},{type:'child',name:'Hamdan',age:8,parent_mobile:'+971 50 000 0001'},{type:'child',name:'Mariam',age:6,parent_mobile:'+971 50 000 0001'}]}),
    b(trips[0], {contact_name:'Example booking (Omar)', mobile:'+971 50 000 0002', adults:2, children:0, total_aed:300, allergies:true, allergy_details:'Peanuts',
      participants:[{type:'adult',name:'Omar'},{type:'adult',name:'Sara'}]}),
  ];
  return {trips, bookings, receipts:{},
    settings:{
      bank:{bank_name:'ADIB', account_holder:'MARYAM AL ALI', account_number:'23906783', iban:'AE380500000000023906783', swift:'ABDIAEADXXX', currency:'AED'},
      contact:{email:'maryamaalali@live.com', phone:'+971529137373', instagram:'macrobymaryam'},
      booking_note:{en:"Please complete the registration by filling in the details below and uploading the payment confirmation.",
                    ar:"يرجى إكمال التسجيل بتعبئة البيانات أدناه ورفع إثبات الدفع."}},
    faqs:[], gallery:[]};
}
let demo = null;
function loadDemo(){
  if (demo) return demo;
  try { demo = JSON.parse(localStorage.getItem(DEMO_KEY)); } catch(e) {}
  if (!demo || !demo.trips) demo = demoSeed();
  const seed = window.MBM_SEED || {};
  ['faqs','gallery'].forEach(k => { if ((!demo[k] || !demo[k].length) && seed[k]) demo[k] = seed[k].map(r => Object.assign({id:uid()}, r)); });
  demo.receipts = demo.receipts || {};
  return demo;
}
function saveDemo(){ try { localStorage.setItem(DEMO_KEY, JSON.stringify(demo)); } catch(e) { try { localStorage.setItem(DEMO_KEY, JSON.stringify(Object.assign({}, demo, {receipts:{}}))); } catch(_) {} } }
const seatsLeft = (t, bookings) => Math.max(0, t.capacity - bookings.filter(b => b.trip_id===t.id && b.status!=='cancelled').reduce((s,b)=>s+b.adults+b.children,0));
const delay = (v) => new Promise(r => setTimeout(() => r(v), 180));

/* ---------------- public API ---------------- */
const api = {
  live: LIVE,
  iso,
  async trips(from, to){
    if (LIVE) return unwrap(await sb.rpc('public_trips', {from_date: from, to_date: to}));
    const d = loadDemo();
    return delay(d.trips.filter(t => t.published && t.trip_date>=from && t.trip_date<=to)
      .sort((a,b)=>(a.trip_date+a.start_time).localeCompare(b.trip_date+b.start_time))
      .map(t => Object.assign({}, t, {seats_left: seatsLeft(t, d.bookings)})));
  },
  async settings(){
    if (LIVE){ const rows = unwrap(await sb.from('settings').select('key,value')); const o={}; rows.forEach(r=>o[r.key]=r.value); return o; }
    return delay(JSON.parse(JSON.stringify(loadDemo().settings)));
  },
  async faqs(){ if (LIVE) return unwrap(await sb.from('faqs').select('*').eq('published',true).order('sort')); return []; },
  async gallery(){ if (LIVE) return unwrap(await sb.from('gallery').select('*').eq('published',true).order('sort')); return []; },
  async uploadReceipt(file, tripId){
    const ext = (file.name.split('.').pop() || 'jpg').toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,5) || 'jpg';
    const path = tripId + '/' + uid() + '.' + ext;
    if (LIVE){ unwrap(await sb.storage.from('receipts').upload(path, file, {contentType: file.type || undefined, upsert:false})); return path; }
    const d = loadDemo();
    d.receipts[path] = file.size < 1.5*1024*1024
      ? await new Promise(r => { const fr = new FileReader(); fr.onload = () => r(fr.result); fr.onerror = () => r(URL.createObjectURL(file)); fr.readAsDataURL(file); })
      : URL.createObjectURL(file);
    return delay(path);
  },
  async book(p){
    if (LIVE){ const {data, error} = await sb.rpc('create_booking', {p}); if (error) throw err((error.message||'').match(/[a-z_]+/)?.[0] || 'request_failed'); return data; }
    const d = loadDemo(), t = d.trips.find(x => x.id===p.trip_id && x.published);
    if (!t) throw err('trip_not_found');
    if (p.adults + p.children > seatsLeft(t, d.bookings)) throw err('not_enough_seats');
    const total = p.adults*t.price_aed + p.children*(t.child_price_aed ?? t.price_aed);
    const ref = Math.random().toString(16).slice(2,10).toUpperCase();
    d.bookings.unshift(Object.assign({id:uid(), ref, status:'pending', admin_note:'', created_at:new Date().toISOString(), total_aed:total}, p));
    saveDemo(); return delay({ref, total_aed: total});
  },

  /* ---------------- admin API ---------------- */
  admin: {
    async session(){ if (!LIVE) return {demo:true}; const {data} = await sb.auth.getSession(); return data.session; },
    async signIn(email, password){ if (!LIVE) return {demo:true}; return unwrap(await sb.auth.signInWithPassword({email, password})).session; },
    async signOut(){ if (LIVE) await sb.auth.signOut(); },
    async isAdmin(){ if (!LIVE) return true; return unwrap(await sb.rpc('is_admin')); },
    async trips(){
      if (LIVE) return unwrap(await sb.from('trips').select('*').order('trip_date').order('start_time'));
      return delay(loadDemo().trips.slice().sort((a,b)=>(a.trip_date+a.start_time).localeCompare(b.trip_date+b.start_time)));
    },
    async saveTrip(t){
      const row = Object.assign({}, t); delete row.seats_left; delete row.example; delete row.created_at;
      if (LIVE){
        row.updated_at = new Date().toISOString();
        if (row.id) return unwrap(await sb.from('trips').update(row).eq('id', row.id).select().single());
        delete row.id; return unwrap(await sb.from('trips').insert(row).select().single());
      }
      const d = loadDemo();
      if (row.id){ const i = d.trips.findIndex(x=>x.id===row.id); d.trips[i] = Object.assign(d.trips[i], row); saveDemo(); return delay(d.trips[i]); }
      row.id = uid(); d.trips.push(row); saveDemo(); return delay(row);
    },
    async deleteTrip(id){
      if (LIVE){ unwrap(await sb.from('trips').delete().eq('id', id)); return; }
      const d = loadDemo(); if (d.bookings.some(b=>b.trip_id===id)) throw err('trip_has_bookings');
      d.trips = d.trips.filter(x=>x.id!==id); saveDemo();
    },
    async bookings(){
      if (LIVE) return unwrap(await sb.from('bookings').select('*').order('created_at', {ascending:false}));
      return delay(loadDemo().bookings.slice());
    },
    async updateBooking(id, patch){
      if (LIVE) return unwrap(await sb.from('bookings').update(patch).eq('id', id).select().single());
      const d = loadDemo(), b = d.bookings.find(x=>x.id===id); Object.assign(b, patch); saveDemo(); return delay(b);
    },
    async receiptUrl(path){
      if (!path) return null;
      if (LIVE) return unwrap(await sb.storage.from('receipts').createSignedUrl(path, 600)).signedUrl;
      return loadDemo().receipts[path] || null;
    },
    async saveSetting(key, value){
      if (LIVE){ unwrap(await sb.from('settings').upsert({key, value, updated_at:new Date().toISOString()})); return; }
      loadDemo().settings[key] = value; saveDemo();
    },
    async list(table){
      if (LIVE) return unwrap(await sb.from(table).select('*').order('sort'));
      return delay((loadDemo()[table]||[]).slice().sort((a,b)=>a.sort-b.sort));
    },
    async save(table, row){
      if (LIVE){
        if (row.id) return unwrap(await sb.from(table).update(row).eq('id', row.id).select().single());
        const r = Object.assign({}, row); delete r.id; return unwrap(await sb.from(table).insert(r).select().single());
      }
      const d = loadDemo(); d[table] = d[table] || [];
      if (row.id){ const i = d[table].findIndex(x=>x.id===row.id); d[table][i] = Object.assign(d[table][i], row); saveDemo(); return d[table][i]; }
      const r = Object.assign({}, row, {id:uid()}); d[table].push(r); saveDemo(); return r;
    },
    async remove(table, id){
      if (LIVE){ unwrap(await sb.from(table).delete().eq('id', id)); return; }
      const d = loadDemo(); d[table] = (d[table]||[]).filter(x=>x.id!==id); saveDemo();
    },
    async uploadGalleryImage(blob, name){
      const path = Date.now() + '-' + name.replace(/[^a-z0-9.-]/gi,'-').toLowerCase();
      if (LIVE){ unwrap(await sb.storage.from('gallery').upload(path, blob, {contentType:'image/jpeg', upsert:false}));
        return sb.storage.from('gallery').getPublicUrl(path).data.publicUrl; }
      return URL.createObjectURL(blob);
    },
    resetDemo(){ if (!LIVE){ demo = demoSeed(); saveDemo(); } },
  }
};
window.MBM = api;
})();
