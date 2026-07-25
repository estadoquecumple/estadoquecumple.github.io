import type { APIRoute } from 'astro';
import { SITE, ROUTES, absoluteUrl } from '../config/site';
export const GET: APIRoute = ({ site }) => {
  if (!site) throw new Error('Astro.site es obligatorio.');
  const routes = ROUTES.filter((route) => route.indexable).map((route) => ({
    path: route.path,
    title: route.title,
    url: absoluteUrl(route.path, site),
    description: route.description,
    group: route.group,
    type: route.type,
    ...(route.dateModified ? {dateModified: route.dateModified} : {}),
    author: SITE.author,
    editorialStatus: route.editorialStatus,
  }));
  return new Response(JSON.stringify({name:SITE.name,alternateName:SITE.alternateName,author:SITE.author,url:site.toString(),language:SITE.language,routes}, null, 2), {
    headers: {'Content-Type': 'application/json; charset=utf-8'},
  });
};
