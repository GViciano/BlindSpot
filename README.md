# BlindSpots

Juego cooperativo de dados y deducción para 3–5 jugadores.

> Ves la misión de todos. Todos ven la tuya. Nadie ve la suya.

Todo el juego está en `index.html`, sin dependencias ni build.

## Idioma

La web está en español y en inglés. Cada jugador elige su idioma con el selector ES / EN (arriba a la derecha) y se recuerda en su navegador; en una partida online cada uno la ve en el suyo.

## Modos de juego

- **En este dispositivo:** varias personas se pasan el móvil u ordenador, o una persona juega con bots.
- **Online, sin cuenta:** quien crea la partida recibe un código de 4 caracteres. Los demás abren la página, eligen «Online» y se unen con ese código. La partida pasa por el servicio en tiempo real de [Supabase](https://supabase.com/) (un canal por código de partida), que funciona con cualquier red. Si Supabase no responde, el juego usa una conexión directa entre navegadores con [PeerJS](https://peerjs.com/). La partida vive en el navegador del anfitrión, que debe mantener la página abierta.

## Ajustes de la partida

- **Colores:** 3 (azul, naranja, verde), 4 (más morado) o 5 (más amarillo). Con cualquier número de jugadores se puede jugar con 3, 4 o 5 colores.
- **Dados:** la bolsa empieza con 15 dados de cada color en juego. En cada ronda, quien reparte saca al azar (jugadores × 2) − 1 dados; los repartidos no vuelven a la bolsa.
- **Objetivos por jugador:** de 1 a 3. La misión de cada jugador se cumple si cumple todos sus objetivos.
- **Dificultad:** se marcan las estrellas que se quieran (1★ a 5★, por ejemplo solo 2★ y 4★). Los objetivos se reparten al azar entre los que tienen esas estrellas y usan colores en juego.

- **Estrellas del equipo para ganar:** con «Todas» hay que cumplir todos los objetivos. Con un número (por ejemplo 4★), se suman las estrellas de los objetivos que cumple cada jugador y el equipo gana si llega a esa cifra entre todos.

- **Dado gris (opcional):** en la primera ronda se tira además un dado gris (del 1 al 6) y sale una de las 7 cartas grises, común para todos. Quien acabe con el dado gris tiene que cumplirla para que el equipo gane.

## Campaña

Además de la partida libre, hay un modo **Campaña**: una serie de niveles con los ajustes ya fijados. Al superar un nivel se pasa al siguiente (y queda desbloqueado en ese navegador); si se pierde, se reintenta. Los niveles están en [`campana.js`](campana.js); para cada uno se indica:

- `cartas`: estrellas de cada carta objetivo por jugador, por ejemplo `[3, 1]`.
- `dados`: dados de cada color en la bolsa según el número de jugadores, por ejemplo `{ 3: 6, 4: 10 }`.
- `ganar`: estrellas necesarias según el número de jugadores, por ejemplo `{ 3: 10, 4: 13 }`.
- `modificadores: true`: acciones especiales (relanzar, +/− 1, invertir dado y eliminar dado). Con 3 jugadores salen 3 de las 4 al azar; con 4, las 4. Cada jugador puede usar una en todo el nivel, en cualquier momento y sobre cualquier dado a la vista, y la acción usada ya no está disponible para nadie más.
- `dado_gris: true`: dado gris y carta gris común.
- `dado_negro: true`: Bomba. Cada ronda se tira además un dado negro con una de las 7 cartas negras. Cada jugador solo puede acabar con un dado negro (si a quien reparte le toca un segundo, el nivel se pierde) y, al final, quien lo tiene aplica la carta a sus propios dados.
- `dados_por_ronda`: dados de colores por ronda según el número de jugadores, por ejemplo `{ 3: 6, 4: 8 }`.
- `intro`: explicación que se muestra antes de empezar el nivel (ahora, antes de los niveles 6, 11 y 16).

La campaña actual tiene 20 niveles y es para 3 o 4 jugadores: 1–5 de iniciación, 6–10 con acciones especiales, 11–15 con dado gris y 16–20 con dado negro.

## Objetivos

Los objetivos están en [`objetivos.js`](objetivos.js), uno por línea, con sus estrellas (1–5), su tipo y sus datos. Al principio del archivo están todos los tipos disponibles: de colores (ningún azul, exactamente 2 verdes…) y de números (sin pares, exactamente 2 dados con el mismo número, ningún dado mayor que 4, suma total, escaleras, dos parejas, full…) y de comparación con los demás (más dados que nadie, menos puntos que nadie…). Los objetivos de tipo «al menos» se muestran sin esas palabras («2 dados azules» = 2 o más) y, como los de «como máximo» y los de suma, llevan un *: si se consigue la cifra exacta dan 1★ extra. Para cambiar los objetivos basta con editar ese archivo; el juego no necesita cambios.

## Publicación

La página se sirve con GitHub Pages desde la rama `main` (carpeta raíz).
