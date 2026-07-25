import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
const root=resolve('dist');
const territorialRoute='/observatorio/laboratorio-territorial/';
const canonicalOrigin='https://estadoquecumple.github.io';
const astroConfig=readFileSync(resolve('astro.config.mjs'),'utf8');
const routes=['/','/cams/','/cams/trayectoria/','/cams/metodo/','/cams/criterios-y-transparencia/','/propuestas/','/conocimiento/','/investigaciones/','/documentos/','/documentos/estado-que-cumple-2026-2030/','/bitacora/','/observatorio/','/archivo/','/participar/','/participar/correcciones/','/participar/aportar-fuente/','/participar/colaborar/','/buscar/','/accesibilidad/','/privacidad-y-datos/','/estado-que-cumple/','/estado-que-cumple/problema/','/estado-que-cumple/fundamentos/','/estado-que-cumple/metodo/','/estado-que-cumple/arquitectura/','/estado-que-cumple/activacion/','/estado-que-cumple/implementacion/','/estado-que-cumple/aplicaciones/','/estado-que-cumple/documento/','/404.html'];
const htmlFiles=[];const walk=d=>readdirSync(d,{withFileTypes:true}).forEach(e=>{const p=join(d,e.name);e.isDirectory()?walk(p):e.name.endsWith('.html')&&htmlFiles.push(p)});
const failures=[];const warn=[];
if(!existsSync(root)) failures.push('No existe dist/. Ejecute npm run build.'); else walk(root);
if(!astroConfig.includes(`'${canonicalOrigin}'`)||!astroConfig.includes('site: siteUrl'))failures.push('astro.config.mjs: fuente SITE_URL o valor predeterminado incorrectos');
if(/^\s*base\s*:/m.test(astroConfig))failures.push('astro.config.mjs: no debe declarar base para un sitio raíz');
const routeFile=r=>r==='/404.html'?join(root,'404.html'):r==='/'?join(root,'index.html'):join(root,r.slice(1),'index.html');
routes.push(territorialRoute);
for(const r of routes)if(!existsSync(routeFile(r)))failures.push(`Falta ruta compilada: ${r}`);
const ids=new Map();const links=[];
for(const file of htmlFiles){const html=readFileSync(file,'utf8');const rel=file.slice(root.length).replaceAll('\\','/');
 if(!/<html[^>]+lang="es-CO"/.test(html))failures.push(`${rel}: falta lang es-CO`);
 if(!/<title>[^<]+<\/title>/.test(html))failures.push(`${rel}: falta title`);
 if(!/<meta name="description" content="[^"]+"/.test(html))failures.push(`${rel}: falta description`);
 if(!html.includes(`<link rel="canonical" href="${canonicalOrigin}`))failures.push(`${rel}: canonical no usa el dominio oficial`);
 if(!html.includes(`<meta property="og:url" content="${canonicalOrigin}`))failures.push(`${rel}: Open Graph no usa el dominio oficial`);
 if(html.includes('camscarlosmartinez.github.io'))failures.push(`${rel}: conserva el dominio público anterior`);
 if(/(?:href|src)="\/(?:styles\.css|script\.js)"/.test(html))failures.push(`${rel}: referencia recurso legado`);
 if(/href="#"/.test(html))failures.push(`${rel}: contiene href="#"`);
 if(/<form\b/i.test(html))failures.push(`${rel}: contiene formulario no autorizado`);
 for(const m of html.matchAll(/\sid="([^"]+)"/g)){const key=`${rel}#${m[1]}`;if(ids.has(key))failures.push(`${rel}: id duplicado ${m[1]}`);ids.set(key,true)}
 for(const m of html.matchAll(/(?:href|src)="(\/[^"]*)"/g))links.push([file,m[1]]);
}
for(const [file,url] of links){const clean=url.split(/[?#]/)[0];if(!clean||clean.startsWith('//'))continue;let target;if(clean.endsWith('/'))target=join(root,clean.slice(1),'index.html');else target=join(root,clean.slice(1));if(!existsSync(target))failures.push(`${file.slice(root.length)}: destino inexistente ${url}`)}
for(const legacy of ['index.html','styles.css','script.js','assets','sitemap.xml'])if(existsSync(resolve(legacy)))failures.push(`Duplicación legado en raíz: ${legacy}`);
for(const old of ['cams','estado-que-cumple','documentos','observatorio','bitacora','participar','archivo'])if(existsSync(resolve(old)))failures.push(`Ruta HTML antigua restante: ${old}/`);
for(const publicFile of ['robots.txt','llms.txt','site-index.json','site.webmanifest','sitemap-index.xml'])if(!existsSync(join(root,publicFile)))failures.push(`Falta archivo público: ${publicFile}`);
if(existsSync(join(root,'robots.txt'))&&!readFileSync(join(root,'robots.txt'),'utf8').includes(`${canonicalOrigin}/sitemap-index.xml`))failures.push('robots.txt: sitemap incorrecto');
if(existsSync(join(root,'llms.txt'))&&readFileSync(join(root,'llms.txt'),'utf8').includes('camscarlosmartinez.github.io'))failures.push('llms.txt: dominio anterior');
if(existsSync(join(root,'site-index.json'))){try{const index=JSON.parse(readFileSync(join(root,'site-index.json'),'utf8'));if(index.url!==`${canonicalOrigin}/`)failures.push('site-index.json: URL incorrecta');for(const item of index.routes)if(!existsSync(routeFile(item.path)))failures.push(`site-index.json: ruta inexistente ${item.path}`)}catch{failures.push('site-index.json: JSON inválido')}}
for(const sitemap of ['sitemap-index.xml','sitemap-0.xml'])if(existsSync(join(root,sitemap))){const xml=readFileSync(join(root,sitemap),'utf8');if(xml.includes('camscarlosmartinez.github.io')||!xml.includes(canonicalOrigin))failures.push(`${sitemap}: dominio incorrecto`)}
const home=routeFile('/');if(existsSync(home)){const html=readFileSync(home,'utf8');if(!html.includes('<title>Estado que Cumple | CAMS — Carlos Arturo Martínez Sánchez</title>'))failures.push('Portada: título de identidad incorrecto');if(!html.includes('"@type":"WebSite"')||!html.includes('"@type":"Person"'))failures.push('Portada: falta JSON-LD WebSite o Person')}
if(warn.length)console.log(warn.map(x=>`AVISO: ${x}`).join('\n'));
if(failures.length){console.error(`AUDITORÍA: ${failures.length} error(es)\n`+failures.map(x=>`- ${x}`).join('\n'));process.exit(1)}
console.log(`AUDITORÍA OK: ${htmlFiles.length} HTML; ${routes.length} rutas obligatorias; enlaces, assets, ids, metadatos, lang, legados y formularios verificados.`);
