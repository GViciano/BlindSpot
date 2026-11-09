// Saves the English texts the app shows for every card into cartas/textos_en.json, so the
// printed cards say exactly the same as the app. Run it after changing objetivos.js or the texts:
//   node cartas/textos_app.js      (needs Playwright's Chromium)
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

const ROOT = path.join(__dirname, '..');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // The game's code lives in a closure: expose what we need before it closes.
  await page.route('**/index.html', async route => {
    let body = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
    const i = body.lastIndexOf('})();');
    body = body.slice(0, i) + 'window.__T = { CATALOGUE, missionText, bonusText, BONUS_TYPES, I18N, setLang: l => { LANG = l; } };\n' + body.slice(i);
    await route.fulfill({ body, contentType: 'text/html' });
  });
  await page.route('**/*.js', route => route.fulfill({ body: fs.readFileSync(path.join(ROOT, path.basename(new URL(route.request().url()).pathname)), 'utf8'), contentType: 'application/javascript' }));
  await page.goto('http://blindspots.local/index.html');
  const texts = await page.evaluate(() => {
    const T = window.__T;
    T.setLang('en');
    const plain = h => h.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
    const en = T.I18N.en;
    const call = (v, ...a) => (typeof v === 'function' ? v(...a) : v);
    if (T.CATALOGUE.bad.length) throw new Error('objetivos.js has entries the game skips: ' + T.CATALOGUE.bad.join(', '));
    return {
      objectives: T.CATALOGUE.list.map(m => ({ id: m.id, text: plain(T.missionText(m)), bonus: T.BONUS_TYPES.includes(m.t) ? plain(T.bonusText(m)) : '' })),
      grey: Array.from({ length: 7 }, (_, k) => plain(call(en['greyRule' + k]))),
      black: Array.from({ length: 9 }, (_, k) => plain(call(en['blackCard' + k]))),
      actions: [
        'Reroll a die.',
        'Add or subtract 1 to a die (never below 1 or above 6).',
        'Flip a die to its opposite face (1↔6, 2↔5, 3↔4).',
        'Remove a die: it goes back into the bag.',
      ],
    };
  });
  // The Spanish card list (cartas/listado.md) is rebuilt from the app too.
  const es = await page.evaluate(() => {
    const T = window.__T;
    T.setLang('es');
    const plain = h => h.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
    return T.CATALOGUE.list.map(m => ({ id: m.id, s: m.s, four: !!m.minC, text: plain(T.missionText(m)), bonus: T.BONUS_TYPES.includes(m.t) ? plain(T.bonusText(m)).replace(/^\*\s*/, '') : '' }));
  });
  await browser.close();
  const listPath = path.join(__dirname, 'listado.md');
  const md = fs.readFileSync(listPath, 'utf8');
  const start = md.indexOf('## Objetivos'), end = md.indexOf('\n## ', start + 5);
  const rows = es.map(o => `| ${o.id} | ${'★'.repeat(o.s)}${'☆'.repeat(5 - o.s)} | ${o.text}${o.four ? ' *(solo con 4 colores)*' : ''} | ${o.bonus} |`).join('\n');
  const table = `## Objetivos\n\n| Nº | Estrellas | Objetivo | Estrella extra (*) |\n|---|---|---|---|\n${rows}\n`;
  fs.writeFileSync(listPath, md.slice(0, start) + table + md.slice(end));
  fs.writeFileSync(path.join(__dirname, 'textos_en.json'), JSON.stringify(texts, null, 1));
  console.log(`textos_en.json: ${texts.objectives.length} objectives`);
})();
