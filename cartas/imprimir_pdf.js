// Convierte cartas.html en cartas.pdf (A4, sin márgenes) con el Chromium de Playwright.
// Uso: node cartas/imprimir_pdf.js
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'cartas.html'));
  await page.pdf({ path: path.join(__dirname, 'cartas.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  console.log('cartas.pdf listo');
})();
