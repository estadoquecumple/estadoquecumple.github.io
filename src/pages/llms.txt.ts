import type { APIRoute } from 'astro';
import { SITE, absoluteUrl } from '../config/site';
export const GET: APIRoute = ({ site }) => {
  if (!site) throw new Error('Astro.site es obligatorio.');
  const link = (label:string,path:string) => `- [${label}](${absoluteUrl(path, site)})`;
  const body = `# ${SITE.name}\n\n> ${SITE.description}\n\nCAMS es el nombre alternativo y la identidad editorial personal de ${SITE.author}. No es una entidad jurídica ni un organismo público.\n\nURL canónica actual: ${site}\nIdioma: ${SITE.language}\n\n## Rutas principales\n\n${link('Estado que Cumple','/estado-que-cumple/')}\n${link('Documento publicado','/documentos/estado-que-cumple-2026-2030/')}\n${link('Método de Estado que Cumple','/estado-que-cumple/metodo/')}\n${link('Laboratorio Territorial CAMS','/observatorio/laboratorio-territorial/')}\n${link('CAMS y autoría','/cams/')}\n${link('Criterios y transparencia','/cams/criterios-y-transparencia/')}\n${link('Archivo y versiones','/archivo/')}\n\nLos documentos y escenarios indican su estado editorial. La propuesta no es una política oficial. Un dominio propio solo sustituirá esta URL cuando exista y esté conectado; este archivo no garantiza indexación.\n`;
  return new Response(body, {headers:{'Content-Type':'text/plain; charset=utf-8'}});
};
