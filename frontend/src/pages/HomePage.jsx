import { useState } from 'react'
import { fetchWeather, createRequest } from '../services/api'

function HomePage() {
  const today = new Date().toISOString().slice(0, 10)
  const [location, setLocation] = useState('')
  const [startDate, setStartDate] = useState(today)
  const [endDate, setEndDate] = useState(today)
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleSearch = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')
    setWeather(null)
    setLoading(true)
    try {
      const data = await fetchWeather(location)
      setWeather(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to fetch weather')
    } finally {
      setLoading(false)
    }
  }

  const handleCurrentLocation = async () => {
    setError('')
    setMessage('')
    setWeather(null)
    setLoading(true)

    if (!navigator.geolocation) {
      setError('Geolocation is not available in your browser')
      setLoading(false)
      return
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const data = await fetchWeather({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          })
          setWeather(data)
          setLocation(`${position.coords.latitude},${position.coords.longitude}`)
        } catch (err) {
          setError(err.response?.data?.detail || 'Unable to fetch weather')
        } finally {
          setLoading(false)
        }
      },
      (geolocationError) => {
        setError('Unable to get current location')
        setLoading(false)
      },
      { timeout: 10000 }
    )
  }

  const handleSave = async () => {
    if (!weather) {
      setError('Search weather before saving a request')
      return
    }

    setError('')
    setMessage('')
    setSaving(true)
    try {
      await createRequest({ location, start_date: startDate, end_date: endDate })
      setMessage('Weather request saved successfully')
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save request')
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="page">
      <h2>Search Weather</h2>
      <form className="search-form" onSubmit={handleSearch}>
        <input
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="City, postal code, landmark, or latitude,longitude"
        />
        <div className="date-row">
          <label>
            Start date
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </label>
          <label>
            End date
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </label>
        </div>
        <div className="button-row">
          <button type="submit" disabled={!location || loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
          <button type="button" className="secondary-button" onClick={handleCurrentLocation} disabled={loading}>
            Use Current Location
          </button>
        </div>
      </form>

      {error && <p className="error-message">{error}</p>}
      {message && <p className="success-message">{message}</p>}

      {weather && (
        <div className="weather-card">
          <h3>{weather.location}</h3>
          <div className="weather-summary">
            <div>
              <div className="weather-value">{weather.temperature}°C</div>
              <div>Condition: {weather.weather_condition}</div>
            </div>
            <div>
              <div>Humidity: {weather.humidity}%</div>
              <div>Wind: {weather.wind_speed} km/h</div>
              <div>Rain chance: {weather.precipitation_probability}%</div>
            </div>
          </div>

          <button className="save-button" type="button" disabled={saving} onClick={handleSave}>
            {saving ? 'Saving...' : 'Save Request'}
          </button>

          {weather.map_url && (
            <div className="map-link">
              <a href={weather.map_url} target="_blank" rel="noreferrer">
                View location on Google Maps
              </a>
            </div>
          )}

          <div className="forecast-grid">
            {weather.forecast.map((day) => (
              <div key={day.date} className="forecast-card">
                <strong>{day.date}</strong>
                <div>{day.condition}</div>
                <div>{day.min_temp}° / {day.max_temp}°</div>
                <div>Rain: {day.precipitation_probability}%</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}

export default HomePage
