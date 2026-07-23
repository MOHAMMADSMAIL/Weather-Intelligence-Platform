const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function ExportPage() {
  return (
    <section className="page">
      <h2>Export Data</h2>
      <div className="export-actions">
        <a className="button" href={`${API_BASE}/export/json`} target="_blank" rel="noreferrer">
          Export JSON
        </a>
        <a className="button" href={`${API_BASE}/export/csv`} target="_blank" rel="noreferrer">
          Export CSV
        </a>
        <a className="button" href={`${API_BASE}/export/pdf`} target="_blank" rel="noreferrer">
          Export PDF
        </a>
      </div>
      <p>Use these buttons to download saved weather request data.</p>
    </section>
  )
}

export default ExportPage
