-- Guestbook / per-paper comments table for jerexjs-blog.
--
-- Run this once in Supabase → SQL Editor (or `supabase db push` if using the CLI).
-- The site is fully static (GitHub Pages) and uses the anon key from the
-- browser, so all access goes through the Postgres RLS policies below.
--
-- Spec from the user:
--   * No auth required.
--   * Comments are scoped per paper (paper_id = the Astro content collection id).
--   * Anyone can create, edit, or delete any comment.
--
-- => RLS is enabled, but every operation is allowed for the anon role.

create extension if not exists pgcrypto;

create table if not exists public.comments (
  id          uuid          primary key default gen_random_uuid(),
  paper_id    text          not null,
  author      text,
  body        text          not null check (length(body) between 1 and 4000),
  created_at  timestamptz   not null default now(),
  updated_at  timestamptz   not null default now()
);

create index if not exists comments_paper_id_created_at_idx
  on public.comments (paper_id, created_at);

alter table public.comments enable row level security;

drop policy if exists "comments_anon_select" on public.comments;
drop policy if exists "comments_anon_insert" on public.comments;
drop policy if exists "comments_anon_update" on public.comments;
drop policy if exists "comments_anon_delete" on public.comments;

create policy "comments_anon_select"
  on public.comments for select
  to anon, authenticated
  using (true);

create policy "comments_anon_insert"
  on public.comments for insert
  to anon, authenticated
  with check (true);

create policy "comments_anon_update"
  on public.comments for update
  to anon, authenticated
  using (true) with check (true);

create policy "comments_anon_delete"
  on public.comments for delete
  to anon, authenticated
  using (true);
