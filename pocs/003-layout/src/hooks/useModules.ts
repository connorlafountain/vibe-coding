import { useState, useEffect } from 'react'
import type { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import type { Module } from '@/types'

export function useModules(user: User | null) {
  const [modules, setModules] = useState<Module[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { setLoading(false); return }
    supabase
      .from('modules')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: true })
      .then(({ data, error }) => {
        if (!error && data) setModules(data as Module[])
        setLoading(false)
      })
  }, [user])

  const createModule = async (values: Omit<Module, 'id' | 'user_id' | 'created_at'>) => {
    const { data, error } = await supabase
      .from('modules')
      .insert({ ...values, user_id: user!.id })
      .select()
      .single()
    if (!error && data) setModules(prev => [...prev, data as Module])
    return { data, error }
  }

  const updateModule = async (id: string, values: Partial<Omit<Module, 'id' | 'user_id' | 'created_at'>>) => {
    const { data, error } = await supabase
      .from('modules')
      .update(values)
      .eq('id', id)
      .select()
      .single()
    if (!error && data) setModules(prev => prev.map(m => m.id === id ? data as Module : m))
    return { data, error }
  }

  const deleteModule = async (id: string) => {
    const { error } = await supabase.from('modules').delete().eq('id', id)
    if (!error) setModules(prev => prev.filter(m => m.id !== id))
    return { error }
  }

  return { modules, loading, createModule, updateModule, deleteModule }
}
