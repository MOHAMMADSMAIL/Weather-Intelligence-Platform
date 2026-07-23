import { useState } from 'react'
import { assistant } from '../services/api'

function AssistantPage() {
  const [question, setQuestion] = useState('Do I need a jacket today in London?')
  const [weatherData, setWeatherData] = useState({
    temperature: 12,
    wind_speed: 18,
    precipitation_probability: 70,
    weather_condition: 'Rain',
  })
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setResponse(null)
    setLoading(true)
    try {
      const data = await assistant({ question, weather_data: weatherData })
      setResponse(data.recommendation)
    } catch (err) {
      setError(err.response?.data?.detail || 'Assistant unavailable')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="page">
      <h2>AI Weather Assistant</h2>
      <form className="assistant-form" onSubmit={handleSubmit}>
        <label>
          Question
          <input value={question} onChange={(e) => setQuestion(e.target.value)} />
        </label>
        <label>
          Temperature (°C)
          <input
            type="number"
            value={weatherData.temperature}
            onChange={(e) => setWeatherData({ ...weatherData, temperature: Number(e.target.value) })}
          />
        </label>
        <label>
          Wind speed (km/h)
          <input
            type="number"
            value={weatherData.wind_speed}
            onChange={(e) => setWeatherData({ ...weatherData, wind_speed: Number(e.target.value) })}
          />
        </label>
        <label>
          Rain chance (%)
          <input
            type="number"
            value={weatherData.precipitation_probability}
            onChange={(e) => setWeatherData({ ...weatherData, precipitation_probability: Number(e.target.value) })}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Ask Assistant'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}
      {response && (
        <div className="assistant-response">
          <h3>Recommendation</h3>
          <p>{response}</p>
        </div>
      )}
    </section>
  )
}

export default AssistantPage
