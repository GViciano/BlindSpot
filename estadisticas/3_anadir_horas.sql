-- BlindSpots · añade la hora de inicio y de fin de cada partida.
-- Solo si ya creaste la tabla con una versión anterior de 1_crear_tabla.sql:
-- Supabase → SQL Editor → New query → pega esto → Run. (Si la creas ahora, no hace falta.)

alter table public.partidas add column if not exists hora_local   text check (char_length(hora_local) <= 20);
alter table public.partidas add column if not exists empezada     timestamptz;
alter table public.partidas add column if not exists terminada    timestamptz;
alter table public.partidas add column if not exists duracion_min numeric(6,1) check (duracion_min between 0 and 9999);

-- Una línea por partida: hora de inicio y de fin, duración y resultado.
-- (Las partidas sin hora de fin se abandonaron antes de terminar.)
create or replace view public.partidas_resumen with (security_invoker = true) as
select
  i.partida,
  i.hora_local        as hora_local_inicio,
  f.hora_local        as hora_local_fin,
  coalesce(i.empezada, i.creada) as empezada,
  f.terminada,
  f.duracion_min,
  i.modo, i.jugadores, i.humanos, i.colores, i.nivel, i.objetivos, i.necesarias,
  f.resultado, f.estrellas,
  i.pais, i.zona, i.idioma, i.dispositivo, i.version
from public.partidas i
left join public.partidas f on f.partida = i.partida and f.tipo = 'fin'
where i.tipo = 'inicio';

revoke all on public.partidas_resumen from anon, authenticated;
