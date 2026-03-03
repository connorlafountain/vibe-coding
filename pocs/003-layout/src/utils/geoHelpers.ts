import * as turf from '@turf/turf'

/** Shrink a polygon inward by offsetMeters. Returns null if offset collapses the polygon. */
export function insetPolygon(
  polygon: GeoJSON.Feature<GeoJSON.Polygon>,
  offsetMeters: number
): GeoJSON.Feature<GeoJSON.Polygon> | null {
  if (offsetMeters <= 0) return polygon
  const buffered = turf.buffer(polygon, -offsetMeters, { units: 'meters' })
  if (!buffered) return null
  const geom = buffered.geometry
  if (!geom || geom.coordinates.length === 0) return null
  if (geom.type === 'MultiPolygon') {
    // Take the largest component
    const largest = geom.coordinates.reduce((a, b) =>
      turf.area(turf.polygon(a)) >= turf.area(turf.polygon(b)) ? a : b
    )
    return turf.polygon(largest) as GeoJSON.Feature<GeoJSON.Polygon>
  }
  return buffered as GeoJSON.Feature<GeoJSON.Polygon>
}

/** Buffer a keepout feature outward by offsetMeters. */
export function bufferKeepout(
  feature: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.LineString>,
  offsetMeters: number
): GeoJSON.Feature<GeoJSON.Polygon> | null {
  const dist = Math.max(offsetMeters, 0.1)
  const buffered = turf.buffer(feature, dist, { units: 'meters' })
  if (!buffered) return null
  const geom = buffered.geometry
  if (!geom) return null
  if (geom.type === 'MultiPolygon') {
    const largest = geom.coordinates.reduce((a, b) =>
      turf.area(turf.polygon(a)) >= turf.area(turf.polygon(b)) ? a : b
    )
    return turf.polygon(largest) as GeoJSON.Feature<GeoJSON.Polygon>
  }
  return buffered as GeoJSON.Feature<GeoJSON.Polygon>
}

/** Subtract all buffered keepouts from the boundary polygon. */
export function computeUsableArea(
  boundary: GeoJSON.Feature<GeoJSON.Polygon>,
  keepouts: GeoJSON.Feature<GeoJSON.Polygon>[]
): GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.MultiPolygon> | null {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let usable: GeoJSON.Feature<any> = boundary
  for (const ko of keepouts) {
    if (!usable) break
    try {
      const diff = turf.difference(turf.featureCollection([usable, ko]))
      if (!diff) return null
      usable = diff
    } catch {
      // Ignore topology errors for individual keepouts
    }
  }
  return usable as GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.MultiPolygon>
}

/** Create a rack-footprint rectangle as a GeoJSON Polygon.
 *  originLng/Lat = SW corner in degrees. widthM/heightM in metres. */
export function makeRackRect(
  originLng: number,
  originLat: number,
  widthM: number,
  heightM: number
): GeoJSON.Feature<GeoJSON.Polygon> {
  const deltaLng = widthM / (111320 * Math.cos((originLat * Math.PI) / 180))
  const deltaLat = heightM / 110540
  return turf.polygon([[
    [originLng, originLat],
    [originLng + deltaLng, originLat],
    [originLng + deltaLng, originLat + deltaLat],
    [originLng, originLat + deltaLat],
    [originLng, originLat],
  ]])
}

/** Test if a rack rectangle is fully inside usable area (handles MultiPolygon). */
export function rackFits(
  usableArea: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.MultiPolygon>,
  rackRect: GeoJSON.Feature<GeoJSON.Polygon>
): boolean {
  try {
    const geom = usableArea.geometry
    if (geom.type === 'Polygon') {
      return turf.booleanContains(usableArea as GeoJSON.Feature<GeoJSON.Polygon>, rackRect)
    }
    // MultiPolygon: check each component
    for (const coords of geom.coordinates) {
      if (turf.booleanContains(turf.polygon(coords), rackRect)) return true
    }
    return false
  } catch {
    return false
  }
}
