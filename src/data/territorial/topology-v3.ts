export type Position = [number, number];
export type TopologyRelation = 'rook' | 'queen' | 'overlap' | 'disjoint';
export const TOPOLOGY_TOLERANCE_DEGREES = 0.00001;

const distance = (a: Position, b: Position) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const cross = (a: Position, b: Position, c: Position) =>
  (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]);
const bbox = (ring: Position[]) => ring.reduce(
  (box, [x, y]) => [Math.min(box[0], x), Math.min(box[1], y), Math.max(box[2], x), Math.max(box[3], y)],
  [Infinity, Infinity, -Infinity, -Infinity],
);
const boxesIntersect = (a: number[], b: number[], tolerance: number) =>
  a[0] <= b[2] + tolerance && a[2] + tolerance >= b[0]
  && a[1] <= b[3] + tolerance && a[3] + tolerance >= b[1];

function sharedSegmentLength(a: Position, b: Position, c: Position, d: Position, tolerance: number) {
  const scale = Math.max(distance(a, b), distance(c, d), tolerance);
  if (Math.abs(cross(a, b, c)) / scale > tolerance || Math.abs(cross(a, b, d)) / scale > tolerance) return 0;
  const axis = Math.abs(b[0] - a[0]) >= Math.abs(b[1] - a[1]) ? 0 : 1;
  const left = Math.max(Math.min(a[axis], b[axis]), Math.min(c[axis], d[axis]));
  const right = Math.min(Math.max(a[axis], b[axis]), Math.max(c[axis], d[axis]));
  return Math.max(0, right - left);
}

export function classifyBoundaryRelation(a: Position[], b: Position[], tolerance = TOPOLOGY_TOLERANCE_DEGREES): TopologyRelation {
  if (!boxesIntersect(bbox(a), bbox(b), tolerance)) return 'disjoint';
  let pointContact = false;
  for (let ai = 1; ai < a.length; ai += 1) {
    for (let bi = 1; bi < b.length; bi += 1) {
      if (sharedSegmentLength(a[ai - 1], a[ai], b[bi - 1], b[bi], tolerance) > tolerance) return 'rook';
      if (
        distance(a[ai - 1], b[bi - 1]) <= tolerance
        || distance(a[ai - 1], b[bi]) <= tolerance
        || distance(a[ai], b[bi - 1]) <= tolerance
        || distance(a[ai], b[bi]) <= tolerance
      ) pointContact = true;
    }
  }
  return pointContact ? 'queen' : 'disjoint';
}

export function repairRing(ring: Position[]): Position[] {
  const clean = ring.filter((point, index) => index === 0 || distance(point, ring[index - 1]) > Number.EPSILON);
  if (clean.length >= 3 && distance(clean[0], clean.at(-1)!) > Number.EPSILON) clean.push([...clean[0]] as Position);
  if (clean.length < 4) throw new Error('Geometría inválida: el anillo no tiene tres vértices distintos.');
  return clean;
}
