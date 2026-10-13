// Objetivos de BlindSpots.
//
// El juego elige al azar entre los objetivos de esta lista que encajen con la
// partida: el rango de estrellas elegido y los colores en juego (un objetivo con
// morado o amarillo no sale en una partida de 3 colores).
//
// Cada objetivo es una línea con:
//   estrellas: dificultad, de 1 a 5.
//   tipo:      qué hay que conseguir (lista abajo).
//   color, color2, n, numero: los datos que pida ese tipo.
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
// Tipos que miran el número de los dados (sin importar el color):
//   sin_pares          Ningún dado con número par (2, 4, 6).
//   sin_impares        Ningún dado con número impar (1, 3, 5).
//   pares_exactos      Exactamente `n` dados con número par.
//   impares_exactos    Exactamente `n` dados con número impar.
//   mas_pares          Más dados con número par que con número impar.
//   mas_impares        Más dados con número impar que con número par.
//   repetidos_exactos  Exactamente `n` dados con el mismo número (ninguno sale más de `n` veces).
//   repetidos_al_menos Al menos `n` dados con el mismo número.
//   valor_maximo       Ningún dado mayor que `n`.
//   valor_minimo       Ningún dado menor que `n`.
//   sin_numero         Ningún dado con el número `numero`.
//   numero_al_menos    Al menos `n` dados con el número `numero`.
//   suma_total_maxima  Todos tus dados suman `n` o menos.
//   suma_total_minima  Todos tus dados suman `n` o más.
//   suma_total_par     Todos tus dados suman un número par.
//   escalera           `n` números seguidos (por ejemplo 2-3-4-5), de cualquier color.
//   escalera_color     `n` números seguidos en dados del mismo color.
//   dos_parejas        Dos números distintos que salgan al menos 2 veces cada uno.
//   full               Un número que salga al menos 3 veces y otro al menos 2.
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
  { estrellas: 3, tipo: 'total_al_menos', n: 6 },
  { estrellas: 4, tipo: 'total_como_maximo', n: 5 },
  { estrellas: 5, tipo: 'exactamente', color: 'verde', n: 4 },
  { estrellas: 5, tipo: 'suma_al_menos', color: 'azul', n: 18 },

  // Objetivos sobre los números de los dados
  { estrellas: 3, tipo: 'sin_pares' },
  { estrellas: 3, tipo: 'sin_impares' },
  { estrellas: 3, tipo: 'pares_exactos', n: 2 },
  { estrellas: 3, tipo: 'pares_exactos', n: 3 },
  { estrellas: 3, tipo: 'impares_exactos', n: 2 },
  { estrellas: 4, tipo: 'impares_exactos', n: 4 },
  { estrellas: 2, tipo: 'mas_pares' },
  { estrellas: 2, tipo: 'mas_impares' },
  { estrellas: 3, tipo: 'repetidos_exactos', n: 2 },
  { estrellas: 4, tipo: 'repetidos_exactos', n: 3 },
  { estrellas: 2, tipo: 'repetidos_al_menos', n: 3 },
  { estrellas: 3, tipo: 'repetidos_al_menos', n: 4 },
  { estrellas: 5, tipo: 'repetidos_al_menos', n: 5 },
  { estrellas: 2, tipo: 'valor_maximo', n: 5 },
  { estrellas: 3, tipo: 'valor_maximo', n: 4 },
  { estrellas: 4, tipo: 'valor_maximo', n: 3 },
  { estrellas: 2, tipo: 'valor_minimo', n: 2 },
  { estrellas: 3, tipo: 'valor_minimo', n: 3 },
  { estrellas: 4, tipo: 'valor_minimo', n: 4 },
  { estrellas: 1, tipo: 'sin_numero', numero: 6 },
  { estrellas: 1, tipo: 'sin_numero', numero: 1 },
  { estrellas: 1, tipo: 'sin_numero', numero: 3 },
  { estrellas: 2, tipo: 'numero_al_menos', numero: 6, n: 2 },
  { estrellas: 2, tipo: 'numero_al_menos', numero: 1, n: 2 },
  { estrellas: 3, tipo: 'numero_al_menos', numero: 6, n: 3 },
  { estrellas: 3, tipo: 'numero_al_menos', numero: 4, n: 3 },
  { estrellas: 3, tipo: 'suma_total_maxima', n: 20 },
  { estrellas: 4, tipo: 'suma_total_maxima', n: 15 },
  { estrellas: 2, tipo: 'suma_total_minima', n: 15 },
  { estrellas: 3, tipo: 'suma_total_minima', n: 20 },
  { estrellas: 4, tipo: 'suma_total_minima', n: 25 },
  { estrellas: 5, tipo: 'suma_total_minima', n: 30 },
  { estrellas: 1, tipo: 'suma_total_par' },

  // Combinaciones de números
  { estrellas: 2, tipo: 'escalera', n: 3 },
  { estrellas: 3, tipo: 'escalera', n: 4 },
  { estrellas: 4, tipo: 'escalera', n: 5 },
  { estrellas: 5, tipo: 'escalera', n: 6 },
  { estrellas: 4, tipo: 'escalera_color', n: 3 },
  { estrellas: 5, tipo: 'escalera_color', n: 4 },
  { estrellas: 3, tipo: 'dos_parejas' },
  { estrellas: 4, tipo: 'full' },
];
