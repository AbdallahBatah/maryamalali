-- =====================================================================
-- macro by maryam · Supabase schema
-- Run once in Supabase → SQL Editor → New query → paste → Run.
-- Then run seed.sql.
-- =====================================================================

create extension if not exists pgcrypto;

-- ---------- admins ----------
create table if not exists public.admins (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);
alter table public.admins enable row level security;   -- no policies: only the functions below read it

create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where user_id = auth.uid());
$$;
grant execute on function public.is_admin() to anon, authenticated;

-- ---------- trips (the calendar) ----------
create table if not exists public.trips (
  id              uuid primary key default gen_random_uuid(),
  kind            text not null default 'macro_walk'
                  check (kind in ('macro_walk','night_walk','kids_trip','workshop','exhibition')),
  title_en        text not null,
  title_ar        text not null default '',
  trip_date       date not null,
  start_time      time not null,
  end_time        time,
  location_en     text not null default '',
  location_ar     text not null default '',
  map_url         text,
  price_aed       numeric(10,2) not null default 0 check (price_aed >= 0),
  child_price_aed numeric(10,2) check (child_price_aed >= 0),      -- empty = same as adult price
  capacity        int not null default 15 check (capacity > 0),
  description_en  text not null default '',
  description_ar  text not null default '',
  includes_en     text[] not null default '{}',
  includes_ar     text[] not null default '{}',
  rules_en        text not null default '',
  rules_ar        text not null default '',
  published       boolean not null default false,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index if not exists trips_date_idx on public.trips (trip_date);

-- ---------- bookings ----------
create table if not exists public.bookings (
  id              uuid primary key default gen_random_uuid(),
  ref             text not null unique default upper(substr(replace(gen_random_uuid()::text,'-',''),1,8)),
  trip_id         uuid not null references public.trips(id) on delete restrict,
  contact_name    text not null,
  mobile          text not null,
  email           text not null,
  adults          int not null default 0 check (adults >= 0),
  children        int not null default 0 check (children >= 0),
  participants    jsonb not null default '[]'::jsonb,   -- [{type:'adult',name} | {type:'child',name,age,parent_mobile}]
  total_aed       numeric(10,2) not null,
  allergies       boolean not null default false,
  allergy_details text,
  photo_consent   boolean not null,
  rules_agreed    boolean not null check (rules_agreed),
  receipt_path    text not null,
  lang            text not null default 'en',
  status          text not null default 'pending' check (status in ('pending','confirmed','cancelled')),
  admin_note      text,
  created_at      timestamptz not null default now(),
  check (adults + children > 0)
);
create index if not exists bookings_trip_idx on public.bookings (trip_id);

-- ---------- editable content ----------
create table if not exists public.settings (
  key        text primary key,          -- 'bank', 'contact', 'booking_note'
  value      jsonb not null,
  updated_at timestamptz not null default now()
);

create table if not exists public.faqs (
  id        uuid primary key default gen_random_uuid(),
  group_en  text not null,
  group_ar  text not null,
  q_en      text not null,
  q_ar      text not null,
  a_en      text not null,
  a_ar      text not null,
  sort      int not null default 0,
  published boolean not null default true
);

create table if not exists public.gallery (
  id           uuid primary key default gen_random_uuid(),
  image_url    text not null,       -- site-relative (img/...) or a full Supabase Storage URL
  thumb_url    text not null,
  name_en      text not null,
  name_ar      text not null,
  taxon        text not null default '',
  taxon_italic boolean not null default false,
  category     text not null default 'other' check (category in ('butterflies','bees','spiders','other')),
  alt_en       text not null default '',
  alt_ar       text not null default '',
  sort         int not null default 0,
  published    boolean not null default true,
  created_at   timestamptz not null default now()
);

-- ---------- row level security ----------
alter table public.trips    enable row level security;
alter table public.bookings enable row level security;
alter table public.settings enable row level security;
alter table public.faqs     enable row level security;
alter table public.gallery  enable row level security;

drop policy if exists "read published trips" on public.trips;
create policy "read published trips" on public.trips for select using (published or public.is_admin());
drop policy if exists "admins manage trips" on public.trips;
create policy "admins manage trips" on public.trips for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- bookings: visitors never read or write the table directly (they use create_booking below)
drop policy if exists "admins manage bookings" on public.bookings;
create policy "admins manage bookings" on public.bookings for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "read settings" on public.settings;
create policy "read settings" on public.settings for select using (true);
drop policy if exists "admins manage settings" on public.settings;
create policy "admins manage settings" on public.settings for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "read published faqs" on public.faqs;
create policy "read published faqs" on public.faqs for select using (published or public.is_admin());
drop policy if exists "admins manage faqs" on public.faqs;
create policy "admins manage faqs" on public.faqs for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "read published gallery" on public.gallery;
create policy "read published gallery" on public.gallery for select using (published or public.is_admin());
drop policy if exists "admins manage gallery" on public.gallery;
create policy "admins manage gallery" on public.gallery for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- public availability (seats left, without exposing bookings) ----------
create or replace function public.public_trips(from_date date, to_date date)
returns table (
  id uuid, kind text, title_en text, title_ar text, trip_date date, start_time time, end_time time,
  location_en text, location_ar text, map_url text, price_aed numeric, child_price_aed numeric,
  capacity int, description_en text, description_ar text, includes_en text[], includes_ar text[],
  rules_en text, rules_ar text, seats_left int
)
language sql stable security definer set search_path = public as $$
  select t.id, t.kind, t.title_en, t.title_ar, t.trip_date, t.start_time, t.end_time,
         t.location_en, t.location_ar, t.map_url, t.price_aed, t.child_price_aed,
         t.capacity, t.description_en, t.description_ar, t.includes_en, t.includes_ar,
         t.rules_en, t.rules_ar,
         greatest(t.capacity - coalesce((select sum(b.adults + b.children) from public.bookings b
                                         where b.trip_id = t.id and b.status <> 'cancelled'), 0), 0)::int
  from public.trips t
  where t.published and t.trip_date between from_date and to_date
  order by t.trip_date, t.start_time;
$$;
grant execute on function public.public_trips(date, date) to anon, authenticated;

-- ---------- create a booking (checks seats atomically) ----------
create or replace function public.create_booking(p jsonb)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  t      public.trips%rowtype;
  a      int := coalesce((p->>'adults')::int, 0);
  c      int := coalesce((p->>'children')::int, 0);
  taken  int;
  total  numeric;
  r      public.bookings%rowtype;
begin
  select * into t from public.trips where id = (p->>'trip_id')::uuid and published for update;
  if not found then raise exception 'trip_not_found'; end if;
  if t.trip_date < (now() at time zone 'Asia/Dubai')::date then raise exception 'trip_closed'; end if;
  if a < 0 or c < 0 or a + c < 1 or a + c > 30 then raise exception 'bad_count'; end if;
  if coalesce(trim(p->>'contact_name'),'') = '' or coalesce(trim(p->>'mobile'),'') = ''
     or coalesce(trim(p->>'email'),'') = '' then raise exception 'missing_fields'; end if;
  if jsonb_typeof(p->'participants') <> 'array' or jsonb_array_length(p->'participants') <> a + c then
    raise exception 'bad_participants'; end if;
  if coalesce(p->>'receipt_path','') not like (t.id::text || '/%') then raise exception 'bad_receipt'; end if;
  if coalesce((p->>'rules_agreed')::boolean, false) is not true then raise exception 'rules_not_agreed'; end if;

  select coalesce(sum(adults + children), 0) into taken
  from public.bookings where trip_id = t.id and status <> 'cancelled';
  if taken + a + c > t.capacity then raise exception 'not_enough_seats'; end if;

  total := a * t.price_aed + c * coalesce(t.child_price_aed, t.price_aed);

  insert into public.bookings (trip_id, contact_name, mobile, email, adults, children, participants, total_aed,
                               allergies, allergy_details, photo_consent, rules_agreed, receipt_path, lang)
  values (t.id, left(trim(p->>'contact_name'),120), left(trim(p->>'mobile'),40), left(trim(p->>'email'),160),
          a, c, p->'participants', total,
          coalesce((p->>'allergies')::boolean, false), left(p->>'allergy_details', 1000),
          coalesce((p->>'photo_consent')::boolean, false), true, p->>'receipt_path',
          case when p->>'lang' = 'ar' then 'ar' else 'en' end)
  returning * into r;

  return jsonb_build_object('ref', r.ref, 'total_aed', r.total_aed);
end $$;
grant execute on function public.create_booking(jsonb) to anon, authenticated;

-- ---------- storage ----------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types) values
  ('receipts', 'receipts', false, 10485760, array['image/jpeg','image/png','image/webp','image/heic','image/heif','application/pdf']),
  ('gallery',  'gallery',  true,  10485760, array['image/jpeg','image/png','image/webp'])
on conflict (id) do nothing;

drop policy if exists "visitors upload receipts" on storage.objects;
create policy "visitors upload receipts" on storage.objects for insert to anon, authenticated
  with check (bucket_id = 'receipts');
drop policy if exists "admins read receipts" on storage.objects;
create policy "admins read receipts" on storage.objects for select to authenticated
  using (bucket_id = 'receipts' and public.is_admin());
drop policy if exists "admins delete receipts" on storage.objects;
create policy "admins delete receipts" on storage.objects for delete to authenticated
  using (bucket_id = 'receipts' and public.is_admin());
drop policy if exists "admins manage gallery files" on storage.objects;
create policy "admins manage gallery files" on storage.objects for all to authenticated
  using (bucket_id = 'gallery' and public.is_admin()) with check (bucket_id = 'gallery' and public.is_admin());
