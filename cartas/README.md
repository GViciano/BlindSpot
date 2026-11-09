# Cartas de objetivos

`cartas.pdf` tiene una carta por cada objetivo de `objetivos.js`, con su texto en inglés tal como aparece en la app, en tamaño póquer (63,5 × 88,9 mm), 9 por hoja A4, una hoja de reversos las 7 cartas grises del dado gris (G1–G7) con sus reversos grises las 9 cartas negras del dado negro (N1–N9) con sus reversos negros y, al final, las 4 cartas de acción (A1–A4) con sus reversos. Las cartas no llevan texto: solo dados de colores, caras de dado, números y símbolos, así que sirven en cualquier idioma.

Para regenerarlo después de cambiar `objetivos.js`:

```bash
node cartas/textos_app.js           # copia los textos de la app (inglés) y rehace listado.md
python3 cartas/generar_cartas.py   # crea cartas/cartas.html
node cartas/imprimir_pdf.js        # crea cartas/cartas.pdf (necesita Playwright)
```

Al imprimir, elige tamaño real (100 %), sin ajustar a la página.

## Cómo leer las cartas negras

Arriba, el dado negro con la flecha: la carta es para quien tenga ese dado. En el centro, el dado con la marca roja ✕ es el que se elimina al final:

- N1 / N2: tu dado de valor más bajo / más alto.
- N3: un dado con el mismo valor que el dado negro.
- N4 / N5: un dado del color del que más / menos tengas (▲ / ▼).
- N6: 2 dados al azar (?).
- N7: dos dados del mismo valor.
- N8 / N9: un dado de valor menor o igual / mayor o igual que el dado negro.

## Cómo leer las cartas de acción

Llevan un rayo arriba. A1: relanzar (dado con flecha circular). A2: ±1. A3: invertir (2 ↔ 5, cara opuesta). A4: eliminar (el dado vuelve a la bolsa).
