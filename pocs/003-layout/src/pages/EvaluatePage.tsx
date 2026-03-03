import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { useModules } from '@/hooks/useModules'
import { useRacks } from '@/hooks/useRacks'
import { runOptimizer } from '@/utils/optimizer'
import { ResultsTable } from '@/components/evaluate/ResultsTable'
import type { ProjectLayout, EvaluatedResult, CustomLayout, KeepoutFeature } from '@/types'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'

export function EvaluatePage() {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { modules } = useModules(user)
  const { racks } = useRacks(user)

  const [layout, setLayout] = useState<ProjectLayout | null>(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<EvaluatedResult[]>([])
  const [customLayouts, setCustomLayouts] = useState<CustomLayout[]>([])
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!projectId || !user) return
    supabase
      .from('project_layouts')
      .select('*')
      .eq('project_id', projectId)
      .single()
      .then(({ data, error }) => {
        if (error || !data) {
          toast.error('No saved layout found. Save the map first.')
          navigate(`/projects/${projectId}/map`)
          return
        }
        const l = data as unknown as ProjectLayout
        setLayout(l)
        setResults(l.evaluated_results ?? [])
        setCustomLayouts(l.custom_layouts ?? [])
        setLoading(false)
      })
  }, [projectId, user, navigate])

  const handleRun = () => {
    if (!layout?.boundary_geojson) { toast.warning('No boundary found'); return }
    if (racks.length === 0 || modules.length === 0) {
      toast.warning('Add at least one rack and one module to your library first')
      return
    }
    setRunning(true)
    setProgress(0)

    // Use setTimeout to let the spinner render before synchronous optimizer runs
    setTimeout(() => {
      const opts = runOptimizer({
        boundary: layout.boundary_geojson!,
        keepouts: (layout.keepouts_geojson ?? []) as KeepoutFeature[],
        perimeterOffset: layout.perimeter_offset_m ?? 0,
        baseNsSpacing: layout.ns_spacing_m ?? 5,
        baseEwSpacing: layout.ew_spacing_m ?? 2,
        racks,
        modules,
        trials: 100,
        onProgress: (done, total) => setProgress(Math.round((done / total) * 100)),
      })
      setResults(opts)
      setRunning(false)
      persistResults(opts, customLayouts)
    }, 50)
  }

  const persistResults = async (res: EvaluatedResult[], custom: CustomLayout[]) => {
    if (!projectId || !user) return
    setSaving(true)
    await supabase
      .from('project_layouts')
      .update({ evaluated_results: res, custom_layouts: custom, updated_at: new Date().toISOString() })
      .eq('project_id', projectId)
    setSaving(false)
  }

  const handleCustomSave = (custom: CustomLayout) => {
    const updated = [...customLayouts, custom]
    setCustomLayouts(updated)
    persistResults(results, updated)
    toast.success('Custom layout saved')
  }

  if (loading) {
    return <div className="flex-1 p-6 space-y-3"><Skeleton className="h-8 w-48" /><Skeleton className="h-64 w-full" /></div>
  }

  return (
    <div className="flex-1 p-6 max-w-screen-xl mx-auto w-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">Evaluate Layouts</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            {racks.length} rack type{racks.length !== 1 ? 's' : ''} × {modules.length} module{modules.length !== 1 ? 's' : ''} = {racks.length * modules.length} combinations × 100 trials
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" onClick={() => navigate(`/projects/${projectId}/map`)}>
            ← Back to Map
          </Button>
          <Button onClick={handleRun} disabled={running || saving}>
            {running ? 'Running…' : results.length > 0 ? 'Re-run Optimizer' : 'Run Optimizer'}
          </Button>
        </div>
      </div>

      {running && (
        <div className="mb-6 space-y-2">
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Running optimizer…</span>
            <span>{progress}%</span>
          </div>
          <Progress value={progress} />
        </div>
      )}

      {results.length === 0 && !running ? (
        <div className="text-center py-20 text-muted-foreground">
          <p className="mb-3">Click "Run Optimizer" to evaluate all rack + module combinations.</p>
          <p className="text-sm">Each combination runs 100 trials with ±20% spacing variation.</p>
        </div>
      ) : (
        <ResultsTable
          results={results}
          customLayouts={customLayouts}
          boundary={layout!.boundary_geojson!}
          keepouts={(layout!.keepouts_geojson ?? []) as KeepoutFeature[]}
          perimeterOffset={layout!.perimeter_offset_m ?? 0}
          racks={racks}
          modules={modules}
          onCustomSave={handleCustomSave}
        />
      )}
    </div>
  )
}
