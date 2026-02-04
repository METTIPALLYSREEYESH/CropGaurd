import { useNavigate } from 'react-router-dom'

export default function FarmerResults({ data }) {
    const navigate = useNavigate()

    if (!data) {
        return (
            <div className="h-full bg-gradient-to-b from-green-50 to-blue-50 flex items-center justify-center p-6">
                <div className="text-center">
                    <div className="text-8xl mb-6">🌾</div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-4">Check Your Field</h2>
                    <button
                        onClick={() => navigate('/')}
                        className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white text-xl font-bold rounded-xl shadow-lg transition"
                    >
                        ← Start Check
                    </button>
                </div>
            </div>
        )
    }

    const { ai_results } = data

    // Simplify status
    const getSimpleStatus = (riskLevel) => {
        if (riskLevel === 'High Risk') {
            return {
                icon: '🚨',
                text: 'URGENT',
                subtitle: 'Water Needed',
                color: 'bg-red-500',
                textColor: 'text-white',
                borderColor: 'border-red-600'
            }
        } else if (riskLevel === 'Medium Risk') {
            return {
                icon: '⚠️',
                text: 'WATCH',
                subtitle: 'Check Your Crops',
                color: 'bg-yellow-400',
                textColor: 'text-gray-900',
                borderColor: 'border-yellow-600'
            }
        } else {
            return {
                icon: '✅',
                text: 'GOOD',
                subtitle: 'Crops Are Healthy',
                color: 'bg-green-500',
                textColor: 'text-white',
                borderColor: 'border-green-600'
            }
        }
    }

    // Simplify actions
    const getSimpleActions = (riskLevel) => {
        if (riskLevel === 'High Risk') {
            return [
                '💧 Start watering TODAY',
                '⏰ Water for 2-3 hours',
                '👀 Check again tomorrow',
                '📞 Call if you need help'
            ]
        } else if (riskLevel === 'Medium Risk') {
            return [
                '🚶 Walk through your field',
                '👀 Look for yellow or brown spots',
                '💧 Water if soil is dry',
                '📅 Check again in 3 days'
            ]
        } else {
            return [
                '✅ Keep doing what you\'re doing',
                '🌾 Crops look good',
                '📅 Check again in 7 days',
                '😊 No action needed now'
            ]
        }
    }

    // Get weather info (simplified)
    const getWeatherInfo = () => {
        return {
            today: '☀️ Sunny & Hot',
            temp: '34°C',
            rain: 'No rain expected',
            advice: 'Very hot - crops need more water'
        }
    }

    const status = getSimpleStatus(ai_results.risk_level)
    const actions = getSimpleActions(ai_results.risk_level)
    const weather = getWeatherInfo()

    return (
        <div className="h-full bg-gradient-to-b from-green-50 to-blue-50 overflow-y-auto">
            {/* Header */}
            <div className="bg-white border-b-4 border-green-500 px-6 py-6 shadow-md">
                <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
                    <span className="text-4xl">🌾</span>
                    My Field Health
                </h1>
                <p className="text-lg text-gray-600 mt-2">Simple view for farmers</p>
            </div>

            {/* Content */}
            <div className="p-6 space-y-6 max-w-2xl mx-auto">

                {/* Status Card - LARGE */}
                <div className={`${status.color} ${status.textColor} rounded-3xl shadow-2xl p-8 border-4 ${status.borderColor} transform hover:scale-105 transition`}>
                    <div className="text-center">
                        <div className="text-9xl mb-4">{status.icon}</div>
                        <h2 className="text-5xl font-black mb-3">{status.text}</h2>
                        <p className="text-3xl font-bold opacity-90">{status.subtitle}</p>
                        {ai_results.risk_level === 'High Risk' && (
                            <p className="text-xl mt-4 opacity-80">Your crops are suffering!</p>
                        )}
                    </div>
                </div>

                {/* What To Do Card */}
                <div className="bg-white rounded-3xl shadow-xl p-8 border-4 border-blue-400">
                    <h3 className="text-3xl font-bold text-blue-700 mb-6 flex items-center gap-3">
                        <span className="text-4xl">💧</span>
                        What To Do
                    </h3>
                    <ul className="space-y-4">
                        {actions.map((action, index) => (
                            <li key={index} className="flex items-start gap-4 text-xl text-gray-800">
                                <span className="text-2xl flex-shrink-0">✓</span>
                                <span className="font-medium leading-relaxed">{action}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Weather Card */}
                <div className="bg-white rounded-3xl shadow-xl p-8 border-4 border-yellow-400">
                    <h3 className="text-3xl font-bold text-yellow-700 mb-6 flex items-center gap-3">
                        <span className="text-4xl">☀️</span>
                        Weather
                    </h3>
                    <div className="space-y-4 text-xl text-gray-800">
                        <div className="flex justify-between items-center">
                            <span className="font-semibold">Today:</span>
                            <span className="text-2xl">{weather.today}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="font-semibold">Temperature:</span>
                            <span className="text-2xl font-bold text-red-600">{weather.temp}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="font-semibold">Rain:</span>
                            <span className="text-2xl">{weather.rain}</span>
                        </div>
                        {ai_results.risk_level === 'High Risk' && (
                            <div className="mt-4 p-4 bg-red-50 rounded-xl border-2 border-red-200">
                                <p className="text-lg font-semibold text-red-700">⚠️ {weather.advice}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Crop Info */}
                <div className="bg-white rounded-3xl shadow-xl p-8 border-4 border-green-400">
                    <h3 className="text-3xl font-bold text-green-700 mb-6 flex items-center gap-3">
                        <span className="text-4xl">🌾</span>
                        Your Crop
                    </h3>
                    <div className="text-center">
                        <p className="text-2xl text-gray-700 mb-2">Crop Type:</p>
                        <p className="text-4xl font-bold text-green-600">{ai_results.detected_crop}</p>
                    </div>
                </div>

                {/* Check Again Button */}
                <button
                    onClick={() => navigate('/')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white text-3xl font-black py-8 rounded-3xl shadow-2xl transition transform hover:scale-105"
                >
                    🔄 Check My Field Again
                </button>

                {/* Help Section */}
                <div className="bg-blue-50 rounded-3xl p-6 border-2 border-blue-200">
                    <p className="text-center text-lg text-blue-800">
                        <span className="font-bold">Need Help?</span><br />
                        Call your local agriculture office<br />
                        or ask a neighbor farmer
                    </p>
                </div>

                {/* Switch to Technical View */}
                <div className="text-center pt-4">
                    <p className="text-sm text-gray-600 mb-2">Want more details?</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="text-blue-600 hover:text-blue-700 underline text-base font-semibold"
                    >
                        Switch to Technical View
                    </button>
                </div>
            </div>
        </div>
    )
}
