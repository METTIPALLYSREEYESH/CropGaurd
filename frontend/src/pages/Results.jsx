import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { generatePDFReport } from '../services/api'
import FarmerResults from '../components/FarmerResults'

export default function Results({ data, language, farmerMode }) {
    const navigate = useNavigate()
    const [downloading, setDownloading] = useState(false)

    // Show farmer-friendly version if farmer mode is enabled
    if (farmerMode) {
        return <FarmerResults data={data} />
    }

    if (!data) {
        return (
            <div className="h-full bg-white flex items-center justify-center">
                <div className="text-center p-12">
                    <div className="text-6xl mb-4">📊</div>
                    <h2 className="text-2xl font-semibold text-gray-700 mb-2">No Analysis Results Yet</h2>
                    <p className="text-gray-600 mb-6">
                        Please run an analysis or load demo scenario first
                    </p>
                    <button
                        onClick={() => navigate('/')}
                        className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition"
                    >
                        ← Go to Select Area
                    </button>
                </div>
            </div>
        )
    }

    const { ai_results, classification, bbox_info, ndvi_map } = data

    const getRiskColor = (riskLevel) => {
        if (riskLevel === 'High Risk') return 'bg-red-500'
        if (riskLevel === 'Medium Risk') return 'bg-orange-500'
        return 'bg-green-500'
    }

    const getRiskBorderColor = (riskLevel) => {
        if (riskLevel === 'High Risk') return 'border-red-500'
        if (riskLevel === 'Medium Risk') return 'border-orange-500'
        return 'border-green-500'
    }

    const getConfidenceColor = (confidence) => {
        if (confidence === 'High') return 'text-green-700 bg-green-100 border-green-300'
        if (confidence === 'Medium') return 'text-orange-700 bg-orange-100 border-orange-300'
        return 'text-red-700 bg-red-100 border-red-300'
    }

    const getScoreColor = (score) => {
        if (score > 70) return '#10b981' // green
        if (score > 40) return '#f59e0b' // orange
        return '#ef4444' // red
    }

    const handleDownloadPDF = async () => {
        setDownloading(true)
        try {
            await generatePDFReport(
                ai_results,
                bbox_info,
                classification,
                ndvi_map,
                ai_results.detected_crop,
                language
            )
        } catch (err) {
            console.error('PDF generation failed:', err)
            alert('Failed to generate PDF: ' + err.message)
        } finally {
            setDownloading(false)
        }
    }

    const circumference = 2 * Math.PI * 70
    const scoreOffset = circumference - (ai_results.ai_score / 100) * circumference

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
                        onClick={() => navigate('/')}
                        className="px-6 py-3 font-medium border-b-2 border-transparent text-gray-600 hover:text-gray-800 transition"
                    >
                        📍 Select Area
                    </button>
                    <button
                        className="px-6 py-3 font-medium border-b-2 border-red-500 text-red-600"
                    >
                        📊 Analysis Results
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="px-8 py-6 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>

                {/* Risk Alert Card */}
                <div className={`${getRiskColor(ai_results.risk_level)} text-white rounded-lg shadow-xl p-8 mb-6 border-4 ${getRiskBorderColor(ai_results.risk_level)}`}>
                    <div className="flex justify-between items-start mb-6">
                        <div>
                            <h2 className="text-3xl font-bold mb-2">
                                {ai_results.risk_level === 'High Risk' && '🚨 '}
                                {ai_results.risk_level === 'Medium Risk' && '⚠️ '}
                                {ai_results.risk_level === 'Low Risk' && '✅ '}
                                {ai_results.risk_level.toUpperCase()}
                            </h2>
                            <p className="text-lg opacity-90">Field Health Assessment</p>
                        </div>
                        <div className="bg-white bg-opacity-20 backdrop-blur-sm px-6 py-3 rounded-lg">
                            <div className="text-sm opacity-90">Detected Crop</div>
                            <div className="text-2xl font-bold">🌾 {ai_results.detected_crop}</div>
                            <div className="text-xs opacity-75">{ai_results.crop_confidence} Confidence</div>
                        </div>
                    </div>

                    <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-6 mb-4">
                        <h3 className="font-semibold text-lg mb-3">🤖 AI Analysis</h3>
                        <p className="text-base leading-relaxed">
                            {ai_results.risk_explanation}
                        </p>
                    </div>

                    <div className="bg-white text-gray-800 rounded-lg p-6 shadow-lg">
                        <h3 className="font-semibold text-lg mb-3 text-green-700">🚜 Recommended Action</h3>
                        <p className="text-base leading-relaxed">
                            {ai_results.action_recommendation}
                        </p>
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                        <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded px-4 py-2">
                            <span className="opacity-75">NDVI Change:</span>
                            <span className="font-bold ml-2">{ai_results.ndvi_change.toFixed(3)}</span>
                        </div>
                        <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded px-4 py-2">
                            <span className="opacity-75">Location:</span>
                            <span className="font-bold ml-2">{bbox_info.center_lat.toFixed(4)}°, {bbox_info.center_lon.toFixed(4)}°</span>
                        </div>
                    </div>
                </div>

                {/* AI Health Score - Circular Gauge */}
                <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8 mb-6">
                    <h3 className="text-2xl font-semibold mb-6 text-center text-gray-800">🧠 AI Health Score</h3>
                    <div className="flex flex-col items-center">
                        {/* Circular Progress */}
                        <div className="relative w-48 h-48 mb-4">
                            <svg className="w-full h-full transform -rotate-90">
                                {/* Background circle */}
                                <circle
                                    cx="96"
                                    cy="96"
                                    r="70"
                                    stroke="#e5e7eb"
                                    strokeWidth="16"
                                    fill="none"
                                />
                                {/* Progress circle */}
                                <circle
                                    cx="96"
                                    cy="96"
                                    r="70"
                                    stroke={getScoreColor(ai_results.ai_score)}
                                    strokeWidth="16"
                                    fill="none"
                                    strokeDasharray={circumference}
                                    strokeDashoffset={scoreOffset}
                                    strokeLinecap="round"
                                    className="transition-all duration-1000"
                                />
                            </svg>
                            {/* Score text */}
                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <span className="text-5xl font-bold" style={{ color: getScoreColor(ai_results.ai_score) }}>
                                    {ai_results.ai_score}
                                </span>
                                <span className="text-2xl text-gray-500">/100</span>
                            </div>
                        </div>

                        {/* Confidence Badge */}
                        <div className={`px-6 py-3 rounded-full font-semibold border-2 ${getConfidenceColor(ai_results.confidence)}`}>
                            🎯 Confidence: {ai_results.confidence} {ai_results.confidence === 'High' ? '✓' : ai_results.confidence === 'Medium' ? '~' : '!'}
                        </div>

                        {/* Score interpretation */}
                        <div className="mt-6 text-center max-w-md">
                            <p className="text-sm text-gray-600">
                                {ai_results.ai_score > 70 && '✅ Excellent crop health. Continue current practices.'}
                                {ai_results.ai_score > 40 && ai_results.ai_score <= 70 && '⚠️ Moderate health. Monitor closely and consider intervention.'}
                                {ai_results.ai_score <= 40 && '🚨 Poor health. Immediate action recommended.'}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Health Distribution */}
                <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8 mb-6">
                    <h3 className="text-2xl font-semibold mb-6 text-gray-800">📊 Health Distribution</h3>
                    <div className="grid grid-cols-3 gap-6">
                        <div className="text-center p-6 bg-green-50 rounded-lg border-2 border-green-200">
                            <div className="text-5xl mb-3">🟢</div>
                            <div className="font-semibold text-lg text-gray-700 mb-2">Healthy</div>
                            <div className="text-4xl font-bold text-green-600 mb-2">
                                {classification.healthy.percentage.toFixed(1)}%
                            </div>
                            <div className="text-sm text-gray-600">
                                {classification.healthy.count.toLocaleString()} pixels
                            </div>
                            <div className="mt-3 text-xs text-gray-500">
                                NDVI ≥ 0.6
                            </div>
                        </div>
                        <div className="text-center p-6 bg-yellow-50 rounded-lg border-2 border-yellow-200">
                            <div className="text-5xl mb-3">🟡</div>
                            <div className="font-semibold text-lg text-gray-700 mb-2">Moderate</div>
                            <div className="text-4xl font-bold text-yellow-600 mb-2">
                                {classification.moderate.percentage.toFixed(1)}%
                            </div>
                            <div className="text-sm text-gray-600">
                                {classification.moderate.count.toLocaleString()} pixels
                            </div>
                            <div className="mt-3 text-xs text-gray-500">
                                0.4 ≤ NDVI &lt; 0.6
                            </div>
                        </div>
                        <div className="text-center p-6 bg-red-50 rounded-lg border-2 border-red-200">
                            <div className="text-5xl mb-3">🔴</div>
                            <div className="font-semibold text-lg text-gray-700 mb-2">Unhealthy</div>
                            <div className="text-4xl font-bold text-red-600 mb-2">
                                {classification.unhealthy.percentage.toFixed(1)}%
                            </div>
                            <div className="text-sm text-gray-600">
                                {classification.unhealthy.count.toLocaleString()} pixels
                            </div>
                            <div className="mt-3 text-xs text-gray-500">
                                NDVI &lt; 0.4
                            </div>
                        </div>
                    </div>

                    {/* Statistics */}
                    <div className="mt-6 grid grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
                        <div className="text-center">
                            <div className="text-xs text-gray-600 mb-1">Mean NDVI</div>
                            <div className="font-bold text-gray-800">{classification.statistics.mean.toFixed(3)}</div>
                        </div>
                        <div className="text-center">
                            <div className="text-xs text-gray-600 mb-1">Std Dev</div>
                            <div className="font-bold text-gray-800">{classification.statistics.std.toFixed(3)}</div>
                        </div>
                        <div className="text-center">
                            <div className="text-xs text-gray-600 mb-1">Min</div>
                            <div className="font-bold text-gray-800">{classification.statistics.min.toFixed(3)}</div>
                        </div>
                        <div className="text-center">
                            <div className="text-xs text-gray-600 mb-1">Max</div>
                            <div className="font-bold text-gray-800">{classification.statistics.max.toFixed(3)}</div>
                        </div>
                    </div>
                </div>

                {/* PDF Download */}
                <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
                    <h3 className="text-xl font-semibold mb-4 text-gray-800">📄 Export Report</h3>
                    <button
                        onClick={handleDownloadPDF}
                        disabled={downloading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-lg shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {downloading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Generating PDF...
                            </span>
                        ) : (
                            '📄 Download Field Report (PDF)'
                        )}
                    </button>
                    <p className="text-xs text-gray-600 mt-2 text-center">
                        Comprehensive report with all analysis results and recommendations
                    </p>
                </div>

                {/* Why This Matters */}
                <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg shadow-md border border-green-200 p-8">
                    <h3 className="text-2xl font-semibold mb-6 text-gray-800">💡 Why This Matters</h3>
                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="bg-white rounded-lg p-5 shadow-sm">
                            <h4 className="font-semibold text-lg mb-3 text-green-700">🌱 Early Detection</h4>
                            <p className="text-gray-700 text-sm leading-relaxed">
                                Catch crop stress before visible damage occurs. Satellite data reveals health issues 7-14 days earlier than the human eye.
                            </p>
                        </div>
                        <div className="bg-white rounded-lg p-5 shadow-sm">
                            <h4 className="font-semibold text-lg mb-3 text-blue-700">🛰️ Zero Hardware</h4>
                            <p className="text-gray-700 text-sm leading-relaxed">
                                No expensive IoT sensors needed. Works anywhere with satellite coverage - 100% satellite-based monitoring.
                            </p>
                        </div>
                        <div className="bg-white rounded-lg p-5 shadow-sm">
                            <h4 className="font-semibold text-lg mb-3 text-purple-700">🌍 Global Scale</h4>
                            <p className="text-gray-700 text-sm leading-relaxed">
                                Monitor from 1 acre to 1 million acres instantly. Perfect for small farmers and large agricultural operations.
                            </p>
                        </div>
                        <div className="bg-white rounded-lg p-5 shadow-sm">
                            <h4 className="font-semibold text-lg mb-3 text-orange-700">👨‍🌾 Farmer First</h4>
                            <p className="text-gray-700 text-sm leading-relaxed">
                                Simple, actionable advice (e.g., "Irrigate now"). No PhD required to understand crop health status.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
