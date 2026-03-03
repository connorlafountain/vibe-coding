export interface Project {
  id: string
  user_id: string
  name: string
  address: string | null
  lat: number
  lng: number
  created_at: string
}

export interface Module {
  id: string
  user_id: string
  name: string
  width_m: number
  height_m: number
  power_w: number
  created_at: string
}

export interface Rack {
  id: string
  user_id: string
  name: string
  max_width_m: number
  max_height_m: number
  racking_type: 'fixed-tilt' | 'tracker'
  created_at: string
}

export interface KeepoutFeature {
  id: string
  geojson: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.LineString>
  offset_m: number
}

export interface ProjectLayout {
  id: string
  project_id: string
  user_id: string
  boundary_geojson: GeoJSON.Feature<GeoJSON.Polygon> | null
  keepouts_geojson: KeepoutFeature[]
  perimeter_offset_m: number
  rack_id: string | null
  module_id: string | null
  ns_spacing_m: number
  ew_spacing_m: number
  evaluated_results: EvaluatedResult[]
  custom_layouts: CustomLayout[]
  updated_at: string
}

export interface RackPlacement {
  rackRect: GeoJSON.Feature<GeoJSON.Polygon>
}

export interface FillParams {
  boundary: GeoJSON.Feature<GeoJSON.Polygon>
  keepouts: KeepoutFeature[]
  perimeterOffset: number
  rack: Rack
  ns_spacing_m: number
  ew_spacing_m: number
}

export interface TrialResult {
  ns_spacing_m: number
  ew_spacing_m: number
  rack_count: number
  kw_dc: number
}

export interface EvaluatedResult {
  rack_id: string
  module_id: string
  rack_name: string
  module_name: string
  gcr: number
  ns_spacing_m: number
  ew_spacing_m: number
  rack_count: number
  kw_dc: number
  trials: TrialResult[]
}

export interface CustomLayout extends EvaluatedResult {
  custom_id: string
  label: string
}
