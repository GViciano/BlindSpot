-- BlindSpots · tabla de estadísticas anónimas.
-- Pégalo entero en Supabase → SQL Editor → New query → Run. Solo hace falta una vez.
--
-- La web puede AÑADIR filas (con la clave pública), pero nadie puede LEERLAS con esa clave:
-- solo tú, desde el panel de Supabase (Table Editor o SQL Editor).

create table if not exists public.partidas (
  id          bigint generated always as identity primary key,
  creada      timestamptz not null default now(),
  tipo        text not null check (tipo in ('inicio', 'fin')),   -- empieza o termina una partida
  partida     text check (char_length(partida) <= 20),            -- identificador de la partida (une inicio y fin)
  modo        text check (modo in ('local', 'online')),
  conexion    text check (char_length(conexion) <= 20),           -- online: supa (servidor) o p2p (directa)
  jugadores   smallint check (jugadores between 3 and 5),
  humanos     smallint check (humanos between 0 and 5),
  nombres     text[] check (cardinality(nombres) <= 5),             -- nombres de los jugadores; los bots, con «(bot)»
  colores     smallint check (colores between 3 and 5),
  nivel       smallint check (nivel between 1 and 99),            -- nivel de campaña (vacío = partida libre)
  objetivos   smallint check (objetivos between 0 and 5),         -- cartas de misión por jugador
  necesarias  smallint check (necesarias between 0 and 99),       -- estrellas para ganar (vacío = todas)
  resultado   text check (resultado in ('victoria', 'derrota')),
  estrellas   smallint check (estrellas between 0 and 99),
  zona        text check (char_length(zona) <= 60),               -- zona horaria del dispositivo, p. ej. Europe/Madrid
  idioma      text check (char_length(idioma) <= 20),
  dispositivo text check (dispositivo in ('movil', 'ordenador')),
  web         text check (char_length(web) <= 60),
  version     text check (char_length(version) <= 20),
  hora_local  text check (char_length(hora_local) <= 20),         -- hora del dispositivo, p. ej. 2026-11-10 18:32:05
  empezada    timestamptz,                                         -- hora de inicio de la partida
  terminada   timestamptz,                                         -- hora de fin (solo en las filas 'fin')
  duracion_min numeric(6,1) check (duracion_min between 0 and 9999),
  -- País (código de 2 letras) que Supabase deduce de la conexión; la IP no se guarda.
  pais        text default (current_setting('request.headers', true)::json ->> 'cf-ipcountry')
);

alter table public.partidas enable row level security;

-- La web (clave pública, rol anon) solo puede insertar. No hay política de lectura:
-- con la clave pública no se puede consultar nada.
drop policy if exists "la web puede registrar partidas" on public.partidas;
create policy "la web puede registrar partidas" on public.partidas
  for insert to anon with check (true);

grant insert on public.partidas to anon;
revoke select, update, delete on public.partidas from anon, authenticated;

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
