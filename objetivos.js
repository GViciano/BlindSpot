// Objetivos de BlindSpots.
//
// El juego elige al azar entre los objetivos de esta lista que encajen con la
// partida: el rango de estrellas elegido y los colores en juego (un objetivo con
// morado o amarillo no sale en una partida de 3 colores).
//
// Cada objetivo es una línea con:
//   estrellas: dificultad, de 1 a 5.
//   tipo:      qué hay que conseguir (lista abajo).
//   color, color2, n: los datos que pida ese tipo.
//
// Colores: 'azul', 'naranja', 'verde', 'morado', 'amarillo'.
//
// Tipos:
//   ninguno            Ningún dado de `color`.
//   exactamente        Exactamente `n` dados de `color`.
//   al_menos           Al menos `n` dados de `color`.
//   como_maximo        Como máximo `n` dados de `color`.
//   suma_mayor         La suma de `color` es mayor que la de `color2`.
//   mas_dados          Más dados de `color` que de `color2`.
//   suma_al_menos      Los dados de `color` suman `n` o más.
//   colores_exactos    Dados de exactamente `n` colores distintos.
//   todos_colores      Al menos un dado de cada color en juego.
//   total_al_menos     Al menos `n` dados en total.
//   total_como_maximo  Como máximo `n` dados en total.
//
// Las estrellas de esta lista son provisionales.

window.BLINDSPOTS_OBJETIVOS = [
  { estrellas: 1, tipo: 'ninguno', color: 'azul' },
  { estrellas: 1, tipo: 'al_menos', color: 'azul', n: 2 },
  { estrellas: 2, tipo: 'al_menos', color: 'azul', n: 3 },
  { estrellas: 2, tipo: 'como_maximo', color: 'azul', n: 1 },
  { estrellas: 3, tipo: 'exactamente', color: 'azul', n: 2 },
  { estrellas: 4, tipo: 'exactamente', color: 'azul', n: 3 },
  { estrellas: 3, tipo: 'suma_al_menos', color: 'azul', n: 12 },
  { estrellas: 4, tipo: 'suma_al_menos', color: 'azul', n: 15 },
  { estrellas: 1, tipo: 'ninguno', color: 'naranja' },
  { estrellas: 1, tipo: 'al_menos', color: 'naranja', n: 2 },
  { estrellas: 2, tipo: 'al_menos', color: 'naranja', n: 3 },
  { estrellas: 2, tipo: 'como_maximo', color: 'naranja', n: 1 },
  { estrellas: 3, tipo: 'exactamente', color: 'naranja', n: 2 },
  { estrellas: 4, tipo: 'exactamente', color: 'naranja', n: 3 },
  { estrellas: 3, tipo: 'suma_al_menos', color: 'naranja', n: 12 },
  { estrellas: 4, tipo: 'suma_al_menos', color: 'naranja', n: 15 },
  { estrellas: 1, tipo: 'ninguno', color: 'verde' },
  { estrellas: 1, tipo: 'al_menos', color: 'verde', n: 2 },
  { estrellas: 2, tipo: 'al_menos', color: 'verde', n: 3 },
  { estrellas: 2, tipo: 'como_maximo', color: 'verde', n: 1 },
  { estrellas: 3, tipo: 'exactamente', color: 'verde', n: 2 },
  { estrellas: 4, tipo: 'exactamente', color: 'verde', n: 3 },
  { estrellas: 3, tipo: 'suma_al_menos', color: 'verde', n: 12 },
  { estrellas: 4, tipo: 'suma_al_menos', color: 'verde', n: 15 },
  { estrellas: 1, tipo: 'ninguno', color: 'morado' },
  { estrellas: 1, tipo: 'al_menos', color: 'morado', n: 2 },
  { estrellas: 2, tipo: 'al_menos', color: 'morado', n: 3 },
  { estrellas: 2, tipo: 'como_maximo', color: 'morado', n: 1 },
  { estrellas: 3, tipo: 'exactamente', color: 'morado', n: 2 },
  { estrellas: 4, tipo: 'exactamente', color: 'morado', n: 3 },
  { estrellas: 3, tipo: 'suma_al_menos', color: 'morado', n: 12 },
  { estrellas: 4, tipo: 'suma_al_menos', color: 'morado', n: 15 },
  { estrellas: 1, tipo: 'ninguno', color: 'amarillo' },
  { estrellas: 1, tipo: 'al_menos', color: 'amarillo', n: 2 },
  { estrellas: 2, tipo: 'al_menos', color: 'amarillo', n: 3 },
  { estrellas: 2, tipo: 'como_maximo', color: 'amarillo', n: 1 },
  { estrellas: 3, tipo: 'exactamente', color: 'amarillo', n: 2 },
  { estrellas: 4, tipo: 'exactamente', color: 'amarillo', n: 3 },
  { estrellas: 3, tipo: 'suma_al_menos', color: 'amarillo', n: 12 },
  { estrellas: 4, tipo: 'suma_al_menos', color: 'amarillo', n: 15 },
  { estrellas: 2, tipo: 'suma_mayor', color: 'azul', color2: 'naranja' },
  { estrellas: 2, tipo: 'mas_dados', color: 'naranja', color2: 'azul' },
  { estrellas: 2, tipo: 'suma_mayor', color: 'naranja', color2: 'verde' },
  { estrellas: 2, tipo: 'mas_dados', color: 'verde', color2: 'naranja' },
  { estrellas: 2, tipo: 'suma_mayor', color: 'verde', color2: 'azul' },
  { estrellas: 2, tipo: 'mas_dados', color: 'azul', color2: 'verde' },
  { estrellas: 2, tipo: 'suma_mayor', color: 'morado', color2: 'amarillo' },
  { estrellas: 2, tipo: 'mas_dados', color: 'amarillo', color2: 'morado' },
  { estrellas: 2, tipo: 'suma_mayor', color: 'amarillo', color2: 'azul' },
  { estrellas: 2, tipo: 'mas_dados', color: 'azul', color2: 'amarillo' },
  { estrellas: 2, tipo: 'suma_mayor', color: 'naranja', color2: 'morado' },
  { estrellas: 2, tipo: 'mas_dados', color: 'morado', color2: 'naranja' },
  { estrellas: 2, tipo: 'todos_colores' },
  { estrellas: 3, tipo: 'colores_exactos', n: 3 },
  { estrellas: 4, tipo: 'colores_exactos', n: 2 },
  { estrellas: 5, tipo: 'colores_exactos', n: 1 },
  { estrellas: 3, tipo: 'total_al_menos', n: 9 },
  { estrellas: 4, tipo: 'total_como_maximo', n: 5 },
  { estrellas: 5, tipo: 'exactamente', color: 'verde', n: 4 },
  { estrellas: 5, tipo: 'suma_al_menos', color: 'azul', n: 18 },
];
