import * as turf from '@turf/turf'
import { insetPolygon, bufferKeepout, computeUsableArea, makeRackRect, rackFits } from './geoHelpers'
import type { FillParams, RackPlacement } from '@/types'

export function runFill(params: FillParams): RackPlacement[] {
  const { boundary, keepouts, perimeterOffset, rack, ns_spacing_m, ew_spacing_m } = params

  // 1. Inset boundary by perimeter offset
  const offsetBoundary = insetPolygon(boundary, perimeterOffset)
  if (!offsetBoundary) return []

  // 2. Buffer keepouts and subtract from boundary
  const bufferedKeeouts = keepouts
    .map(k => bufferKeepout(k.geojson, k.offset_m))
    .filter((k): k is GeoJSON.Feature<GeoJSON.Polygon> => k !== null)

  const usableArea = computeUsableArea(offsetBoundary, bufferedKeeouts)
  if (!usableArea) return []

  // 3. Bounding box grid
  const bbox = turf.bbox(usableArea)
  const [minLng, minLat, maxLng, maxLat] = bbox

  const centerLat = (minLat + maxLat) / 2
  const metersPerLat = 110540
  const metersPerLng = 111320 * Math.cos((centerLat * Math.PI) / 180)

  const rackWidthDeg = rack.max_width_m / metersPerLng
  const rackHeightDeg = rack.max_height_m / metersPerLat
  const ewStepDeg = (rack.max_width_m + ew_spacing_m) / metersPerLng
  const nsStepDeg = (rack.max_height_m + ns_spacing_m) / metersPerLat

  const placements: RackPlacement[] = []

  for (let lat = minLat; lat + rackHeightDeg <= maxLat + 1e-9; lat += nsStepDeg) {
    for (let lng = minLng; lng + rackWidthDeg <= maxLng + 1e-9; lng += ewStepDeg) {
      const rackRect = makeRackRect(lng, lat, rack.max_width_m, rack.max_height_m)
      if (rackFits(usableArea, rackRect)) {
        placements.push({ rackRect })
      }
    }
  }

  return placements
}
