type Position = [number, number];
type Ring = Position[];

const ringArea = (ring: Ring) => Math.abs(ring.reduce((sum, point, index) => {
  const next = ring[(index + 1) % ring.length];
  return sum + point[0] * next[1] - next[0] * point[1];
}, 0) / 2);

const coordinates = (geometry: any): Ring[] => {
  if (geometry?.type === 'Polygon') return geometry.coordinates;
  if (geometry?.type === 'MultiPolygon') return geometry.coordinates.flat();
  throw new Error('La geometría debe ser Polygon o MultiPolygon.');
};

const bbox = (geometry: unknown) => {
  const points = coordinates(geometry).flat();
  if (!points.length || points.some((point) => point.length < 2 || !point.every(Number.isFinite))) throw new Error('Geometría inválida.');
  return points.reduce<[number, number, number, number]>((box, [x, y]) => [
    Math.min(box[0], x), Math.min(box[1], y), Math.max(box[2], x), Math.max(box[3], y),
  ], [Infinity, Infinity, -Infinity, -Infinity]);
};

self.onmessage = (event: MessageEvent<{ operation: 'inspect' | 'dissolve'; geometries: unknown[] }>) => {
  try {
    const geometries = event.data.geometries;
    const boxes = geometries.map(bbox);
    const combined = boxes.reduce<[number, number, number, number]>((box, item) => [
      Math.min(box[0], item[0]), Math.min(box[1], item[1]), Math.max(box[2], item[2]), Math.max(box[3], item[3]),
    ], [Infinity, Infinity, -Infinity, -Infinity]);
    const planarArea = geometries.reduce<number>((sum, geometry) => sum + coordinates(geometry).reduce((value, ring) => value + ringArea(ring), 0), 0);
    self.postMessage({
      ok: true,
      operation: event.data.operation,
      bbox: combined,
      planarArea,
      geometry: event.data.operation === 'dissolve'
        ? { type: 'GeometryCollection', geometries }
        : null,
      method: 'Operación reproducible en Web Worker; GeometryCollection conserva originales y no altera cartografía oficial.',
    });
  } catch (error) {
    self.postMessage({ ok: false, error: error instanceof Error ? error.message : String(error) });
  }
};
