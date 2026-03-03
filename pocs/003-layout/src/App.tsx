import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { LoginPage } from '@/pages/LoginPage'
import { ProjectsPage } from '@/pages/ProjectsPage'
import { ModulesPage } from '@/pages/ModulesPage'
import { RacksPage } from '@/pages/RacksPage'
import { ProjectMapPage } from '@/pages/ProjectMapPage'
import { EvaluatePage } from '@/pages/EvaluatePage'

function ProtectedRoute() {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-muted-foreground text-sm">Loading…</div>
      </div>
    )
  }
  return user ? <Outlet /> : <Navigate to="/login" replace />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route path="/" element={<ProjectsPage />} />
            <Route path="/modules" element={<ModulesPage />} />
            <Route path="/racks" element={<RacksPage />} />
            <Route path="/projects/:id/map" element={<ProjectMapPage />} />
            <Route path="/projects/:id/evaluate" element={<EvaluatePage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
