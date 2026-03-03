import { useState } from 'react'
import type { Rack } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

type FormValues = Omit<Rack, 'id' | 'user_id' | 'created_at'>

interface Props {
  initialValues?: FormValues
  onSubmit: (values: FormValues) => Promise<void>
  onCancel: () => void
  loading?: boolean
}

const empty: FormValues = { name: '', max_width_m: 4.268, max_height_m: 4.556, racking_type: 'fixed-tilt' }

export function RackForm({ initialValues, onSubmit, onCancel, loading }: Props) {
  const [values, setValues] = useState<FormValues>(initialValues ?? empty)

  const set = (key: keyof FormValues, val: string | number) =>
    setValues(prev => ({ ...prev, [key]: val }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await onSubmit(values)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-1">
        <Label>Rack Name</Label>
        <Input value={values.name} onChange={e => set('name', e.target.value)} required placeholder="e.g. Fixed Tilt 2V" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <Label>Max Width (m)</Label>
          <Input type="number" step="0.001" min="0" value={values.max_width_m} onChange={e => set('max_width_m', parseFloat(e.target.value))} required />
        </div>
        <div className="space-y-1">
          <Label>Max Height (m)</Label>
          <Input type="number" step="0.001" min="0" value={values.max_height_m} onChange={e => set('max_height_m', parseFloat(e.target.value))} required />
        </div>
      </div>
      <div className="space-y-1">
        <Label>Racking Type</Label>
        <Select value={values.racking_type} onValueChange={v => set('racking_type', v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="fixed-tilt">Fixed Tilt</SelectItem>
            <SelectItem value="tracker">Tracker</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>Cancel</Button>
        <Button type="submit" disabled={loading}>{loading ? 'Saving…' : 'Save'}</Button>
      </div>
    </form>
  )
}
