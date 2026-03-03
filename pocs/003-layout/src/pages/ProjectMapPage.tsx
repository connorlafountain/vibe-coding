import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/hooks/useAuth'
import { useModules } from '@/hooks/useModules'
import { useRacks } from '@/hooks/useRacks'
import { LeafletMap } from '@/components/map/LeafletMap'
import { runFill } from '@/utils/fillAlgorithm'
import { calcKwDC, calcGCR, nsSpacingFromGCR } from '@/utils/optimizer'
import type { Project, ProjectLayout, KeepoutFeature, RackPlacement, Rack, Module } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'

export function ProjectMapPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { modules } = useModules(user)
  const { racks } = useRacks(user)

  const [project, setProject] = useState<Project | null>(null)
  const [layout, setLayout] = useState<ProjectLayout | null>(null)
  const [loadingProject, setLoadingProject] = useState(true)

  // Design state
  const [boundary, setBoundary] = useState<GeoJSON.Feature<GeoJSON.Polygon> | null>(null)
  const [keepouts, setKeeouts] = useState<KeepoutFeature[]>([])
  const [perimeterOffset, setPerimeterOffset] = useState(0)
  const [selectedRackId, setSelectedRackId] = useState<string>('')
  const [selectedModuleId, setSelectedModuleId] = useState<string>('')
  const [nsSpacing, setNsSpacing] = useState(5)
  const [ewSpacing, setEwSpacing] = useState(2)
  const [gcr, setGcr] = useState<number | null>(null)
  const [placements, setPlacements] = useState<RackPlacement[]>([])
  const [drawMode, setDrawMode] = useState<'boundary' | 'keepout' | null>(null)
  const [saving, setSaving] = useState(false)
  const keepoutOffsetRef = useRef<number>(5)

  const selectedRack = racks.find(r => r.id === selectedRackId) ?? null
  const selectedModule = modules.find(m => m.id === selectedModuleId) ?? null

  // Load project + layout
  useEffect(() => {
    if (!projectId || !user) return
    Promise.all([
      supabase.from('projects').select('*').eq('id', projectId).single(),
      supabase.from('project_layouts').select('*').eq('project_id', projectId).single(),
    ]).then(([{ data: proj, error: projErr }, { data: lay }]) => {
      if (projErr || !proj) { toast.error('Project not found'); navigate('/'); return }
      setProject(proj as Project)
      if (lay) {
        const l = lay as unknown as ProjectLayout
        setLayout(l)
        setBoundary(l.boundary_geojson)
        setKeeouts(l.keepouts_geojson ?? [])
        setPerimeterOffset(l.perimeter_offset_m ?? 0)
        setSelectedRackId(l.rack_id ?? '')
        setSelectedModuleId(l.module_id ?? '')
        setNsSpacing(l.ns_spacing_m ?? 5)
        setEwSpacing(l.ew_spacing_m ?? 2)
      }
      setLoadingProject(false)
    })
  }, [projectId, user, navigate])

  // Recalculate GCR when rack or nsSpacing changes
  useEffect(() => {
    if (selectedRack) setGcr(calcGCR(selectedRack, nsSpacing))
  }, [selectedRack, nsSpacing])

  // Restore placements when layout + racks loaded
  useEffect(() => {
    if (!layout || !boundary || !selectedRack) return
    const result = runFill({ boundary, keepouts, perimeterOffset, rack: selectedRack, ns_spacing_m: nsSpacing, ew_spacing_m: ewSpacing })
    setPlacements(result)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layout, selectedRack])

  const handleNsChange = (val: number) => {
    setNsSpacing(val)
    if (selectedRack) setGcr(calcGCR(selectedRack, val))
  }

  const handleGcrChange = (val: number) => {
    setGcr(val)
    if (selectedRack && val > 0 && val < 1) setNsSpacing(nsSpacingFromGCR(selectedRack, val))
  }

  const handleFill = () => {
    if (!boundary) { toast.warning('Draw a boundary first'); return }
    if (!selectedRack) { toast.warning('Select a rack type first'); return }
    const result = runFill({ boundary, keepouts, perimeterOffset, rack: selectedRack, ns_spacing_m: nsSpacing, ew_spacing_m: ewSpacing })
    setPlacements(result)
  }

  const handleAddKeepout = (feature: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.LineString>) => {
    const ko: KeepoutFeature = {
      id: crypto.randomUUID(),
      geojson: feature,
      offset_m: keepoutOffsetRef.current,
    }
    setKeeouts(prev => [...prev, ko])
  }

  const handleRemoveKeepout = (id: string) => {
    setKeeouts(prev => prev.filter(k => k.id !== id))
    setPlacements([])
  }

  const handleSave = async () => {
    if (!user || !projectId) return
    setSaving(true)
    const payload = {
      project_id: projectId,
      user_id: user.id,
      boundary_geojson: boundary,
      keepouts_geojson: keepouts,
      perimeter_offset_m: perimeterOffset,
      rack_id: selectedRackId || null,
      module_id: selectedModuleId || null,
      ns_spacing_m: nsSpacing,
      ew_spacing_m: ewSpacing,
      evaluated_results: layout?.evaluated_results ?? [],
      custom_layouts: layout?.custom_layouts ?? [],
      updated_at: new Date().toISOString(),
    }
    const { error } = await supabase.from('project_layouts').upsert(payload, { onConflict: 'project_id' })
    setSaving(false)
    if (error) toast.error(error.message)
    else { toast.success('Layout saved'); navigate('/') }
  }

  const kwDC = selectedRack && selectedModule && placements.length > 0
    ? calcKwDC(placements.length, selectedRack, selectedModule)
    : null

  if (loadingProject) {
    return <div className="flex-1 flex items-center justify-center"><Skeleton className="w-64 h-8" /></div>
  }

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Sidebar */}
      <aside className="w-72 flex-shrink-0 border-r overflow-y-auto bg-background p-4 space-y-4">
        <div>
          <h2 className="font-semibold text-sm">{project?.name}</h2>
          {project?.address && <p className="text-xs text-muted-foreground">{project.address}</p>}
        </div>

        <Separator />

        {/* Boundary */}
        <div className="space-y-2">
          <Label className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Boundary</Label>
          <Button
            size="sm"
            className="w-full"
            variant={drawMode === 'boundary' ? 'default' : 'outline'}
            onClick={() => setDrawMode(m => m === 'boundary' ? null : 'boundary')}
          >
            {drawMode === 'boundary' ? 'Click to finish drawing…' : boundary ? '✓ Redraw Boundary' : 'Draw Boundary'}
          </Button>
          {boundary && (
            <div className="flex items-center gap-2">
              <Label className="text-xs flex-1">Perimeter Offset (m)</Label>
              <Input
                type="number"
                min={0}
                step={1}
                value={perimeterOffset}
                onChange={e => setPerimeterOffset(parseFloat(e.target.value) || 0)}
                className="w-20 h-7 text-xs"
              />
            </div>
          )}
        </div>

        <Separator />

        {/* Keepouts */}
        <div className="space-y-2">
          <Label className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Keepout Zones</Label>
          <div className="flex items-center gap-2">
            <Label className="text-xs flex-1">Zone Offset (m)</Label>
            <Input
              type="number"
              min={0}
              step={1}
              defaultValue={5}
              onChange={e => { keepoutOffsetRef.current = parseFloat(e.target.value) || 0 }}
              className="w-20 h-7 text-xs"
            />
          </div>
          <Button
            size="sm"
            className="w-full"
            variant={drawMode === 'keepout' ? 'default' : 'outline'}
            onClick={() => setDrawMode(m => m === 'keepout' ? null : 'keepout')}
          >
            {drawMode === 'keepout' ? 'Click to finish drawing…' : '+ Draw Keepout'}
          </Button>
          {keepouts.length > 0 && (
            <div className="space-y-1">
              {keepouts.map((ko, i) => (
                <div key={ko.id} className="flex items-center justify-between text-xs bg-muted rounded px-2 py-1">
                  <span>Zone {i + 1} ({ko.offset_m}m buffer)</span>
                  <button onClick={() => handleRemoveKeepout(ko.id)} className="text-destructive hover:underline">remove</button>
                </div>
              ))}
            </div>
          )}
        </div>

        <Separator />

        {/* Rack + Module */}
        <div className="space-y-2">
          <Label className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Rack & Module</Label>
          <div className="space-y-1">
            <Label className="text-xs">Rack Type</Label>
            <Select value={selectedRackId} onValueChange={setSelectedRackId}>
              <SelectTrigger className="h-8 text-xs">
                <SelectValue placeholder="Select rack…" />
              </SelectTrigger>
              <SelectContent>
                {racks.map((r: Rack) => (
                  <SelectItem key={r.id} value={r.id}>{r.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <Label className="text-xs">PV Module</Label>
            <Select value={selectedModuleId} onValueChange={setSelectedModuleId}>
              <SelectTrigger className="h-8 text-xs">
                <SelectValue placeholder="Select module…" />
              </SelectTrigger>
              <SelectContent>
                {modules.map((m: Module) => (
                  <SelectItem key={m.id} value={m.id}>{m.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        {/* Spacing */}
        <div className="space-y-2">
          <Label className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Spacing</Label>
          <div className="flex items-center gap-2">
            <Label className="text-xs flex-1">N/S Spacing (m)</Label>
            <Input
              type="number" min={0.1} step={0.1}
              value={nsSpacing.toFixed(2)}
              onChange={e => handleNsChange(parseFloat(e.target.value) || 5)}
              className="w-20 h-7 text-xs"
            />
          </div>
          <div className="flex items-center gap-2">
            <Label className="text-xs flex-1">GCR</Label>
            <Input
              type="number" min={0.01} max={0.99} step={0.01}
              value={gcr !== null ? gcr.toFixed(3) : ''}
              onChange={e => handleGcrChange(parseFloat(e.target.value))}
              className="w-20 h-7 text-xs"
              disabled={!selectedRack}
            />
          </div>
          <div className="flex items-center gap-2">
            <Label className="text-xs flex-1">E/W Spacing (m)</Label>
            <Input
              type="number" min={0.1} step={0.1}
              value={ewSpacing}
              onChange={e => setEwSpacing(parseFloat(e.target.value) || 2)}
              className="w-20 h-7 text-xs"
            />
          </div>
        </div>

        <Button className="w-full" onClick={handleFill} disabled={!boundary || !selectedRack}>
          Fill
        </Button>

        {/* Live stats */}
        {placements.length > 0 && (
          <div className="bg-muted rounded-md p-3 space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Racks</span>
              <span className="font-semibold">{placements.length}</span>
            </div>
            {kwDC !== null && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">kW DC</span>
                <span className="font-semibold">{kwDC.toFixed(1)}</span>
              </div>
            )}
          </div>
        )}

        <Separator />

        <div className="space-y-2 pb-2">
          <Button
            className="w-full"
            variant="outline"
            onClick={() => navigate(`/projects/${projectId}/evaluate`)}
            disabled={!boundary}
          >
            Evaluate
          </Button>
          <Button className="w-full" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving…' : 'Save & Exit'}
          </Button>
        </div>

        {racks.length === 0 || modules.length === 0 ? (
          <Badge variant="outline" className="text-xs w-full justify-center">
            {racks.length === 0 ? 'Add racks in the Racking page' : 'Add modules in the Modules page'}
          </Badge>
        ) : null}
      </aside>

      {/* Map */}
      <div className="flex-1 relative">
        {project && (
          <LeafletMap
            lat={project.lat}
            lng={project.lng}
            onBoundaryDrawn={setBoundary}
            onKeepoutDrawn={handleAddKeepout}
            initialBoundary={layout?.boundary_geojson}
            initialKeeouts={layout?.keepouts_geojson ?? []}
            rackPlacements={placements.map(p => p.rackRect)}
            drawMode={drawMode}
            onDrawModeEnd={() => setDrawMode(null)}
          />
        )}
      </div>
    </div>
  )
}
