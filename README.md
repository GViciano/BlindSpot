# BlindSpots

Juego cooperativo de dados y deducción para 3–5 jugadores.

> Ves la misión de todos. Todos ven la tuya. Nadie ve la suya.

Todo el juego está en `index.html`, sin dependencias ni build.

## Modos de juego

- **En este dispositivo:** varias personas se pasan el móvil u ordenador, o una persona juega con bots.
- **Online, sin cuenta:** quien crea la partida recibe un código de 4 caracteres. Los demás abren la página, eligen «Online» y se unen con ese código. Los navegadores se conectan entre sí por WebRTC con [PeerJS](https://peerjs.com/); su servidor público solo se usa para que se encuentren. La partida vive en el navegador del anfitrión, que debe mantener la página abierta.

## Niveles

1. **Iniciación:** 3 colores (azul, naranja, verde) y una misión por jugador.
2. **Avanzado:** 5 colores y misiones de suma y de total de dados.
3. **Experto:** 5 colores y dos misiones por jugador.

## Publicación

La página se sirve con GitHub Pages desde la rama `main` (carpeta raíz).
