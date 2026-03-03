import { useState } from 'react'
import { toast } from 'sonner'
import { useAuth } from '@/hooks/useAuth'
import { useModules } from '@/hooks/useModules'
import type { Module } from '@/types'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Skeleton } from '@/components/ui/skeleton'
import { ModuleForm } from '@/components/library/ModuleForm'

type FormValues = Omit<Module, 'id' | 'user_id' | 'created_at'>

export function ModulesPage() {
  const { user } = useAuth()
  const { modules, loading, createModule, updateModule, deleteModule } = useModules(user)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Module | null>(null)
  const [deleting, setDeleting] = useState<Module | null>(null)
  const [saving, setSaving] = useState(false)

  const openCreate = () => { setEditing(null); setDialogOpen(true) }
  const openEdit = (m: Module) => { setEditing(m); setDialogOpen(true) }

  const handleSubmit = async (values: FormValues) => {
    setSaving(true)
    if (editing) {
      const { error } = await updateModule(editing.id, values)
      if (error) toast.error(error.message)
      else toast.success('Module updated')
    } else {
      const { error } = await createModule(values)
      if (error) toast.error(error.message)
      else toast.success('Module created')
    }
    setSaving(false)
    setDialogOpen(false)
  }

  const handleDelete = async () => {
    if (!deleting) return
    const { error } = await deleteModule(deleting.id)
    if (error) toast.error(error.message)
    else toast.success('Module deleted')
    setDeleting(null)
  }

  return (
    <div className="max-w-screen-lg mx-auto p-6 w-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">PV Modules</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Your module library</p>
        </div>
        <Button onClick={openCreate}>+ Add Module</Button>
      </div>

      {loading ? (
        <div className="space-y-2">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
        </div>
      ) : modules.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">No modules yet. Add your first one.</div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead className="text-right">Width (m)</TableHead>
              <TableHead className="text-right">Height (m)</TableHead>
              <TableHead className="text-right">Power (W)</TableHead>
              <TableHead className="w-24" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {modules.map(m => (
              <TableRow key={m.id}>
                <TableCell className="font-medium">{m.name}</TableCell>
                <TableCell className="text-right">{m.width_m}</TableCell>
                <TableCell className="text-right">{m.height_m}</TableCell>
                <TableCell className="text-right">{m.power_w}</TableCell>
                <TableCell>
                  <div className="flex justify-end gap-2">
                    <Button size="sm" variant="outline" onClick={() => openEdit(m)}>Edit</Button>
                    <Button size="sm" variant="destructive" onClick={() => setDeleting(m)}>Delete</Button>
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
            <DialogTitle>{editing ? 'Edit Module' : 'Add Module'}</DialogTitle>
          </DialogHeader>
          <ModuleForm
            initialValues={editing ? { name: editing.name, width_m: editing.width_m, height_m: editing.height_m, power_w: editing.power_w } : undefined}
            onSubmit={handleSubmit}
            onCancel={() => setDialogOpen(false)}
            loading={saving}
          />
        </DialogContent>
      </Dialog>

      <AlertDialog open={!!deleting} onOpenChange={open => { if (!open) setDeleting(null) }}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete module?</AlertDialogTitle>
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
