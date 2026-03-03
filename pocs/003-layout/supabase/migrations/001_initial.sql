-- ============================================================
-- Anza SolarPro — Initial Schema
-- Run this once in your Supabase project's SQL Editor.
-- ============================================================

create extension if not exists "uuid-ossp";

-- ============================================================
-- TABLE: profiles
-- Auto-created for each new auth.users row via trigger.
-- ============================================================
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  created_at timestamptz default now()
);

alter table public.profiles enable row level security;

create policy "profiles: select own"
  on public.profiles for select using (auth.uid() = id);
create policy "profiles: insert own"
  on public.profiles for insert with check (auth.uid() = id);
create policy "profiles: update own"
  on public.profiles for update using (auth.uid() = id);

-- ============================================================
-- TABLE: modules
-- ============================================================
create table public.modules (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  width_m double precision not null,
  height_m double precision not null,
  power_w double precision not null,
  created_at timestamptz default now()
);

alter table public.modules enable row level security;

create policy "modules: all own"
  on public.modules for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- ============================================================
-- TABLE: racks
-- ============================================================
create table public.racks (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  max_width_m double precision not null,
  max_height_m double precision not null,
  racking_type text not null check (racking_type in ('fixed-tilt', 'tracker')),
  created_at timestamptz default now()
);

alter table public.racks enable row level security;

create policy "racks: all own"
  on public.racks for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- ============================================================
-- TABLE: projects
-- ============================================================
create table public.projects (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  address text,
  lat double precision not null,
  lng double precision not null,
  created_at timestamptz default now()
);

alter table public.projects enable row level security;

create policy "projects: all own"
  on public.projects for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- ============================================================
-- TABLE: project_layouts
-- ============================================================
create table public.project_layouts (
  id uuid primary key default uuid_generate_v4(),
  project_id uuid not null references public.projects(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  boundary_geojson jsonb,
  keepouts_geojson jsonb default '[]'::jsonb,
  perimeter_offset_m double precision default 0,
  rack_id uuid references public.racks(id) on delete set null,
  module_id uuid references public.modules(id) on delete set null,
  ns_spacing_m double precision default 5,
  ew_spacing_m double precision default 2,
  evaluated_results jsonb default '[]'::jsonb,
  custom_layouts jsonb default '[]'::jsonb,
  updated_at timestamptz default now()
);

alter table public.project_layouts enable row level security;

create policy "layouts: all own"
  on public.project_layouts for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- ============================================================
-- TRIGGER: seed default library for each new user
-- ============================================================
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  -- Create profile
  insert into public.profiles (id, full_name)
  values (new.id, new.raw_user_meta_data->>'full_name');

  -- Seed default modules
  insert into public.modules (user_id, name, width_m, height_m, power_w) values
    (new.id, 'JinkoSolar Tiger Neo 605W',  1.134, 2.278, 605),
    (new.id, 'LONGi Hi-MO 6 580W',         1.134, 2.256, 580),
    (new.id, 'Trina Vertex S+ 600W',        1.134, 2.278, 600),
    (new.id, 'Canadian Solar HiKu7 665W',   1.303, 2.384, 665);

  -- Seed default racks
  insert into public.racks (user_id, name, max_width_m, max_height_m, racking_type) values
    (new.id, 'Fixed Tilt 2V',                 4.268,  4.556, 'fixed-tilt'),
    (new.id, 'Fixed Tilt 4V',                 4.268,  9.112, 'fixed-tilt'),
    (new.id, 'NEXTracker NX Horizon',          4.268,  4.556, 'tracker'),
    (new.id, 'Array Technologies DuraTrack',   4.268,  4.556, 'tracker');

  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
