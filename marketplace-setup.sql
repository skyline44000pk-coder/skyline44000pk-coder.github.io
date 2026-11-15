-- SKYLINE free property marketplace: run this in Supabase SQL Editor.
-- Public visitors can submit ads that become visible immediately.
-- Automatic publishing increases spam and scam risk; monitor listings regularly.
create extension if not exists pgcrypto;

create table if not exists public.property_listings (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) between 8 and 110),
  purpose text not null check (purpose in ('sale','rent')),
  property_type text not null check (property_type in ('Plot','House','Apartment / Flat','Commercial','Agricultural Land','Other')),
  city text not null,
  area text not null,
  size text not null,
  price numeric(16,2) not null check (price > 0),
  bedrooms integer check (bedrooms is null or bedrooms between 0 and 30),
  description text not null check (char_length(description) between 10 and 1800),
  photo_urls text[] not null default '{}',
  contact_name text not null,
  contact_phone text not null,
  status text not null default 'pending' check (status in ('pending','approved','rejected')),
  created_at timestamptz not null default now()
);

alter table public.property_listings enable row level security;
grant select on public.property_listings to anon, authenticated;
grant insert on public.property_listings to anon, authenticated;

drop policy if exists "Public can view approved property ads" on public.property_listings;
create policy "Public can view approved property ads"
on public.property_listings for select to anon, authenticated
using (status = 'approved');

drop policy if exists "Public can submit pending property ads" on public.property_listings;
drop policy if exists "Public can publish property ads immediately" on public.property_listings;
create policy "Public can publish property ads immediately"
on public.property_listings for insert to anon, authenticated
with check (status = 'approved');

create index if not exists property_listings_browse_idx
on public.property_listings (status, city, purpose, created_at desc);

-- Public photo bucket. Only image files up to 5 MB are accepted by the bucket.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('property-photos', 'property-photos', true, 5242880, array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set public = true, file_size_limit = 5242880,
allowed_mime_types = array['image/jpeg','image/png','image/webp'];

drop policy if exists "Public can upload property photos" on storage.objects;
create policy "Public can upload property photos"
on storage.objects for insert to anon, authenticated
with check (bucket_id = 'property-photos');

drop policy if exists "Anyone can view property photos" on storage.objects;
create policy "Anyone can view property photos"
on storage.objects for select to anon, authenticated
using (bucket_id = 'property-photos');

-- Ads submitted through the website are published immediately without manual approval.
-- Monitor the table regularly and remove fraudulent or misleading ads.
-- Do not expose any secret/service_role key in marketplace.html.
