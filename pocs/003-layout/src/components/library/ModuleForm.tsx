import { useState } from 'react'
import type { Module } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type FormValues = Omit<Module, 'id' | 'user_id' | 'created_at'>

interface Props {
  initialValues?: FormValues
  onSubmit: (values: FormValues) => Promise<void>
  onCancel: () => void
  loading?: boolean
}

const empty: FormValues = { name: '', width_m: 1.134, height_m: 2.278, power_w: 600 }

export function ModuleForm({ initialValues, onSubmit, onCancel, loading }: Props) {
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
        <Label>Module Name</Label>
        <Input value={values.name} onChange={e => set('name', e.target.value)} required placeholder="e.g. JinkoSolar 600W" />
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div className="space-y-1">
          <Label>Width (m)</Label>
          <Input type="number" step="0.001" min="0" value={values.width_m} onChange={e => set('width_m', parseFloat(e.target.value))} required />
        </div>
        <div className="space-y-1">
          <Label>Height (m)</Label>
          <Input type="number" step="0.001" min="0" value={values.height_m} onChange={e => set('height_m', parseFloat(e.target.value))} required />
        </div>
        <div className="space-y-1">
          <Label>Power (W)</Label>
          <Input type="number" step="1" min="0" value={values.power_w} onChange={e => set('power_w', parseFloat(e.target.value))} required />
        </div>
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>Cancel</Button>
        <Button type="submit" disabled={loading}>{loading ? 'Saving…' : 'Save'}</Button>
      </div>
    </form>
  )
}
