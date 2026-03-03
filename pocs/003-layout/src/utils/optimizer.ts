import { runFill } from './fillAlgorithm'
import type { FillParams, EvaluatedResult, TrialResult, Rack, Module, KeepoutFeature } from '@/types'

export function calcModulesPerRack(rack: Rack, module: Module): number {
  return (
    Math.floor(rack.max_width_m / module.width_m) *
    Math.floor(rack.max_height_m / module.height_m)
  )
}

export function calcKwDC(rackCount: number, rack: Rack, module: Module): number {
  const mpr = calcModulesPerRack(rack, module)
  return (rackCount * mpr * module.power_w) / 1000
}

export function calcGCR(rack: Rack, ns_spacing_m: number): number {
  return rack.max_height_m / (rack.max_height_m + ns_spacing_m)
}

export function nsSpacingFromGCR(rack: Rack, gcr: number): number {
  if (gcr <= 0 || gcr >= 1) return 5
  return rack.max_height_m / gcr - rack.max_height_m
}

interface OptimizerParams {
  boundary: GeoJSON.Feature<GeoJSON.Polygon>
  keepouts: KeepoutFeature[]
  perimeterOffset: number
  baseNsSpacing: number
  baseEwSpacing: number
  racks: Rack[]
  modules: Module[]
  trials?: number
  onProgress?: (done: number, total: number) => void
}

export function runOptimizer({
  boundary,
  keepouts,
  perimeterOffset,
  baseNsSpacing,
  baseEwSpacing,
  racks,
  modules,
  trials = 100,
  onProgress,
}: OptimizerParams): EvaluatedResult[] {
  const results: EvaluatedResult[] = []
  const total = racks.length * modules.length * trials
  let done = 0

  const baseFill: Omit<FillParams, 'rack' | 'ns_spacing_m' | 'ew_spacing_m'> = {
    boundary,
    keepouts,
    perimeterOffset,
  }

  for (const rack of racks) {
    for (const module of modules) {
      const trialResults: TrialResult[] = []

      for (let i = 0; i < trials; i++) {
        const ns = baseNsSpacing * (0.8 + Math.random() * 0.4)
        const ew = baseEwSpacing * (0.8 + Math.random() * 0.4)

        const placements = runFill({ ...baseFill, rack, ns_spacing_m: ns, ew_spacing_m: ew })
        const rack_count = placements.length
        const kw_dc = calcKwDC(rack_count, rack, module)

        trialResults.push({ ns_spacing_m: ns, ew_spacing_m: ew, rack_count, kw_dc })
        done++
        onProgress?.(done, total)
      }

      trialResults.sort((a, b) => b.kw_dc - a.kw_dc)
      const best = trialResults[0]

      results.push({
        rack_id: rack.id,
        module_id: module.id,
        rack_name: rack.name,
        module_name: module.name,
        gcr: calcGCR(rack, best.ns_spacing_m),
        ns_spacing_m: best.ns_spacing_m,
        ew_spacing_m: best.ew_spacing_m,
        rack_count: best.rack_count,
        kw_dc: best.kw_dc,
        trials: trialResults,
      })
    }
  }

  results.sort((a, b) => b.kw_dc - a.kw_dc)
  return results
}
