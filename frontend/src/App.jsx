import { Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import HistoryPage from './pages/HistoryPage'
import ExportPage from './pages/ExportPage'
import AssistantPage from './pages/AssistantPage'

function App() {
  return (
    <div className="app-shell">
      <header className="site-header">
        <div>
          <h1>Weather Intelligence Platform</h1>
          <p>Global weather search, history, export, and AI recommendations.</p>
        </div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/history">History</Link>
          <Link to="/export">Export</Link>
          <Link to="/assistant">Assistant</Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/export" element={<ExportPage />} />
          <Route path="/assistant" element={<AssistantPage />} />
        </Routes>
      </main>
      <footer className="app-footer">
        <p>Made by student MUHAMMAD ISMAIL</p>
      </footer>
    </div>
  )
}

export default App
