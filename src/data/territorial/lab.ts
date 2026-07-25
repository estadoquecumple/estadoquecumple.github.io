import { z } from 'zod';

export const resultTypeSchema = z.enum(['observed', 'calculated', 'assumption']);
export const paramsSchema = z.object({
  mode: z.enum(['roots','sap','seeds']).catch('roots'),
  scenario: z.enum(['current','regional-exploratory','shared-services']).catch('current'),
  territory: z.string().regex(/^(CO|\d{2}|\d{5}|[a-z0-9-]+)$/).catch('CO'),
  metric: z.enum(['population','fiscal','sgr','secop','coverage']).catch('coverage'),
  year: z.coerce.number().int().min(2018).max(2042).catch(2025),
});
export type LabParams = z.infer<typeof paramsSchema>;
export function parseLabParams(search: URLSearchParams): LabParams {
  return paramsSchema.parse(Object.fromEntries(search));
}
export function coverage(values: Array<number|null|undefined>) {
  const available=values.filter((x)=>typeof x==='number' && Number.isFinite(x)).length;
  return {available,total:values.length,percent:values.length ? available/values.length*100 : 0,missingPercent:values.length ? (values.length-available)/values.length*100 : 0};
}
export function aggregate(values: Array<number|null|undefined>) {
  const valid=values.filter((x):x is number=>typeof x==='number'&&Number.isFinite(x));
  return {sum:valid.reduce((a,b)=>a+b,0),count:valid.length,mean:valid.length?valid.reduce((a,b)=>a+b,0)/valid.length:null};
}
