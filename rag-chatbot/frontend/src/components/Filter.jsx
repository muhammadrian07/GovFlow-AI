import React from 'react'
import './Filter.css'

/**
 * Filter component
 * Country selector for RAG context filtering
 * 
 * @param {string} selectedCountry - Currently selected country
 * @param {Function} onCountryChange - Callback when country changes
 */
const Filter = ({ selectedCountry, onCountryChange }) => {
  const countries = [
    'USA',
    'UK',
    'Canada',
    'Australia',
    'Germany',
    'France',
    'Japan',
    'India',
    'Pakistan'
  ]

  return (
    <div className="filter-container">
      <label htmlFor="country-select">Select Country:</label>
      <select
        id="country-select"
        value={selectedCountry}
        onChange={(e) => onCountryChange(e.target.value)}
        className="country-select"
      >
        {countries.map(country => (
          <option key={country} value={country}>
            🌍 {country}
          </option>
        ))}
      </select>
      <p className="filter-hint">
        Results will be filtered for {selectedCountry} policies
      </p>
    </div>
  )
}

export default Filter
