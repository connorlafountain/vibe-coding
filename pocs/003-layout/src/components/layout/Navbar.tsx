import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'

const links = [
  { to: '/', label: 'Projects' },
  { to: '/modules', label: 'Modules' },
  { to: '/racks', label: 'Racking' },
]

export function Navbar() {
  const { user, signOut } = useAuth()
  const location = useLocation()

  return (
    <header className="border-b bg-background">
      <div className="max-w-screen-xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <span className="font-semibold text-base tracking-tight">☀️ Anza SolarPro</span>
          <nav className="flex items-center gap-1">
            {links.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={`text-sm px-3 py-1.5 rounded-md transition-colors ${
                  location.pathname === to
                    ? 'bg-muted font-medium'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                }`}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground hidden sm:block">{user?.email}</span>
          <Button variant="outline" size="sm" onClick={() => signOut()}>
            Sign out
          </Button>
        </div>
      </div>
    </header>
  )
}
