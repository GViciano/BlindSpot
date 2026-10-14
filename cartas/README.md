# Cartas de objetivos

`cartas.pdf` tiene una carta por cada objetivo de `objetivos.js`, en tamaño póquer (63,5 × 88,9 mm), 9 por hoja A4, y una última hoja de reversos. Las cartas no llevan texto: solo dados de colores, caras de dado, números y símbolos, así que sirven en cualquier idioma.

Para regenerarlo después de cambiar `objetivos.js`:

```bash
python3 cartas/generar_cartas.py   # crea cartas/cartas.html
node cartas/imprimir_pdf.js        # crea cartas/cartas.pdf (necesita Playwright)
```

Al imprimir, elige tamaño real (100 %), sin ajustar a la página.
