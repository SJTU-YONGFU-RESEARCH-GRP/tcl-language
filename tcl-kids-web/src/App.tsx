import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { SiteHeader } from './components/SiteHeader'
import { Home } from './pages/Home'
import { Roadmap } from './pages/Roadmap'
import { WeekPage } from './pages/WeekPage'
import { ExamplePage } from './pages/ExamplePage'
import { Help } from './pages/Help'
import { Glossary } from './pages/Glossary'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <SiteHeader />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/week/:weekId" element={<WeekPage />} />
          <Route path="/week/:weekId/example/:exampleId" element={<ExamplePage />} />
          <Route path="/help" element={<Help />} />
          <Route path="/glossary" element={<Glossary />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
