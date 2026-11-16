// Render every chart of the page as a PNG for the READMEs: stills/nl/NN.png, stills/fr/NN.png and stills/en/NN.png.
//   node visualisations/src/stills.cjs
// The stills leave out each chart's title and dek (the READMEs print them). Needs Playwright with Chromium; set
// PLAYWRIGHT to its package folder if `require('playwright')` does not resolve.
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const root = path.resolve(__dirname, '..');
const page = 'file:///' + path.join(root, 'belgisch-recht-in-20-grafieken.html').replace(/\\/g, '/');
(async () => {
  const b = await chromium.launch();
  for (const lang of ['nl', 'fr', 'en']) {
    const p = await b.newPage({ viewport: { width: 1100, height: 900 }, colorScheme: 'light', deviceScaleFactor: 1 });
    await p.goto(page + '?lang=' + lang);
    await p.waitForTimeout(2500);
    await p.addStyleTag({ content: 'details.tbl{display:none} figure.chart h3, figure.chart .dek{display:none} figure.chart{padding-top:14px;padding-bottom:12px}' });
    const figs = await p.$$('figure.chart');
    for (let i = 0; i < figs.length; i++) {
      await figs[i].screenshot({ path: path.join(root, 'stills', lang, String(i + 1).padStart(2, '0') + '.png') });
    }
    console.log(lang, figs.length);
    await p.close();
  }
  await b.close();
})();
