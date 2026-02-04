import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { runAnalysis, loadDemoScenario } from '../services/api'

export default function SelectArea({ onAnalysisComplete, language, credentials }) {
    const navigate = useNavigate()
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [activeTab, setActiveTab] = useState('select')

    const [formData, setFormData] = useState({
        minLat: 17.385,
        minLon: 78.486,
        maxLat: 17.395,
        maxLon: 78.496,
        areaKm2: 1.0
    })

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: parseFloat(e.target.value)
        })
    }

    const handleRunAnalysis = async () => {
        if (!credentials.clientId || !credentials.clientSecret) {
            setError('Please enter Sentinel Hub credentials in the sidebar')
            return
        }

        setLoading(true)
        setError(null)

        try {
            const bbox = {
                min_x: formData.minLon,
                min_y: formData.minLat,
                max_x: formData.maxLon,
                max_y: formData.maxLat
            }

            const result = await runAnalysis(
                bbox,
                formData.areaKm2,
                credentials.clientId,
                credentials.clientSecret
            )

            onAnalysisComplete(result)
            navigate('/results')
        } catch (err) {
            setError(err.response?.data?.detail || err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleLoadDemo = async () => {
        setLoading(true)
        setError(null)

        try {
            const result = await loadDemoScenario()
            onAnalysisComplete(result)
            navigate('/results')
        } catch (err) {
            setError(err.response?.data?.detail || err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="h-full bg-white">
            {/* Page Header */}
            <div className="border-b border-gray-200 bg-white px-8 py-6">
                <h1 className="text-3xl font-bold text-gray-800">🌾 CropGuard - Crop Health Monitoring</h1>
                <p className="text-gray-600 mt-2">Automated crop health assessment using Sentinel-2 satellite imagery</p>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200 bg-white px-8">
                <div className="flex gap-2">
                    <button
                        onClick={() => setActiveTab('select')}
                        className={`px-6 py-3 font-medium border-b-2 transition ${activeTab === 'select'
                                ? 'border-red-500 text-red-600'
                                : 'border-transparent text-gray-600 hover:text-gray-800'
                            }`}
                    >
                        📍 Select Area
                    </button>
                    <button
                        onClick={() => navigate('/results')}
                        className="px-6 py-3 font-medium border-b-2 border-transparent text-gray-600 hover:text-gray-800 transition"
                    >
                        📊 Analysis Results
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="px-8 py-6 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>
                {/* Demo Mode Button - Prominent */}
                <div className="mb-8 p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border-2 border-purple-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <h3 className="text-lg font-bold text-purple-900 mb-2">🎬 Demo Mode</h3>
                            <p className="text-sm text-purple-700">
                                Click to instantly load a pre-configured HIGH RISK scenario for presentation
                            </p>
                        </div>
                        <button
                            onClick={handleLoadDemo}
                            disabled={loading}
                            className="px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-lg shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? '⏳ Loading...' : '🎬 Load Demo Scenario'}
                        </button>
                    </div>
                </div>

                {/* Step 1: Interactive Map */}
                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">Step 1: Select Area</h2>
                    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                        <h3 className="font-semibold text-gray-700 mb-3">🗺️ Interactive Map</h3>
                        <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
                            <p className="text-sm text-blue-800 font-medium mb-2">Instructions:</p>
                            <ul className="text-sm text-blue-700 space-y-1 ml-4 list-disc">
                                <li>🎯 Click the location button (top-left) to find your current position</li>
                                <li>🔍 Use the search box (top-right) to find any location</li>
                                <li>✏️ Use drawing tools (left sidebar) to draw your field area</li>
                                <li>The area will be automatically detected!</li>
                            </ul>
                        </div>
                        <div className="bg-gray-100 rounded-lg h-64 flex items-center justify-center border-2 border-dashed border-gray-300">
                            <p className="text-gray-500 text-sm">🗺️ Interactive map will be integrated here (Leaflet)</p>
                        </div>
                    </div>
                </div>

                {/* Step 2: Manual Coordinates */}
                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">
                        Step 2: Provide Area Coordinates (Optional)
                    </h2>
                    <p className="text-sm text-gray-600 mb-4">
                        If you drew on the map above, you can skip this and go directly to Step 3
                    </p>

                    <div className="bg-white rounded-lg border border-gray-200 p-6">
                        <h3 className="font-semibold text-gray-700 mb-4">📍 Manual Coordinates</h3>

                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Latitude
                                </label>
                                <input
                                    type="number"
                                    name="minLat"
                                    value={formData.minLat}
                                    onChange={handleInputChange}
                                    step="0.0001"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Longitude
                                </label>
                                <input
                                    type="number"
                                    name="minLon"
                                    value={formData.minLon}
                                    onChange={handleInputChange}
                                    step="0.0001"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                />
                            </div>
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Area (km²)
                            </label>
                            <input
                                type="number"
                                name="areaKm2"
                                value={formData.areaKm2}
                                onChange={handleInputChange}
                                step="0.1"
                                min="0.1"
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                            />
                        </div>
                    </div>
                </div>

                {/* Step 3: Run Analysis */}
                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">Step 3: Run Analysis</h2>

                    {error && (
                        <div className="mb-4 p-4 bg-red-50 border border-red-300 text-red-800 rounded-lg">
                            <p className="font-semibold">❌ Error</p>
                            <p className="text-sm mt-1">{error}</p>
                        </div>
                    )}

                    <button
                        onClick={handleRunAnalysis}
                        disabled={loading}
                        className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-lg shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed text-lg"
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Analyzing Satellite Data...
                            </span>
                        ) : (
                            '🚀 Run Analysis'
                        )}
                    </button>

                    {!credentials.clientId && (
                        <p className="text-sm text-orange-600 mt-3 text-center">
                            ⚠️ Please enter Sentinel Hub credentials in the sidebar to run analysis
                        </p>
                    )}
                </div>
            </div>
        </div>
    )
}
