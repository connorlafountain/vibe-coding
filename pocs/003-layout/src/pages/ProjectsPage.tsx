import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useAuth } from '@/hooks/useAuth'
import { useProjects } from '@/hooks/useProjects'
import type { Project } from '@/types'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'
import { Skeleton } from '@/components/ui/skeleton'
import { ProjectForm } from '@/components/projects/ProjectForm'

type FormValues = Omit<Project, 'id' | 'user_id' | 'created_at'>

export function ProjectsPage() {
  const { user } = useAuth()
  const { projects, loading, createProject, deleteProject } = useProjects(user)
  const navigate = useNavigate()
  const [dialogOpen, setDialogOpen] = useState(false)
  const [deleting, setDeleting] = useState<Project | null>(null)
  const [saving, setSaving] = useState(false)

  const handleCreate = async (values: FormValues) => {
    setSaving(true)
    const { error } = await createProject(values)
    setSaving(false)
    if (error) toast.error(error.message)
    else { toast.success('Project created'); setDialogOpen(false) }
  }

  const handleDelete = async () => {
    if (!deleting) return
    const { error } = await deleteProject(deleting.id)
    if (error) toast.error(error.message)
    else toast.success('Project deleted')
    setDeleting(null)
  }

  return (
    <div className="max-w-screen-lg mx-auto p-6 w-full">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">Projects</h1>
          <p className="text-sm text-muted-foreground mt-0.5">Manage your solar farm layouts</p>
        </div>
        <Button onClick={() => setDialogOpen(true)}>+ New Project</Button>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => <Skeleton key={i} className="h-40" />)}
        </div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          <p className="text-base mb-2">No projects yet.</p>
          <Button onClick={() => setDialogOpen(true)}>Create your first project</Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map(p => (
            <Card key={p.id} className="flex flex-col">
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{p.name}</CardTitle>
              </CardHeader>
              <CardContent className="flex-1 pb-3">
                {p.address && <p className="text-sm text-muted-foreground">{p.address}</p>}
                <p className="text-xs text-muted-foreground mt-1">
                  {p.lat.toFixed(5)}, {p.lng.toFixed(5)}
                </p>
              </CardContent>
              <CardFooter className="flex gap-2 pt-0">
                <Button className="flex-1" onClick={() => navigate(`/projects/${p.id}/map`)}>
                  Open Map
                </Button>
                <Button variant="destructive" size="sm" onClick={() => setDeleting(p)}>
                  Delete
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>New Project</DialogTitle>
          </DialogHeader>
          <ProjectForm
            onSubmit={handleCreate}
            onCancel={() => setDialogOpen(false)}
            loading={saving}
          />
        </DialogContent>
      </Dialog>

      <AlertDialog open={!!deleting} onOpenChange={open => { if (!open) setDeleting(null) }}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete project?</AlertDialogTitle>
            <AlertDialogDescription>
              "{deleting?.name}" and all its layouts will be permanently deleted.
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
