import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SelectArea from './pages/SelectArea'
import Results from './pages/Results'
import './App.css'

function App() {
  const [analysisData, setAnalysisData] = useState(null)
  const [language, setLanguage] = useState('en')
  const [farmerMode, setFarmerMode] = useState(false)
  const [credentials, setCredentials] = useState({ clientId: '', clientSecret: '' })

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar - Streamlit Style */}
        <aside className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-6">
            {/* Logo/Title */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <span className="text-3xl">🌾</span>
                CropGuard
              </h1>
              <p className="text-sm text-gray-600 mt-1">Crop Health Monitoring</p>
            </div>

            {/* Language Selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🌐 Language / भाषा / భాష
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="en">English</option>
                <option value="hi">हिंदी</option>
                <option value="te">తెలుగు</option>
              </select>
            </div>

            {/* Farmer Mode Toggle */}
            <div className="mb-6 p-4 bg-green-50 rounded-lg border border-green-200">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={farmerMode}
                  onChange={(e) => setFarmerMode(e.target.checked)}
                  className="w-4 h-4 text-green-600 rounded focus:ring-green-500"
                />
                <span className="ml-3 text-sm font-medium text-gray-700">
                  👨‍🌾 Farmer-Friendly Mode
                </span>
              </label>
              <p className="text-xs text-gray-600 mt-2">
                Simple language without technical terms
              </p>
            </div>

            {/* Credentials */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                🔐 Sentinel Hub Credentials
              </h3>
              <p className="text-xs text-gray-600 mb-3">
                Get free credentials from{' '}
                <a
                  href="https://www.sentinel-hub.com/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  Sentinel Hub
                </a>
              </p>
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Client ID
                  </label>
                  <input
                    type="password"
                    value={credentials.clientId}
                    onChange={(e) => setCredentials({ ...credentials, clientId: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Enter Client ID"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Client Secret
                  </label>
                  <input
                    type="password"
                    value={credentials.clientSecret}
                    onChange={(e) => setCredentials({ ...credentials, clientSecret: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Enter Client Secret"
                  />
                </div>
              </div>
            </div>

            {/* About */}
            <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">ℹ️ About</h3>
              <p className="text-xs text-gray-600 leading-relaxed">
                CropGuard uses satellite data to monitor crop health via NDVI analysis.
              </p>
              <div className="mt-3 text-xs text-gray-600">
                <p className="font-semibold mb-1">Features:</p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li>📍 GPS location detection</li>
                  <li>🔍 Global location search</li>
                  <li>✏️ Interactive map drawing</li>
                  <li>🛰️ Real Sentinel-2 data</li>
                  <li>📊 Health classification</li>
                </ul>
              </div>
            </div>

            {/* Footer */}
            <div className="text-xs text-gray-500 text-center pt-4 border-t border-gray-200">
              <p>Data: Copernicus Sentinel-2 (ESA)</p>
            </div>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route
              path="/"
              element={
                <SelectArea
                  onAnalysisComplete={setAnalysisData}
                  language={language}
                  credentials={credentials}
                />
              }
            />
            <Route
              path="/results"
              element={
                <Results
                  data={analysisData}
                  language={language}
                  farmerMode={farmerMode}
                />
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
