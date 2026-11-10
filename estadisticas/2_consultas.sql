-- BlindSpots · consultas para ver las estadísticas.
-- En Supabase → SQL Editor, pega la consulta que quieras y pulsa Run.

-- Resumen general.
select
  count(*) filter (where tipo = 'inicio')                         as partidas_empezadas,
  count(*) filter (where tipo = 'fin')                            as partidas_terminadas,
  count(*) filter (where tipo = 'fin' and resultado = 'victoria') as victorias,
  count(distinct creada::date)                                    as dias_con_partidas
from public.partidas;

-- Partidas por día (últimos 30 días).
select creada::date as dia,
       count(*) filter (where tipo = 'inicio') as empezadas,
       count(*) filter (where tipo = 'fin')    as terminadas
from public.partidas
where creada > now() - interval '30 days'
group by 1 order by 1 desc;

-- Niveles de campaña: cuántas veces se juega cada uno y cuántas se gana.
select nivel,
       count(*) filter (where tipo = 'inicio')                         as jugadas,
       count(*) filter (where tipo = 'fin' and resultado = 'victoria') as ganadas,
       count(*) filter (where tipo = 'fin' and resultado = 'derrota')  as perdidas
from public.partidas
where nivel is not null
group by nivel order by nivel;

-- Número de jugadores y cuántos son personas (el resto, bots).
select jugadores, humanos, modo, count(*) as partidas
from public.partidas
where tipo = 'inicio'
group by 1, 2, 3 order by partidas desc;

-- Desde dónde se juega: país y zona horaria.
select coalesce(pais, '?') as pais, zona, count(*) as partidas
from public.partidas
where tipo = 'inicio'
group by 1, 2 order by partidas desc;

-- Móvil u ordenador, idioma y versión de la web.
select dispositivo, idioma, version, count(*) as partidas
from public.partidas
where tipo = 'inicio'
group by 1, 2, 3 order by partidas desc;

-- Las últimas 50 filas, tal cual.
select * from public.partidas order by creada desc limit 50;
