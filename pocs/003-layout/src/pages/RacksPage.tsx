import { useState } from 'react'
import { toast } from 'sonner'
import { useAuth } from '@/hooks/useAuth'
import { useRacks } from '@/hooks/useRacks'
import type { Rack } from '@/types'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Skeleton } from '@/components/ui/skeleton'
import { RackForm } from '@/components/library/RackForm'

type FormValues = Omit<Rack, 'id' | 'user_id' | 'created_at'>

export function RacksPage() {
  const { user } = useAuth()
  const { racks, loading, createRack, updateRack, deleteRack } = useRacks(user)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Rack | null>(null)
  const [deleting, setDeleting] = useState<Rack | null>(null)
  const [saving, setSaving] = useState(false)

  const openCreate = () => { setEditing(null); setDialogOpen(true) }
  const openEdit = (r: Rack) => { setEditing(r); setDialogOpen(true) }

  const handleSubmit = async (values: FormValues) => {
    setSaving(true)
    if (editing) {
      const { error } = await updateRack(editing.id, values)
      if (error) toast.error(error.message)
      else toast.success('Rack updated')
    } else {
      const { error } = await createRack(values)
      if (error) toast.error(error.message)
      else toast.success('Rack created')
    }
    setSaving(false)
    setDialogOpen(false)
  }

  const handleDelete = async () => {
    if (!deleting) return
    const { error } = await deleteRack(deleting.id)
    if (error) toast.error(error.message)
    else toast.success('Rack deleted')
    setDeleting(null)
  }

  return (
    <div className="max-w-screen-lg mx-auto p-6 w-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">Racking</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Your racking library</p>
        </div>
        <Button onClick={openCreate}>+ Add Rack</Button>
      </div>

      {loading ? (
        <div className="space-y-2">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
        </div>
      ) : racks.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">No racks yet. Add your first one.</div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead className="text-right">Max Width (m)</TableHead>
              <TableHead className="text-right">Max Height (m)</TableHead>
              <TableHead>Type</TableHead>
              <TableHead className="w-24" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {racks.map(r => (
              <TableRow key={r.id}>
                <TableCell className="font-medium">{r.name}</TableCell>
                <TableCell className="text-right">{r.max_width_m}</TableCell>
                <TableCell className="text-right">{r.max_height_m}</TableCell>
                <TableCell>
                  <Badge variant={r.racking_type === 'tracker' ? 'default' : 'secondary'}>
                    {r.racking_type}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex justify-end gap-2">
                    <Button size="sm" variant="outline" onClick={() => openEdit(r)}>Edit</Button>
                    <Button size="sm" variant="destructive" onClick={() => setDeleting(r)}>Delete</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editing ? 'Edit Rack' : 'Add Rack'}</DialogTitle>
          </DialogHeader>
          <RackForm
            initialValues={editing ? { name: editing.name, max_width_m: editing.max_width_m, max_height_m: editing.max_height_m, racking_type: editing.racking_type } : undefined}
            onSubmit={handleSubmit}
            onCancel={() => setDialogOpen(false)}
            loading={saving}
          />
        </DialogContent>
      </Dialog>

      <AlertDialog open={!!deleting} onOpenChange={open => { if (!open) setDeleting(null) }}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete rack?</AlertDialogTitle>
            <AlertDialogDescription>
              "{deleting?.name}" will be permanently deleted.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
