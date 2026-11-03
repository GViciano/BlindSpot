// Campaña de BlindSpots.
//
// Cada nivel es un bloque { ... } con:
//   nombre:             nombre del nivel. Puede ser un texto o { es: '...', en: '...' }.
//   texto:              frase que se muestra durante el nivel (opcional, igual que nombre).
//   colores:            3, 4 o 5.
//   objetivos:          objetivos por jugador: 1, 2 o 3.
//   estrellas:          dificultades de los objetivos que pueden salir, por ejemplo [1, 2] o [2, 3, 4].
//   ganar:              estrellas que tiene que sumar el equipo para ganar (un número fijo)...
//   ganar_por_jugador:  ...o estrellas por jugador (se multiplica por el número de jugadores).
//                       Si no pones ninguna de las dos, hay que cumplir todos los objetivos.
//   dado_gris:          true para jugar el nivel con dado gris y carta gris.
//
// Al superar un nivel se desbloquea el siguiente. Para añadir, quitar o cambiar niveles
// basta con editar esta lista.

window.BLINDSPOTS_CAMPANA = [
  {
    nombre: { es: 'Primeros pasos', en: 'First steps' },
    texto: { es: 'Tres colores y un objetivo sencillo cada uno. Hay que cumplirlos todos.', en: 'Three colours and one easy objective each. Complete them all.' },
    colores: 3, objetivos: 1, estrellas: [1, 2],
  },
  {
    nombre: { es: 'Calentando motores', en: 'Warming up' },
    texto: { es: 'Los objetivos empiezan a complicarse.', en: 'The objectives start to get harder.' },
    colores: 3, objetivos: 1, estrellas: [1, 2, 3],
  },
  {
    nombre: { es: 'Un color más', en: 'One more colour' },
    texto: { es: 'Entra el morado en la bolsa.', en: 'Purple joins the bag.' },
    colores: 4, objetivos: 1, estrellas: [2, 3],
  },
  {
    nombre: { es: 'Doble misión', en: 'Double mission' },
    texto: { es: 'Dos objetivos por jugador, pero no hace falta cumplirlo todo: sumad 3★ por jugador.', en: 'Two objectives per player, but you don’t need them all: earn 3★ per player.' },
    colores: 4, objetivos: 2, estrellas: [1, 2], ganar_por_jugador: 3,
  },
  {
    nombre: { es: 'El dado gris', en: 'The grey die' },
    texto: { es: 'Aparece el dado gris y su carta común. Cumplid todos los objetivos y la carta gris.', en: 'The grey die and its common card appear. Complete every objective and the grey card.' },
    colores: 4, objetivos: 1, estrellas: [2, 3], dado_gris: true,
  },
  {
    nombre: { es: 'Arcoíris', en: 'Rainbow' },
    texto: { es: 'Los cinco colores en juego. Sumad 4★ por jugador.', en: 'All five colours in play. Earn 4★ per player.' },
    colores: 5, objetivos: 2, estrellas: [2, 3], ganar_por_jugador: 4,
  },
  {
    nombre: { es: 'Gris y arcoíris', en: 'Grey and rainbow' },
    texto: { es: 'Cinco colores, dado gris y objetivos de hasta 4★.', en: 'Five colours, the grey die and objectives up to 4★.' },
    colores: 5, objetivos: 2, estrellas: [2, 3, 4], ganar_por_jugador: 4, dado_gris: true,
  },
  {
    nombre: { es: 'Triple misión', en: 'Triple mission' },
    texto: { es: 'Tres objetivos por jugador. Sumad 6★ por jugador.', en: 'Three objectives per player. Earn 6★ per player.' },
    colores: 5, objetivos: 3, estrellas: [2, 3], ganar_por_jugador: 6,
  },
  {
    nombre: { es: 'Sin margen', en: 'No room for error' },
    texto: { es: 'Objetivos difíciles y dado gris. Sumad 7★ por jugador.', en: 'Hard objectives and the grey die. Earn 7★ per player.' },
    colores: 5, objetivos: 3, estrellas: [3, 4], ganar_por_jugador: 7, dado_gris: true,
  },
  {
    nombre: { es: 'Maestros de BlindSpots', en: 'BlindSpots masters' },
    texto: { es: 'El reto final: tres objetivos de 3★ a 5★ cada uno, dado gris, y hay que cumplirlo todo.', en: 'The final challenge: three objectives of 3★ to 5★ each, the grey die, and everything must be completed.' },
    colores: 5, objetivos: 3, estrellas: [3, 4, 5], dado_gris: true,
  },
];
