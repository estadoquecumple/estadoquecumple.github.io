import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const command=process.argv[2];
const siteUrl=(process.env.SITE_URL ?? 'https://estadoquecumple.github.io').replace(/\/+$/,'');
const key=process.env.INDEXNOW_KEY?.trim();
if(!['prepare','submit'].includes(command)) throw new Error('Use prepare o submit.');
if(!key){console.log('IndexNow omitido: defina INDEXNOW_KEY con una clave real.');process.exit(0);}
if(!/^[A-Za-z0-9_-]{8,128}$/.test(key)) throw new Error('INDEXNOW_KEY tiene un formato no válido.');
const keyFile=resolve('public',`${key}.txt`);
if(command==='prepare'){
  writeFileSync(keyFile,`${key}\n`,{flag:'w'});
  console.log(`IndexNow preparado: public/${key}.txt. Compile y publique antes de enviar.`);
} else {
  const sitemap=resolve('dist/sitemap-0.xml');
  if(!existsSync(sitemap)) throw new Error('Falta dist/sitemap-0.xml; ejecute npm run build.');
  const urls=[...readFileSync(sitemap,'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map((m)=>m[1]).filter((url)=>url.startsWith(`${siteUrl}/`)).slice(0,10000);
  if(!urls.length) throw new Error('El sitemap no contiene URLs canónicas para enviar.');
  const response=await fetch('https://api.indexnow.org/indexnow',{method:'POST',headers:{'Content-Type':'application/json; charset=utf-8'},body:JSON.stringify({host:new URL(siteUrl).host,key,keyLocation:`${siteUrl}/${key}.txt`,urlList:urls})});
  if(!response.ok) throw new Error(`IndexNow respondió ${response.status}.`);
  console.log(`IndexNow aceptó ${urls.length} URL(s) para ${new URL(siteUrl).host}.`);
}
