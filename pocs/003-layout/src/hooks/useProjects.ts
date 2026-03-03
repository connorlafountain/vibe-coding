import { useState, useEffect } from 'react'
import type { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import type { Project } from '@/types'

export function useProjects(user: User | null) {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { setLoading(false); return }
    supabase
      .from('projects')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })
      .then(({ data, error }) => {
        if (!error && data) setProjects(data as Project[])
        setLoading(false)
      })
  }, [user])

  const createProject = async (values: Omit<Project, 'id' | 'user_id' | 'created_at'>) => {
    const { data, error } = await supabase
      .from('projects')
      .insert({ ...values, user_id: user!.id })
      .select()
      .single()
    if (!error && data) setProjects(prev => [data as Project, ...prev])
    return { data, error }
  }

  const deleteProject = async (id: string) => {
    const { error } = await supabase.from('projects').delete().eq('id', id)
    if (!error) setProjects(prev => prev.filter(p => p.id !== id))
    return { error }
  }

  return { projects, loading, createProject, deleteProject }
}
