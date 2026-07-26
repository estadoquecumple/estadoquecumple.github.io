import { readFileSync, writeFileSync } from 'node:fs';

const componentFiles = ['TerritorialLab.astro', 'TerritoryMap.astro', 'RootsWorkspace.astro', 'SaviaWorkspace.astro', 'SeedsWorkspace.astro', 'ScenarioOutputs.astro'].map((file) => `src/components/territorial/${file}`);
const components = componentFiles.map((file) => readFileSync(file, 'utf8')).join('\n');
const evidence = JSON.parse(readFileSync('reports/territorial-v3-playwright-evidence.json', 'utf8'));
const passedFiles = new Set(evidence.executions.filter((item) => item.status === 'passed').map((item) => item.file.replaceAll('\\', '/')));
const stripComments = (text) => text.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|\s)\/\/.*$/gm, '$1').replace(/<!--[\s\S]*?-->/g, '');
const specs = ['territorial-v3.spec.ts', 'territorial-v2.spec.ts', 'territorial-map.spec.ts'].map((name) => ({
  file: `tests/browser/${name}`,
  source: stripComments(readFileSync(`tests/browser/${name}`, 'utf8')),
}));
const attributes = [...new Set([...components.matchAll(/<button\b[^>]*\b(data-[a-z0-9-]+)/gi)].map((match) => match[1]))];
const generic = new Set(['data-mode', 'data-mobile-panel', 'data-camera', 'data-consequence-tab']);
const implementation = readFileSync('src/components/territorial/TerritorialLab.astro', 'utf8') + readFileSync('src/components/territorial/TerritoryMap.astro', 'utf8');
const controls = attributes.map((attribute) => {
  const selector = `[${attribute}`;
  const candidates = specs.filter(({ source }) => {
    if (source.includes(`activate('${selector}`) || source.includes(`activate("${selector}`)) return true;
    const positions = [...source.matchAll(new RegExp(`\\[${attribute}`, 'g'))].map((match) => match.index ?? -1);
    return positions.some((position) => /(?:\.(?:click|check|uncheck|fill|selectOption|press|evaluate)|activate)\s*\(/.test(source.slice(position, position + 300)));
  });
  const executed = candidates.some(({ file }) => {
    const name = file.split('/').at(-1);
    return [...passedFiles].some((passed) => passed.endsWith(file) || passed === name);
  });
  const handler = generic.has(attribute) || implementation.includes(selector);
  return { selector, handler, playwrightInteraction: candidates.map((item) => item.file), executed, classification: handler && executed ? 'funcional' : 'huérfano' };
});
writeFileSync('reports/territorial-v3-controls-final.json', `${JSON.stringify({
  generatedAt: evidence.generatedAt,
  rule: 'Un botón cuenta solo si tiene manejador y una interacción en un archivo Playwright aprobado. Los comentarios se eliminan.',
  controls,
}, null, 2)}\n`);
const errors = controls.filter((control) => control.classification !== 'funcional');
if (errors.length) {
  console.error(`BUTTON CONTRACT: ${errors.length} control(es) sin evidencia\n${errors.map((item) => `- ${item.selector}: handler=${item.handler}, executed=${item.executed}`).join('\n')}`);
  process.exit(1);
}
console.log(`BUTTON CONTRACT OK: ${controls.length} botones con manejador e interacción Playwright ejecutada.`);
