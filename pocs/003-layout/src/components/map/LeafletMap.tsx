import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'
import 'leaflet-draw'
import type { KeepoutFeature } from '@/types'

// Fix Leaflet default marker icon paths broken by Vite
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
})

interface Props {
  lat: number
  lng: number
  /** Called when user finishes drawing the boundary polygon */
  onBoundaryDrawn: (feature: GeoJSON.Feature<GeoJSON.Polygon>) => void
  /** Called when user finishes drawing a keepout */
  onKeepoutDrawn: (feature: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.LineString>) => void
  /** Existing boundary to restore on load */
  initialBoundary?: GeoJSON.Feature<GeoJSON.Polygon> | null
  /** Existing keepouts to restore on load */
  initialKeeouts?: KeepoutFeature[]
  /** Rack rectangles to render as a layer */
  rackPlacements?: GeoJSON.Feature<GeoJSON.Polygon>[]
  /** Which drawing mode is active */
  drawMode: 'boundary' | 'keepout' | null
  onDrawModeEnd: () => void
}

export function LeafletMap({
  lat, lng,
  onBoundaryDrawn,
  onKeepoutDrawn,
  initialBoundary,
  initialKeeouts = [],
  rackPlacements = [],
  drawMode,
  onDrawModeEnd,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const boundaryLayerRef = useRef<L.Layer | null>(null)
  const keepoutLayerRef = useRef<L.FeatureGroup | null>(null)
  const rackLayerRef = useRef<L.GeoJSON | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const activeHandlerRef = useRef<any | null>(null)

  // Init map once
  useEffect(() => {
    if (mapRef.current || !containerRef.current) return

    const map = L.map(containerRef.current).setView([lat, lng], 17)
    mapRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 22,
    }).addTo(map)

    // Keepout layer
    const keepoutGroup = new L.FeatureGroup()
    keepoutLayerRef.current = keepoutGroup
    map.addLayer(keepoutGroup)

    // Restore initial boundary
    if (initialBoundary) {
      const layer = L.geoJSON(initialBoundary, {
        style: { color: '#3b82f6', weight: 2, fillOpacity: 0.08 },
      }).addTo(map)
      boundaryLayerRef.current = layer
    }

    // Restore initial keepouts
    for (const ko of initialKeeouts) {
      L.geoJSON(ko.geojson, {
        style: { color: '#ef4444', weight: 2, fillOpacity: 0.12, dashArray: '4 4' },
      }).addTo(keepoutGroup)
    }

    // Listen for draw events
    map.on(L.Draw.Event.CREATED, (e) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const layer = (e as any).layer as L.Layer
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const type = (e as any).layerType as string

      if (type === 'polygon' || type === 'rectangle') {
        const feature = (layer as L.Polygon).toGeoJSON() as GeoJSON.Feature<GeoJSON.Polygon>
        if (activeHandlerRef.current && (activeHandlerRef.current as unknown as { _mode?: string })._mode === 'boundary') {
          // boundary draw
          if (boundaryLayerRef.current) map.removeLayer(boundaryLayerRef.current)
          const newLayer = L.geoJSON(feature, { style: { color: '#3b82f6', weight: 2, fillOpacity: 0.08 } }).addTo(map)
          boundaryLayerRef.current = newLayer
          onBoundaryDrawn(feature)
        } else {
          // keepout draw
          L.geoJSON(feature, { style: { color: '#ef4444', weight: 2, fillOpacity: 0.12, dashArray: '4 4' } }).addTo(keepoutLayerRef.current!)
          onKeepoutDrawn(feature)
        }
      } else if (type === 'polyline') {
        const feature = (layer as L.Polyline).toGeoJSON() as GeoJSON.Feature<GeoJSON.LineString>
        L.geoJSON(feature, { style: { color: '#ef4444', weight: 3, dashArray: '4 4' } }).addTo(keepoutLayerRef.current!)
        onKeepoutDrawn(feature)
      }
      activeHandlerRef.current = null
      onDrawModeEnd()
    })

    return () => {
      map.remove()
      mapRef.current = null
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Handle drawMode changes
  useEffect(() => {
    const map = mapRef.current
    if (!map) return

    // Stop any existing handler
    if (activeHandlerRef.current) {
      try { activeHandlerRef.current.disable() } catch { /* ignore */ }
      activeHandlerRef.current = null
    }

    if (!drawMode) return

    if (drawMode === 'boundary') {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const handler = new (L.Draw as any).Polygon(map, { shapeOptions: { color: '#3b82f6', weight: 2, fillOpacity: 0.08 } })
      handler._mode = 'boundary'
      activeHandlerRef.current = handler
      handler.enable()
    } else if (drawMode === 'keepout') {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const handler = new (L.Draw as any).Polygon(map, { shapeOptions: { color: '#ef4444', weight: 2, fillOpacity: 0.12 } })
      handler._mode = 'keepout'
      activeHandlerRef.current = handler
      handler.enable()
    }
  }, [drawMode])

  // Update rack layer whenever placements change
  useEffect(() => {
    const map = mapRef.current
    if (!map) return
    if (rackLayerRef.current) { map.removeLayer(rackLayerRef.current); rackLayerRef.current = null }
    if (rackPlacements.length === 0) return
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const layer = L.geoJSON({ type: 'FeatureCollection', features: rackPlacements } as any, {
      style: { color: '#f59e0b', weight: 1, fillOpacity: 0.35 },
    }).addTo(map)
    rackLayerRef.current = layer
  }, [rackPlacements])

  return <div ref={containerRef} className="w-full h-full" />
}
