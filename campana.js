// Campaña de BlindSpots.
//
// Cada nivel es un bloque { ... } con:
//   nombre:          nombre del nivel (opcional). Puede ser un texto o { es: '...', en: '...' }.
//   texto:           frase que se muestra durante el nivel (opcional, igual que nombre).
//   colores:         3, 4 o 5.
//   cartas:          estrellas de cada carta objetivo que recibe cada jugador.
//                    [3, 1] = una carta de 3★ y otra de 1★.
//   dados:           dados de cada color en la bolsa, según el número de jugadores: { 3: 6, 4: 10 }.
//   ganar:           estrellas que tiene que sumar el equipo para pasar el nivel, según el número
//                    de jugadores: { 3: 10, 4: 13 }. Si no se pone, hay que cumplir todos los objetivos.
//   modificadores:   true = el equipo tiene una ficha de cada modificador para todo el nivel:
//                    relanzar un dado, sumarle o restarle 1, y darle la vuelta (cara opuesta).
//   dado_gris:       true = se juega con dado gris y carta gris común.
//
// También se pueden usar las claves de la versión anterior: objetivos + estrellas (dificultades
// que pueden salir), ganar con un número fijo o ganar_por_jugador.
//
// La campaña solo admite los números de jugadores que aparecen en `dados` y `ganar` de todos
// los niveles (ahora, 3 y 4).
//
// Las estrellas necesarias de los niveles Gris 1 a Gris 5 están calculadas con la misma
// proporción que los niveles 1 a 10 (salvo el 6 de Gris 1 a 3 jugadores): ajústalas aquí.

const DADOS = { 3: 6, 4: 10 };

window.BLINDSPOTS_CAMPANA = [
  { colores: 3, cartas: [1],    dados: DADOS, ganar: { 3: 2, 4: 3 } },
  { colores: 3, cartas: [2],    dados: DADOS, ganar: { 3: 4, 4: 6 } },
  { colores: 3, cartas: [1, 1], dados: DADOS, ganar: { 3: 5, 4: 7 } },
  { colores: 3, cartas: [2, 2], dados: DADOS, ganar: { 3: 10, 4: 14 } },
  { colores: 3, cartas: [3],    dados: DADOS, ganar: { 3: 9, 4: 12 } },
  { colores: 3, cartas: [3, 1], dados: DADOS, ganar: { 3: 10, 4: 13 }, modificadores: true },
  { colores: 3, cartas: [3, 2], dados: DADOS, ganar: { 3: 13, 4: 18 }, modificadores: true },
  { colores: 3, cartas: [3, 3], dados: DADOS, ganar: { 3: 15, 4: 20 }, modificadores: true },
  { colores: 3, cartas: [4, 3], dados: DADOS, ganar: { 3: 18, 4: 25 }, modificadores: true },
  { colores: 3, cartas: [4, 4], dados: DADOS, ganar: { 3: 12, 4: 16 }, modificadores: true },
  { nombre: 'Gris 1', colores: 3, cartas: [3],    dados: DADOS, ganar: { 3: 6, 4: 8 },   dado_gris: true },
  { nombre: 'Gris 2', colores: 3, cartas: [1, 3], dados: DADOS, ganar: { 3: 10, 4: 13 }, dado_gris: true },
  { nombre: 'Gris 3', colores: 3, cartas: [2, 3], dados: DADOS, ganar: { 3: 12, 4: 16 }, dado_gris: true },
  { nombre: 'Gris 4', colores: 3, cartas: [3, 3], dados: DADOS, ganar: { 3: 14, 4: 19 }, dado_gris: true },
  { nombre: 'Gris 5', colores: 3, cartas: [5],    dados: DADOS, ganar: { 3: 10, 4: 13 }, dado_gris: true },
];
