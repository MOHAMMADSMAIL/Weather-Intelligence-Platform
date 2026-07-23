import { useEffect, useState } from 'react'
import { getRequests, deleteRequest, updateRequest } from '../services/api'

function HistoryPage() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editId, setEditId] = useState(null)
  const [editData, setEditData] = useState({ location: '', start_date: '', end_date: '' })

  const loadRecords = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getRequests()
      setRecords(data)
    } catch (err) {
      setError('Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteRequest(id)
      setRecords((prev) => prev.filter((record) => record.id !== id))
    } catch (err) {
      setError('Unable to delete record')
    }
  }

  const startEdit = (record) => {
    setEditId(record.id)
    setEditData({ location: record.location, start_date: record.start_date, end_date: record.end_date })
    setError('')
  }

  const handleUpdate = async (id) => {
    try {
      const updated = await updateRequest(id, editData)
      setRecords((prev) => prev.map((record) => (record.id === id ? updated : record)))
      setEditId(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to update record')
    }
  }

  useEffect(() => {
    loadRecords()
  }, [])

  return (
    <section className="page">
      <h2>Search History</h2>
      {loading && <p>Loading saved requests...</p>}
      {error && <p className="error-message">{error}</p>}
      {!loading && records.length === 0 && <p>No previous weather requests found.</p>}
      <div className="history-list">
        {records.map((record) => (
          <div key={record.id} className="history-card">
            <div className="history-content">
              {editId === record.id ? (
                <>
                  <label>
                    Location
                    <input
                      value={editData.location}
                      onChange={(e) => setEditData({ ...editData, location: e.target.value })}
                    />
                  </label>
                  <label>
                    Start
                    <input
                      type="date"
                      value={editData.start_date}
                      onChange={(e) => setEditData({ ...editData, start_date: e.target.value })}
                    />
                  </label>
                  <label>
                    End
                    <input
                      type="date"
                      value={editData.end_date}
                      onChange={(e) => setEditData({ ...editData, end_date: e.target.value })}
                    />
                  </label>
                </>
              ) : (
                <>
                  <strong>{record.location}</strong>
                  <div>{new Date(record.request_date).toLocaleString()}</div>
                  <div>Range: {record.start_date} to {record.end_date}</div>
                </>
              )}
            </div>
            <div className="history-actions">
              {editId === record.id ? (
                <>
                  <button onClick={() => handleUpdate(record.id)}>Save</button>
                  <button onClick={() => setEditId(null)}>Cancel</button>
                </>
              ) : (
                <>
                  <button onClick={() => startEdit(record)}>Edit</button>
                  <button onClick={() => handleDelete(record.id)}>Delete</button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default HistoryPage
