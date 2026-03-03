import { Outlet } from 'react-router-dom'
import { Navbar } from './Navbar'
import { Toaster } from '@/components/ui/sonner'

export function AppShell() {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>
      <Toaster richColors position="bottom-right" />
    </div>
  )
}
