import booleanIntersects from '@turf/boolean-intersects';
import booleanOverlap from '@turf/boolean-overlap';
import booleanTouches from '@turf/boolean-touches';
import booleanValid from '@turf/boolean-valid';
import cleanCoords from '@turf/clean-coords';
import difference from '@turf/difference';
import intersect from '@turf/intersect';
import { feature, featureCollection } from '@turf/helpers';
import union from '@turf/union';
import unkinkPolygon from '@turf/unkink-polygon';

export const INTERACTIVE_COORDINATE_LIMIT = 25_000;

type PolygonGeometry = GeoJSON.Polygon | GeoJSON.MultiPolygon;
type PolygonFeature = GeoJSON.Feature<PolygonGeometry>;

const coordinateCount = (value: unknown): number => {
  if (!Array.isArray(value)) return 0;
  if (value.length >= 2 && value.every((item) => typeof item === 'number')) return 1;
  return value.reduce((sum, item) => sum + coordinateCount(item), 0);
};

const asFeature = (geometry: PolygonGeometry): PolygonFeature =>
  feature(geometry) as PolygonFeature;

export type GeometryOperationResult = {
  ok: boolean;
  geometry: PolygonGeometry | null;
  backendRequired: boolean;
  valid: boolean;
  warnings: string[];
};

const guard = (geometries: PolygonGeometry[]): GeometryOperationResult | null => {
  const points = geometries.reduce((sum, geometry) => sum + coordinateCount(geometry.coordinates), 0);
  if (points > INTERACTIVE_COORDINATE_LIMIT) {
    return {
      ok: false,
      geometry: null,
      backendRequired: true,
      valid: false,
      warnings: [`La operación tiene ${points} coordenadas; requiere el backend geoespacial de una fase posterior.`],
    };
  }
  return null;
};

export function dissolveGeometries(geometries: PolygonGeometry[]): GeometryOperationResult {
  if (geometries.length < 2) throw new Error('La unión requiere al menos dos geometrías.');
  const blocked = guard(geometries);
  if (blocked) return blocked;
  const cleaned = geometries.map((geometry) => cleanCoords(asFeature(geometry)));
  const result = union(featureCollection(cleaned) as never);
  return result
    ? { ok: true, geometry: result.geometry as PolygonGeometry, backendRequired: false, valid: booleanValid(result), warnings: [] }
    : { ok: false, geometry: null, backendRequired: false, valid: false, warnings: ['Turf no produjo una unión válida.'] };
}

export function differenceGeometries(a: PolygonGeometry, b: PolygonGeometry): GeometryOperationResult {
  const blocked = guard([a, b]);
  if (blocked) return blocked;
  const result = difference(featureCollection([asFeature(a), asFeature(b)]) as never);
  return result
    ? { ok: true, geometry: result.geometry as PolygonGeometry, backendRequired: false, valid: booleanValid(result), warnings: [] }
    : { ok: true, geometry: null, backendRequired: false, valid: true, warnings: ['La diferencia es vacía.'] };
}

export function intersectGeometries(a: PolygonGeometry, b: PolygonGeometry): GeometryOperationResult {
  const blocked = guard([a, b]);
  if (blocked) return blocked;
  const result = intersect(featureCollection([asFeature(a), asFeature(b)]) as never);
  return result
    ? { ok: true, geometry: result.geometry as PolygonGeometry, backendRequired: false, valid: booleanValid(result), warnings: [] }
    : { ok: true, geometry: null, backendRequired: false, valid: true, warnings: ['No existe intersección.'] };
}

export function inspectGeometry(geometry: PolygonGeometry) {
  const item = asFeature(geometry);
  return {
    valid: booleanValid(item),
    cleaned: cleanCoords(item).geometry as PolygonGeometry,
    partsAfterUnkink: geometry.type === 'Polygon' ? unkinkPolygon(item as GeoJSON.Feature<GeoJSON.Polygon>).features.length : null,
  };
}
export function geometryRelations(a: PolygonGeometry, b: PolygonGeometry) {
  const first = asFeature(a);
  const second = asFeature(b);
  return {
    intersects: booleanIntersects(first, second),
    overlaps: booleanOverlap(first, second),
    touches: booleanTouches(first, second),
  };
}
