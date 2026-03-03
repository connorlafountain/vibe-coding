import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import type { Project } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type FormValues = Omit<Project, 'id' | 'user_id' | 'created_at'>

interface Props {
  onSubmit: (values: FormValues) => Promise<void>
  onCancel: () => void
  loading?: boolean
}

export function ProjectForm({ onSubmit, onCancel, loading }: Props) {
  const [name, setName] = useState('')
  const [address, setAddress] = useState('')
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null)
  const [searching, setSearching] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)

  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const markerRef = useRef<L.Marker | null>(null)

  // Init mini map after modal has rendered
  useEffect(() => {
    const timer = setTimeout(() => {
      if (mapRef.current || !mapContainerRef.current) return
      const map = L.map(mapContainerRef.current, { zoomControl: true }).setView([39.5, -98.35], 3)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
      }).addTo(map)
      mapRef.current = map
    }, 100)

    return () => {
      clearTimeout(timer)
      mapRef.current?.remove()
      mapRef.current = null
    }
  }, [])

  const searchAddress = async () => {
    if (!address.trim()) return
    setSearching(true)
    setSearchError(null)
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`,
        { headers: { 'Accept-Language': 'en' } }
      )
      const data = await res.json()
      if (!data.length) {
        setSearchError('Address not found. Try a more specific address.')
        return
      }
      const { lat, lon, display_name } = data[0]
      const newCoords = { lat: parseFloat(lat), lng: parseFloat(lon) }
      setCoords(newCoords)
      setAddress(display_name.split(',').slice(0, 3).join(',').trim())

      const map = mapRef.current
      if (map) {
        map.flyTo([newCoords.lat, newCoords.lng], 15, { duration: 1 })
        markerRef.current?.remove()
        markerRef.current = L.marker([newCoords.lat, newCoords.lng]).addTo(map)
      }
    } catch {
      setSearchError('Search failed. Please try again.')
    } finally {
      setSearching(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!coords) { setSearchError('Search for an address first.'); return }
    await onSubmit({ name, address, lat: coords.lat, lng: coords.lng })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-1">
        <Label>Project Name</Label>
        <Input
          value={name}
          onChange={e => setName(e.target.value)}
          required
          placeholder="e.g. Desert Sun Farm"
          autoFocus
        />
      </div>
      <div className="space-y-1">
        <Label>Address</Label>
        <div className="flex gap-2">
          <Input
            value={address}
            onChange={e => { setAddress(e.target.value); setSearchError(null); setCoords(null) }}
            onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); searchAddress() } }}
            placeholder="123 Solar Rd, Barstow, CA"
          />
          <Button type="button" onClick={searchAddress} disabled={searching || !address.trim()}>
            {searching ? '…' : 'Search'}
          </Button>
        </div>
        {searchError && <p className="text-sm text-destructive">{searchError}</p>}
        {coords && (
          <p className="text-xs text-muted-foreground">
            {coords.lat.toFixed(5)}, {coords.lng.toFixed(5)}
          </p>
        )}
      </div>

      {/* Location preview map */}
      <div
        ref={mapContainerRef}
        className="w-full rounded-md border overflow-hidden"
        style={{ height: 220 }}
      />

      <div className="flex justify-end gap-2 pt-1">
        <Button type="button" variant="outline" onClick={onCancel}>Cancel</Button>
        <Button type="submit" disabled={loading || !coords}>
          {loading ? 'Creating…' : 'Create Project'}
        </Button>
      </div>
    </form>
  )
}
