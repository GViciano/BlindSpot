# Estadísticas de partidas

La web guarda en Supabase una fila cada vez que empieza y cada vez que termina una partida:
los nombres de los jugadores (los bots, marcados con «(bot)»), modo (en un dispositivo u online), número de jugadores y cuántos son personas, colores, nivel de
campaña, cartas por jugador, estrellas necesarias y conseguidas, resultado, país (lo añade Supabase a
partir de la conexión, sin guardar la IP), zona horaria, idioma, móvil u ordenador y versión de la web. También la hora de inicio y de fin de
cada partida (hora local del dispositivo) y su duración en minutos.
No se guarda la dirección IP ni ningún otro dato personal.

En las partidas online solo envía datos el anfitrión, para no contar la misma partida varias veces.
Las partidas abiertas en `localhost` no se cuentan.

## Ponerlo en marcha (una sola vez)

1. Entra en [supabase.com](https://supabase.com), abre el proyecto de BlindSpots.
2. Menú de la izquierda → **SQL Editor** → **New query**.
3. Pega todo el contenido de [`1_crear_tabla.sql`](1_crear_tabla.sql) y pulsa **Run**.

Desde ese momento, cada partida queda registrada en la tabla `partidas`.

Si ya habías creado la tabla antes de que se añadieran las horas, ejecuta también
[`3_anadir_horas.sql`](3_anadir_horas.sql) (igual que el anterior). Hasta que lo hagas, Supabase
rechazará las filas nuevas.

Y si la creaste antes de que se añadieran los nombres, ejecuta también
[`4_anadir_nombres.sql`](4_anadir_nombres.sql).

## Ver las estadísticas

- **Table Editor** → tabla `partidas`: todas las filas, con filtros y orden.
- **Table Editor** → vista `partidas_resumen`: una línea por partida, con hora de inicio, hora de fin,
  duración y resultado.
- **SQL Editor**: pega una de las consultas de [`2_consultas.sql`](2_consultas.sql) (resumen,
  partidas por día, niveles, jugadores, países, dispositivos) y pulsa **Run**.

Solo tú puedes leerlas: la clave pública que usa la web permite añadir filas, pero no leerlas.

## Que no cuenten tus partidas de prueba

Abre una vez la web con `?nostats` al final de la dirección, por ejemplo
`https://gviciano.github.io/blindspot/?nostats`. Ese navegador deja de enviar estadísticas.
Para volver a activarlo, abre la web con `?stats`.
