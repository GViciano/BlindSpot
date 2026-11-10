-- BlindSpots · añade los nombres de los jugadores de cada partida.
-- Solo si ya creaste la tabla con una versión anterior de 1_crear_tabla.sql (y, si hacía falta,
-- ejecutaste 3_anadir_horas.sql): Supabase → SQL Editor → New query → pega esto → Run.

alter table public.partidas add column if not exists nombres text[] check (cardinality(nombres) <= 5);

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
  i.pais, i.zona, i.idioma, i.dispositivo, i.version,
  i.nombres
from public.partidas i
left join public.partidas f on f.partida = i.partida and f.tipo = 'fin'
where i.tipo = 'inicio';

revoke all on public.partidas_resumen from anon, authenticated;
