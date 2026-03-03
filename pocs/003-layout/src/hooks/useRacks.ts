import { useState, useEffect } from 'react'
import type { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import type { Rack } from '@/types'

export function useRacks(user: User | null) {
  const [racks, setRacks] = useState<Rack[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { setLoading(false); return }
    supabase
      .from('racks')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: true })
      .then(({ data, error }) => {
        if (!error && data) setRacks(data as Rack[])
        setLoading(false)
      })
  }, [user])

  const createRack = async (values: Omit<Rack, 'id' | 'user_id' | 'created_at'>) => {
    const { data, error } = await supabase
      .from('racks')
      .insert({ ...values, user_id: user!.id })
      .select()
      .single()
    if (!error && data) setRacks(prev => [...prev, data as Rack])
    return { data, error }
  }

  const updateRack = async (id: string, values: Partial<Omit<Rack, 'id' | 'user_id' | 'created_at'>>) => {
    const { data, error } = await supabase
      .from('racks')
      .update(values)
      .eq('id', id)
      .select()
      .single()
    if (!error && data) setRacks(prev => prev.map(r => r.id === id ? data as Rack : r))
    return { data, error }
  }

  const deleteRack = async (id: string) => {
    const { error } = await supabase.from('racks').delete().eq('id', id)
    if (!error) setRacks(prev => prev.filter(r => r.id !== id))
    return { error }
  }

  return { racks, loading, createRack, updateRack, deleteRack }
}
