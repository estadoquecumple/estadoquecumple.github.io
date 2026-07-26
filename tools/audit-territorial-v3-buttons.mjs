import { readFileSync } from 'node:fs';
const componentFiles=['TerritorialLab.astro','TerritoryMap.astro','RootsWorkspace.astro','SapWorkspace.astro','SeedsWorkspace.astro','ScenarioOutputs.astro'].map((file)=>`src/components/territorial/${file}`);
const components=componentFiles.map((file)=>readFileSync(file,'utf8')).join('\n');
const implementation=readFileSync('src/components/territorial/TerritorialLab.astro','utf8')+readFileSync('src/components/territorial/TerritoryMap.astro','utf8');
const browser=readFileSync('tests/browser/territorial-v3.spec.ts','utf8');
const buttons=[...components.matchAll(/<button\b[^>]*\b(data-[a-z0-9-]+)(?:=(?:"[^"]*"|\{[^}]*\}))?[^>]*>/gi)].map((match)=>match[1]);
const unique=[...new Set(buttons)];
const generic=new Set(['data-mode','data-mobile-panel','data-camera','data-consequence-tab']);
const errors=[];
for(const attribute of unique){
  const selector=`[${attribute}`;
  if(!implementation.includes(selector)&&!generic.has(attribute))errors.push(`${attribute}: sin manejador`);
  if(!browser.includes(selector)&&!browser.includes(attribute))errors.push(`${attribute}: sin prueba de navegador declarada`);
}
for(const forbidden of ['disponible sobre las unidades cargadas; use la tabla','const half = Math.ceil',"prompt('Nombre del nuevo nivel"])if(implementation.includes(forbidden))errors.push(`marcador engañoso: ${forbidden}`);
if(errors.length){console.error(`BUTTON CONTRACT: ${errors.length} error(es)\n${errors.map((error)=>`- ${error}`).join('\n')}`);process.exit(1);}
console.log(`BUTTON CONTRACT OK: ${unique.length} contratos data-* visibles tienen manejador y cobertura de navegador declarada.`);
