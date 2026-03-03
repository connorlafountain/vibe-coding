import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import type { EvaluatedResult, CustomLayout, Rack, Module } from '@/types'
import { runFill } from '@/utils/fillAlgorithm'
import { calcKwDC, calcGCR, nsSpacingFromGCR } from '@/utils/optimizer'
import { TrialHistogram } from './TrialHistogram'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { HoverCard, HoverCardContent, HoverCardTrigger } from '@/components/ui/hover-card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface Props {
  results: EvaluatedResult[]
  customLayouts: CustomLayout[]
  boundary: GeoJSON.Feature<GeoJSON.Polygon>
  keepouts: import('@/types').KeepoutFeature[]
  perimeterOffset: number
  racks: Rack[]
  modules: Module[]
  onCustomSave: (layout: CustomLayout) => void
}

export function ResultsTable({ results, customLayouts, boundary, keepouts, perimeterOffset, racks, modules, onCustomSave }: Props) {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [editTarget, setEditTarget] = useState<EvaluatedResult | CustomLayout | null>(null)
  const [editNs, setEditNs] = useState(5)
  const [editEw, setEditEw] = useState(2)
  const [editGcr, setEditGcr] = useState(0)
  const [editLabel, setEditLabel] = useState('')
  const [editPreview, setEditPreview] = useState<{ rack_count: number; kw_dc: number } | null>(null)

  const openEdit = (r: EvaluatedResult | CustomLayout) => {
    setEditTarget(r)
    setEditNs(r.ns_spacing_m)
    setEditEw(r.ew_spacing_m)
    setEditGcr(r.gcr)
    setEditLabel('label' in r ? r.label : `Custom — ${r.rack_name} + ${r.module_name}`)
    setEditPreview({ rack_count: r.rack_count, kw_dc: r.kw_dc })
  }

  const handleEditNsChange = (val: number) => {
    setEditNs(val)
    const rack = racks.find(r => r.id === editTarget?.rack_id)
    if (rack) setEditGcr(calcGCR(rack, val))
    runEditPreview(editTarget?.rack_id, editTarget?.module_id, val, editEw)
  }

  const handleEditGcrChange = (val: number) => {
    setEditGcr(val)
    const rack = racks.find(r => r.id === editTarget?.rack_id)
    if (rack && val > 0 && val < 1) {
      const ns = nsSpacingFromGCR(rack, val)
      setEditNs(ns)
      runEditPreview(editTarget?.rack_id, editTarget?.module_id, ns, editEw)
    }
  }

  const handleEditEwChange = (val: number) => {
    setEditEw(val)
    runEditPreview(editTarget?.rack_id, editTarget?.module_id, editNs, val)
  }

  const runEditPreview = (rackId?: string, moduleId?: string, ns = editNs, ew = editEw) => {
    if (!rackId || !moduleId) return
    const rack = racks.find(r => r.id === rackId)
    const module = modules.find(m => m.id === moduleId)
    if (!rack || !module) return
    const placements = runFill({ boundary, keepouts, perimeterOffset, rack, ns_spacing_m: ns, ew_spacing_m: ew })
    const kw_dc = calcKwDC(placements.length, rack, module)
    setEditPreview({ rack_count: placements.length, kw_dc })
  }

  const handleSaveCustom = () => {
    if (!editTarget) return
    const rack = racks.find(r => r.id === editTarget.rack_id)
    const module = modules.find(m => m.id === editTarget.module_id)
    if (!rack || !module || !editPreview) return
    const custom: CustomLayout = {
      ...editTarget,
      custom_id: crypto.randomUUID(),
      label: editLabel,
      gcr: editGcr,
      ns_spacing_m: editNs,
      ew_spacing_m: editEw,
      rack_count: editPreview.rack_count,
      kw_dc: editPreview.kw_dc,
      trials: [],
    }
    onCustomSave(custom)
    setEditTarget(null)
  }

  const handleUseLayout = (r: EvaluatedResult | CustomLayout) => {
    navigate(`/projects/${projectId}/map?ns=${r.ns_spacing_m}&ew=${r.ew_spacing_m}&rack=${r.rack_id}&module=${r.module_id}`)
  }

  const allRows: (EvaluatedResult & { isCustom?: boolean; label?: string })[] = [
    ...customLayouts.map(c => ({ ...c, isCustom: true })),
    ...results,
  ].sort((a, b) => b.kw_dc - a.kw_dc)

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Module</TableHead>
            <TableHead>Rack</TableHead>
            <TableHead className="text-right">GCR</TableHead>
            <TableHead className="text-right">N/S (m)</TableHead>
            <TableHead className="text-right">E/W (m)</TableHead>
            <TableHead className="text-right">Racks</TableHead>
            <TableHead className="text-right">kW DC</TableHead>
            <TableHead className="w-32" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {allRows.map((r, i) => (
            <HoverCard key={`${r.rack_id}-${r.module_id}-${i}`} openDelay={300}>
              <HoverCardTrigger asChild>
                <TableRow
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => handleUseLayout(r)}
                >
                  <TableCell className="font-medium">
                    {r.isCustom && <Badge variant="secondary" className="mr-1.5 text-xs">Custom</Badge>}
                    {r.module_name}
                  </TableCell>
                  <TableCell>{r.rack_name}</TableCell>
                  <TableCell className="text-right">{r.gcr.toFixed(3)}</TableCell>
                  <TableCell className="text-right">{r.ns_spacing_m.toFixed(1)}</TableCell>
                  <TableCell className="text-right">{r.ew_spacing_m.toFixed(1)}</TableCell>
                  <TableCell className="text-right">{r.rack_count}</TableCell>
                  <TableCell className="text-right font-semibold">{r.kw_dc.toFixed(1)}</TableCell>
                  <TableCell onClick={e => e.stopPropagation()}>
                    <Button size="sm" variant="outline" onClick={() => openEdit(r)}>
                      Edit Layout
                    </Button>
                  </TableCell>
                </TableRow>
              </HoverCardTrigger>
              {r.trials.length > 0 && (
                <HoverCardContent side="left" className="w-auto p-0">
                  <TrialHistogram trials={r.trials} />
                </HoverCardContent>
              )}
            </HoverCard>
          ))}
        </TableBody>
      </Table>

      {/* Edit Layout Dialog */}
      <Dialog open={!!editTarget} onOpenChange={open => { if (!open) setEditTarget(null) }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Layout</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-1">
              <Label>Label</Label>
              <Input value={editLabel} onChange={e => setEditLabel(e.target.value)} />
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div className="space-y-1">
                <Label>N/S Spacing (m)</Label>
                <Input type="number" step="0.1" min="0.1" value={editNs.toFixed(2)} onChange={e => handleEditNsChange(parseFloat(e.target.value))} />
              </div>
              <div className="space-y-1">
                <Label>GCR</Label>
                <Input type="number" step="0.01" min="0.01" max="0.99" value={editGcr.toFixed(3)} onChange={e => handleEditGcrChange(parseFloat(e.target.value))} />
              </div>
              <div className="space-y-1">
                <Label>E/W Spacing (m)</Label>
                <Input type="number" step="0.1" min="0.1" value={editEw.toFixed(2)} onChange={e => handleEditEwChange(parseFloat(e.target.value))} />
              </div>
            </div>
            {editPreview && (
              <div className="bg-muted rounded p-3 flex gap-6 text-sm">
                <div><span className="text-muted-foreground">Racks: </span><strong>{editPreview.rack_count}</strong></div>
                <div><span className="text-muted-foreground">kW DC: </span><strong>{editPreview.kw_dc.toFixed(1)}</strong></div>
              </div>
            )}
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setEditTarget(null)}>Cancel</Button>
              <Button onClick={handleSaveCustom}>Save as Custom Layout</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
