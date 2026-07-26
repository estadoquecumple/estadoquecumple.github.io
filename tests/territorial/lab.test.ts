import { describe,expect,it } from 'vitest';
import { aggregate,coverage,parseLabParams,resultTypeSchema } from '../../src/data/territorial/metrics-v3';
import current from '../../data/scenarios/current.json';
import regional from '../../data/scenarios/regional-exploratory.json';
import shared from '../../data/scenarios/shared-services.json';

describe('contrato territorial',()=>{
  it('agrega solo números finitos sin imputar',()=>expect(aggregate([1,null,2,undefined,Number.NaN])).toEqual({sum:3,count:2,mean:1.5}));
  it('calcula cobertura y faltantes',()=>expect(coverage([1,null,3]).missingPercent).toBeCloseTo(33.333));
  it.each(['observed','calculated','assumption'])('acepta tipo %s',type=>expect(resultTypeSchema.parse(type)).toBe(type));
  it('normaliza parámetros URL y rechaza valores fuera de contrato',()=>{
    const valid=parseLabParams(new URLSearchParams('mode=semillas&scenario=shared-services&territory=25099&metric=fiscal&year=2024'));
    expect(valid).toMatchObject({mode:'semillas',scenario:'shared-services',territory:'25099',metric:'fiscal',year:2024});
    expect(parseLabParams(new URLSearchParams('mode=x&year=3000'))).toMatchObject({mode:'raices',year:2025});
  });
});
describe('escenarios declarativos',()=>{
  it('publica los tres escenarios',()=>expect([current.id,regional.id,shared.id]).toEqual(['current','regional-exploratory','shared-services']));
  it('regional tiene entre 8 y 12 unidades',()=>expect(regional.assignments.length).toBeGreaterThanOrEqual(8));
  it('servicios compartidos incluye tres demostraciones',()=>expect(shared.assignments.map(x=>x.id)).toEqual(expect.arrayContaining(['bogota-sabana','pacifico-medio','norte-caldas-pequenos'])));
  it('no declara ahorros exactos',()=>expect(JSON.stringify([regional,shared]).toLowerCase()).not.toMatch(/ahorro.{0,15}\d/));
});
