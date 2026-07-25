import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

const root = resolve('dist');
const origin = (process.env.SITE_URL ?? 'https://estadoquecumple.github.io').replace(/\/+$/, '');
const failures = [];
const warnings = [];
const pages = [];
const routeFile = (pathname) => pathname === '/' ? join(root,'index.html') : pathname === '/404.html' ? join(root,'404.html') : join(root,pathname.slice(1),'index.html');
const walk = (dir) => readdirSync(dir,{withFileTypes:true}).flatMap((item) => item.isDirectory() ? walk(join(dir,item.name)) : item.name.endsWith('.html') && !/^google[a-zA-Z0-9_-]+\.html$/.test(item.name) ? [join(dir,item.name)] : []);
const sitemapFiles = existsSync(root) ? readdirSync(root).filter((name)=>/^sitemap.*\.xml$/.test(name)) : [];
const sitemapXml = sitemapFiles.map((name)=>readFileSync(join(root,name),'utf8')).join('\n');
const sitemapUrls = new Set([...sitemapXml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match)=>match[1]).filter((url)=>!url.endsWith('.xml')));

if (!existsSync(root)) failures.push('No existe dist/. Ejecute npm run build.');
for (const file of existsSync(root) ? walk(root) : []) {
  const html = readFileSync(file,'utf8');
  const rel = relative(root,file).replaceAll('\\','/');
  const path = rel === 'index.html' ? '/' : rel === '404.html' ? '/404.html' : `/${rel.replace(/index\.html$/,'')}`;
  const canonicals = [...html.matchAll(/<link rel="canonical" href="([^"]+)"/g)].map((m)=>m[1]);
  const ogUrl = html.match(/<meta property="og:url" content="([^"]+)"/)?.[1];
  const robots = html.match(/<meta name="robots" content="([^"]+)"/)?.[1] ?? '';
  const indexable = !robots.includes('noindex') && path !== '/404.html';
  const title = html.match(/<title>([^<]+)<\/title>/)?.[1]?.trim();
  const description = html.match(/<meta name="description" content="([^"]+)"/)?.[1]?.trim();
  if (canonicals.length !== 1) failures.push(`${path}: debe tener exactamente una canonical; tiene ${canonicals.length}.`);
  if (canonicals[0] && new URL(canonicals[0]).origin !== origin) failures.push(`${path}: canonical usa host incorrecto.`);
  if (!title) failures.push(`${path}: falta título.`);
  if (!description) failures.push(`${path}: falta descripción.`);
  if (ogUrl !== canonicals[0]) failures.push(`${path}: og:url no coincide con canonical.`);
  if (indexable && !sitemapUrls.has(canonicals[0])) failures.push(`${path}: URL indexable ausente del sitemap.`);
  if (!indexable && sitemapUrls.has(canonicals[0])) failures.push(`${path}: URL noindex presente en el sitemap.`);
  const jsonScripts = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  if (indexable && !jsonScripts.length) failures.push(`${path}: falta JSON-LD.`);
  for (const script of jsonScripts) try { JSON.parse(script[1]); } catch { failures.push(`${path}: JSON-LD inválido.`); }
  const image = html.match(/<meta property="og:image" content="([^"]+)"/)?.[1];
  if (!image) failures.push(`${path}: falta imagen social.`);
  else if (new URL(image).origin !== origin || !existsSync(join(root,new URL(image).pathname.slice(1)))) failures.push(`${path}: imagen social inexistente o externa al host canónico.`);
  const visible = html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  if (['/','/cams/','/estado-que-cumple/','/observatorio/laboratorio-territorial/'].includes(path) && visible.length < 500) failures.push(`${path}: contenido HTML principal insuficiente.`);
  pages.push({path,canonical:canonicals[0],title,indexable,jsonLdBlocks:jsonScripts.length});
}
for (const url of sitemapUrls) {
  if (!url.startsWith(`${origin}/`) && url !== `${origin}/`) failures.push(`Sitemap: host incorrecto en ${url}.`);
  if (!existsSync(routeFile(new URL(url).pathname))) failures.push(`Sitemap: URL no compilada ${url}.`);
}
const allOutput = existsSync(root) ? readdirSync(root,{recursive:true}).filter((name)=>typeof name==='string').map((name)=>{const file=join(root,name);try{return readFileSync(file,'utf8')}catch{return ''}}).join('\n') : '';
if (allOutput.includes('camscarlosmartinez.github.io')) failures.push('La salida contiene el dominio público anterior.');
if (/https:\/\/estadoquecumple\.(?:co|com\.co)(?:\/|["'])/.test(allOutput)) failures.push('La salida usa prematuramente un dominio futuro.');
if (allOutput.includes('localhost')) failures.push('La salida contiene localhost.');
const robots = existsSync(join(root,'robots.txt')) ? readFileSync(join(root,'robots.txt'),'utf8') : '';
if (!robots.includes(`Sitemap: ${origin}/sitemap-index.xml`)) failures.push('robots.txt no enlaza el sitemap canónico.');
const inbound = new Map(pages.map((page)=>[page.path,0]));
for (const file of existsSync(root) ? walk(root) : []) {
  const html=readFileSync(file,'utf8');
  for(const match of html.matchAll(/href="(\/[^"#?]*(?:\/|\.html))[^"]*"/g)) if(inbound.has(match[1])) inbound.set(match[1],inbound.get(match[1])+1);
}
for(const [path,count] of inbound) if(count===0 && !['/','/404.html'].includes(path)) failures.push(`${path}: página huérfana.`);
const googleFiles = readdirSync(resolve('public')).filter((name)=>/^google[a-zA-Z0-9_-]+\.html$/.test(name));
for(const file of googleFiles) if(!existsSync(join(root,file)) || readFileSync(join(root,file),'utf8')!==readFileSync(resolve('public',file),'utf8')) failures.push(`${file}: la verificación de Google no se conservó al compilar.`);
const report={generatedAt:new Date().toISOString(),canonicalOrigin:origin,indexablePages:pages.filter((p)=>p.indexable).length,noindexPages:pages.filter((p)=>!p.indexable).map((p)=>p.path),sitemaps:sitemapFiles,pages,failures,warnings};
mkdirSync(resolve('reports'),{recursive:true});
writeFileSync(resolve('reports/seo-report.json'),`${JSON.stringify(report,null,2)}\n`);
console.log(`SEO: ${report.indexablePages} indexables; ${report.noindexPages.length} noindex; ${sitemapFiles.length} sitemap(s); ${failures.length} error(es); ${warnings.length} aviso(s).`);
if(failures.length){console.error(failures.map((item)=>`- ${item}`).join('\n'));process.exitCode=1;}
