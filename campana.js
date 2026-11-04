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
//   modificadores:   true = acciones especiales: relanzar un dado, sumarle o restarle 1, invertirlo
//                    (cara opuesta) y eliminarlo (vuelve a la bolsa). Con 3 jugadores salen 3 de las 4
//                    al azar; con 4 jugadores, las 4. Cada jugador puede usar una en todo el nivel, en
//                    cualquier momento y sobre cualquier dado a la vista; la acción usada ya no está
//                    disponible para nadie más.
//   dado_gris:       true = se juega con dado gris y carta gris común.
//   dado_negro:      true = Bomba: cada ronda se tira además un dado negro con una carta negra.
//                    Cada jugador solo puede acabar con un dado negro; al final, quien lo tiene
//                    aplica la carta a sus propios dados.
//   dados_por_ronda: dados de colores que se sacan cada ronda, según el número de jugadores:
//                    { 3: 6, 4: 8 }. Si no se pone, (jugadores × 2) − 1.
//   intro:           explicación que se muestra antes de empezar el nivel:
//                    { titulo: { es, en }, texto: { es, en } }. En el texto, cada salto de
//                    línea (\n) empieza un párrafo nuevo.
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
const DADOS_BOMBA = { 3: 6, 4: 11 };
const POR_RONDA_BOMBA = { 3: 6, 4: 8 };

const INTRO_ACCIONES = {
  titulo: { es: 'Nuevo: acciones especiales', en: 'New: special actions' },
  texto: {
    es: 'Desde este nivel el equipo tiene acciones especiales: relanzar un dado, sumarle o restarle 1, invertirlo (poner la cara opuesta: el 1 pasa a 6, el 2 a 5…) y eliminarlo (vuelve a la bolsa).\n'
      + 'Con 3 jugadores salen 3 de las 4 acciones al azar; con 4 jugadores, las 4.\n'
      + 'Cada jugador puede usar una sola acción en todo el nivel, en cualquier momento y sobre cualquier dado a la vista: los de la mesa o los que ya tiene alguien. La acción usada ya no está disponible para nadie más, así que poneos de acuerdo.',
    en: 'From this level on the team has special actions: reroll a die, add or subtract 1, flip it (turn it to the opposite face: 1 becomes 6, 2 becomes 5…) and remove it (it goes back to the bag).\n'
      + 'With 3 players, 3 of the 4 actions come up at random; with 4 players, all 4.\n'
      + 'Each player can use just one action during the whole level, at any time and on any visible die: on the table or already in someone’s area. A used action is gone for everyone, so agree on it together.',
  },
};
const INTRO_GRIS = {
  titulo: { es: 'Nuevo: el dado gris', en: 'New: the grey die' },
  texto: {
    es: 'En estos niveles, en la primera ronda se tira además un dado gris y sale una carta gris que ve todo el mundo.\n'
      + 'Quien acabe la partida con el dado gris tiene que cumplir la carta gris; si no, el equipo pierde el nivel aunque llegue a las estrellas.\n'
      + 'El dado gris cuenta como dado, para la suma y para los números, pero no cuenta como color. Pensad bien a quién le conviene llevárselo.',
    en: 'In these levels, in the first round a grey die is rolled as well and a grey card that everyone can see is drawn.\n'
      + 'Whoever ends the game with the grey die must meet the grey card; otherwise the team loses the level even if it reaches the stars.\n'
      + 'The grey die counts as a die, for sums and for numbers, but not as a colour. Think carefully about who should take it.',
  },
};
const INTRO_BOMBA = {
  titulo: { es: 'Nuevo: el dado negro (Bomba)', en: 'New: the black die (Bomb)' },
  texto: {
    es: 'En estos niveles se sacan más dados por ronda (6 con 3 jugadores, 8 con 4) y, además, cada ronda se tira un dado negro con una carta negra que ve todo el mundo.\n'
      + 'Cada jugador solo puede acabar con UN dado negro: si ya tienes uno, no puedes coger un grupo que lleve otro. Cuidado con quien reparte: si le queda un grupo con un dado negro y ya tiene uno, el equipo pierde el nivel en el acto.\n'
      + 'Al final de la partida explotan las bombas: quien tiene un dado negro aplica su carta a sus propios dados y elige cuál elimina (por ejemplo, «Elimina un dado de valor mayor»: el que más puntos tenga de los suyos). Si ningún dado cumple la carta, no pasa nada.\n'
      + 'El dado negro cuenta como dado, para la suma y para los números, pero no cuenta como color.',
    en: 'In these levels more dice are dealt each round (6 with 3 players, 8 with 4) and, on top of that, every round a black die is rolled with a black card that everyone can see.\n'
      + 'Each player can end up with only ONE black die: if you already have one, you can’t take a group that has another. Watch out for the dealer: if they are left a group with a black die and already have one, the team loses the level on the spot.\n'
      + 'At the end of the game the bombs go off: whoever has a black die applies its card to their own dice and chooses which one to remove (for example, “Remove your highest die”: the one with the most pips among their own). If no die fits the card, nothing happens.\n'
      + 'The black die counts as a die, for sums and for numbers, but not as a colour.',
  },
};

window.BLINDSPOTS_CAMPANA = [
  { colores: 3, cartas: [1],    dados: DADOS, ganar: { 3: 2, 4: 3 } },
  { colores: 3, cartas: [2],    dados: DADOS, ganar: { 3: 4, 4: 6 } },
  { colores: 3, cartas: [1, 1], dados: DADOS, ganar: { 3: 5, 4: 7 } },
  { colores: 3, cartas: [2, 2], dados: DADOS, ganar: { 3: 10, 4: 14 } },
  { colores: 3, cartas: [3],    dados: DADOS, ganar: { 3: 9, 4: 12 } },
  { colores: 3, cartas: [3, 1], dados: DADOS, ganar: { 3: 10, 4: 13 }, modificadores: true, intro: INTRO_ACCIONES },
  { colores: 3, cartas: [3, 2], dados: DADOS, ganar: { 3: 13, 4: 18 }, modificadores: true },
  { colores: 3, cartas: [3, 3], dados: DADOS, ganar: { 3: 15, 4: 20 }, modificadores: true },
  { colores: 3, cartas: [4, 3], dados: DADOS, ganar: { 3: 18, 4: 25 }, modificadores: true },
  { colores: 3, cartas: [4, 4], dados: DADOS, ganar: { 3: 12, 4: 16 }, modificadores: true },
  { nombre: 'Gris 1', colores: 3, cartas: [3],    dados: DADOS, ganar: { 3: 6, 4: 8 },   dado_gris: true, intro: INTRO_GRIS },
  { nombre: 'Gris 2', colores: 3, cartas: [1, 3], dados: DADOS, ganar: { 3: 10, 4: 13 }, dado_gris: true },
  { nombre: 'Gris 3', colores: 3, cartas: [2, 3], dados: DADOS, ganar: { 3: 12, 4: 16 }, dado_gris: true },
  { nombre: 'Gris 4', colores: 3, cartas: [3, 3], dados: DADOS, ganar: { 3: 14, 4: 19 }, dado_gris: true },
  { nombre: 'Gris 5', colores: 3, cartas: [5],    dados: DADOS, ganar: { 3: 10, 4: 13 }, dado_gris: true },
  { nombre: 'Bomba 1', colores: 3, cartas: [4],       dados: DADOS_BOMBA, dados_por_ronda: POR_RONDA_BOMBA, ganar: { 3: 8, 4: 12 },  dado_negro: true, intro: INTRO_BOMBA },
  { nombre: 'Bomba 2', colores: 3, cartas: [2, 3],    dados: DADOS_BOMBA, dados_por_ronda: POR_RONDA_BOMBA, ganar: { 3: 12, 4: 17 }, dado_negro: true },
  { nombre: 'Bomba 3', colores: 3, cartas: [1, 2, 3], dados: DADOS_BOMBA, dados_por_ronda: POR_RONDA_BOMBA, ganar: { 3: 15, 4: 20 }, dado_negro: true },
  { nombre: 'Bomba 4', colores: 3, cartas: [3, 4],    dados: DADOS_BOMBA, dados_por_ronda: POR_RONDA_BOMBA, ganar: { 3: 18, 4: 24 }, dado_negro: true },
  { nombre: 'Bomba 5', colores: 3, cartas: [2, 2, 3], dados: DADOS_BOMBA, dados_por_ronda: POR_RONDA_BOMBA, ganar: { 3: 20, 4: 26 }, dado_negro: true },
  { nombre: '4 colores 1', colores: 4, cartas: [2, 3],    dados: DADOS, ganar: { 3: 13, 4: 17 } },
  { nombre: '4 colores 2', colores: 4, cartas: [3, 3],    dados: DADOS, ganar: { 3: 15, 4: 20 } },
  { nombre: '4 colores 3', colores: 4, cartas: [3, 4],    dados: DADOS, ganar: { 3: 21, 4: 24 } },
  { nombre: '4 colores 4', colores: 4, cartas: [2, 2, 3], dados: DADOS, ganar: { 3: 19, 4: 23 } },
  { nombre: '4 colores 5', colores: 4, cartas: [3, 3, 3], dados: DADOS, ganar: { 3: 24, 4: 33 } },
];
