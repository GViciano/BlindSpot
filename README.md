# BlindSpots

Juego cooperativo de dados y deducción para 3–5 jugadores.

> Ves la misión de todos. Todos ven la tuya. Nadie ve la suya.

Todo el juego está en `index.html`, sin dependencias ni build.

## Idioma

La web está en español y en inglés. Cada jugador elige su idioma con el selector ES / EN (arriba a la derecha) y se recuerda en su navegador; en una partida online cada uno la ve en el suyo.

## Modos de juego

- **En este dispositivo:** varias personas se pasan el móvil u ordenador, o una persona juega con bots.
- **Online, sin cuenta:** quien crea la partida recibe un código de 4 caracteres. Los demás abren la página, eligen «Online» y se unen con ese código. Los navegadores se conectan entre sí por WebRTC con [PeerJS](https://peerjs.com/); su servidor público solo se usa para que se encuentren. La partida vive en el navegador del anfitrión, que debe mantener la página abierta.

## Ajustes de la partida

- **Colores:** 3 (azul, naranja, verde), 4 (más morado) o 5 (más amarillo). Con cualquier número de jugadores se puede jugar con 3, 4 o 5 colores.
- **Dados:** la bolsa empieza con 15 dados de cada color en juego. En cada ronda, quien reparte saca al azar (jugadores × 2) − 1 dados; los repartidos no vuelven a la bolsa.
- **Objetivos por jugador:** de 1 a 3. La misión de cada jugador se cumple si cumple todos sus objetivos.
- **Dificultad:** se marcan las estrellas que se quieran (1★ a 5★, por ejemplo solo 2★ y 4★). Los objetivos se reparten al azar entre los que tienen esas estrellas y usan colores en juego.

- **Estrellas del equipo para ganar:** con «Todas» hay que cumplir todos los objetivos. Con un número (por ejemplo 4★), se suman las estrellas de los objetivos que cumple cada jugador y el equipo gana si llega a esa cifra entre todos.

## Objetivos

Los objetivos están en [`objetivos.js`](objetivos.js), uno por línea, con sus estrellas (1–5), su tipo y sus datos. Al principio del archivo están todos los tipos disponibles: de colores (ningún azul, exactamente 2 verdes…) y de números (sin pares, exactamente 2 dados con el mismo número, ningún dado mayor que 4, suma total, escaleras, dos parejas, full…) y de comparación con los demás (más dados que nadie, menos puntos que nadie…). Los objetivos de tipo «al menos» se muestran sin esas palabras («2 dados azules» = 2 o más) y, como los de «como máximo» y los de suma, llevan un *: si se consigue la cifra exacta dan 1★ extra. Para cambiar los objetivos basta con editar ese archivo; el juego no necesita cambios.

## Publicación

La página se sirve con GitHub Pages desde la rama `main` (carpeta raíz).
