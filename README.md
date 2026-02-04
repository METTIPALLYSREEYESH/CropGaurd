# 🌾 CropGuard - AI-Powered Crop Health Monitoring

<div align="center">

![CropGuard Banner](https://img.shields.io/badge/CropGuard-AI%20Crop%20Monitoring-green?style=for-the-badge&logo=leaf)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Revolutionizing Agriculture with Satellite AI** 🛰️🌱

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## 🌟 Overview

**CropGuard** is an intelligent crop health monitoring system that leverages **Sentinel-2 satellite imagery** and **AI-powered analysis** to help farmers make data-driven decisions. With support for **3 languages** (English, Hindi, Telugu) and a **farmer-friendly mode**, CropGuard makes advanced agricultural technology accessible to everyone.

### 🎯 Key Highlights

- 🛰️ **Real-time Satellite Data** - Live Sentinel-2 imagery analysis
- 🤖 **AI Risk Assessment** - Intelligent crop health scoring (0-100)
- 🌤️ **Live Weather Integration** - Real-time weather from Open-Meteo API
- 🌱 **Smart Crop Recommendations** - 10 crops analyzed based on weather, soil & location
- 👨‍🌾 **Farmer-Friendly Mode** - Simple language with Hindi/Telugu support
- 📊 **Interactive Maps** - NDVI visualization with time comparison
- 📄 **PDF Reports** - Downloadable field analysis reports

---

## ✨ Features

### 🔍 **Advanced Crop Monitoring**

<table>
<tr>
<td width="50%">

#### 🛰️ Satellite Analysis
- **NDVI Calculation** from Sentinel-2
- **Cloud-free** image selection
- **Time-series comparison** (Before vs Now)
- **Health classification** (Healthy/Moderate/Unhealthy)

</td>
<td width="50%">

#### 🤖 AI-Powered Insights
- **Risk Level Detection** (High/Medium/Stable)
- **AI Health Score** (0-100 scale)
- **Confidence Rating** with visual indicators
- **Actionable Recommendations**

</td>
</tr>
</table>

### 🌍 **Real-World Data Integration**

| Feature | Description | API |
|---------|-------------|-----|
| 🌤️ **Weather** | Temperature, Rain, Wind, Humidity | Open-Meteo (Free) |
| 🌱 **Crop Detection** | AI-based crop type identification | Custom ML Model |
| 📍 **Location** | GPS, Search, or Manual coordinates | Nominatim |

### 🌾 **Crop Recommendation System**

**10 Crops Analyzed:**
- 🌾 Rice (धान / వరి)
- 🌾 Wheat (गेहूं / గోధుమ)
- ☁️ Cotton (कपास / పత్తి)
- 🎋 Sugarcane (गन्ना / చెరకు)
- 🌽 Maize (मक्का / మొక్కజొన్న)
- 🫘 Soybean (सोयाबीन / సోయాబీన్)
- 🥜 Groundnut (मूंगफली / వేరుశెనగ)
- 🫘 Chickpea (चना / శనగలు)
- 🍅 Tomato (टमाटर / టమోటా)
- 🧅 Onion (प्याज / ఉల్లిపాయ)

**Scoring Algorithm:**
- ✅ Temperature suitability (40 points)
- 💧 Water availability (25 points)
- 🌱 Soil health from NDVI (20 points)
- 📍 Region compatibility (10 points)
- 📅 Season alignment (5 points)

### 👨‍🌾 **Farmer-Friendly Mode**

<table>
<tr>
<td width="50%">

**Simple Language**
- No technical jargon
- Relatable comparisons
- "Crops thirsty like person in summer"
- Visual status indicators

</td>
<td width="50%">

**Multilingual Support**
- 🇬🇧 English
- 🇮🇳 Hindi (हिंदी)
- 🇮🇳 Telugu (తెలుగు)
- Auto-translates all content

</td>
</tr>
</table>

---

## 🚀 Demo

### Quick Start with Demo Mode

1. Click **"🎬 Load Demo Scenario"** in sidebar
2. Go to **"📊 Analysis Results"** tab
3. Toggle **"👨‍🌾 Farmer-Friendly Mode"** to see simplified view

### Real Analysis

1. Get free Sentinel Hub credentials: [sentinel-hub.com](https://www.sentinel-hub.com/)
2. Enter Client ID & Secret in sidebar
3. Choose location (GPS/Search/Coordinates)
4. Click **"🚀 Run Analysis"**

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Sentinel Hub account (free tier available)

### Setup

```bash
# Clone repository
git clone https://github.com/vardhan4161/CropGaurd.git
cd CropGaurd

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Environment Variables (Optional)

Create `.env` file:
```env
SENTINEL_CLIENT_ID=your_client_id
SENTINEL_CLIENT_SECRET=your_client_secret
```

---

## 💻 Usage

### 1. **Select Field Area**

Three methods to choose your field:

```python
# Method 1: GPS Location
Click "📍 Use My Location" button

# Method 2: Search
Search for "Village Name, State, India"

# Method 3: Manual Coordinates
Latitude: 17.39
Longitude: 78.491
Area: 1.0 km²
```

### 2. **Run Analysis**

```bash
# Enter Sentinel Hub credentials
Client ID: your_client_id
Client Secret: your_client_secret

# Click "🚀 Run Analysis"
# Wait 30-60 seconds for satellite data processing
```

### 3. **View Results**

**Technical Mode:**
- AI Health Score (0-100)
- Risk Level with explanation
- Weather Conditions (4 metrics)
- Crop Recommendations (Top 5)
- Interactive NDVI maps
- PDF Report download

**Farmer Mode:**
- 😰/😐/😊 Visual status
- Simple action steps
- Weather in farmer's terms
- Top 3 crop suggestions
- Local language support

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Interactive web UI
- **Folium** - Interactive maps
- **Plotly** - Data visualization

### Backend
- **Python 3.11** - Core language
- **NumPy** - NDVI calculations
- **Sentinel Hub API** - Satellite imagery
- **Open-Meteo API** - Weather data (FREE!)

### AI/ML
- Custom risk assessment model
- Crop detection algorithm
- Multi-factor recommendation engine

### Data Sources
- 🛰️ **Sentinel-2** - 10m resolution satellite imagery
- 🌤️ **Open-Meteo** - Real-time weather data
- 📍 **Nominatim** - Location geocoding

---

## 📊 Project Structure

```
CropGuard/
├── app.py                          # Main Streamlit application
├── utils/
│   ├── satellite.py                # Sentinel Hub integration
│   ├── ndvi.py                     # NDVI calculation
│   ├── ai_risk_model.py            # AI risk assessment
│   ├── crop_detection.py           # Crop type detection
│   ├── crop_recommendation.py      # Crop suggestion engine
│   ├── weather.py                  # Weather API integration
│   ├── farmer_mode.py              # Farmer-friendly helpers
│   ├── translations.py             # Multilingual support
│   ├── visualization.py            # Map & chart generation
│   ├── report_generator.py         # PDF report creation
│   ├── persistence.py              # Data storage
│   └── field_manager.py            # Saved fields management
├── data/
│   └── demo_scenario.json          # Demo data
├── config.py                       # Configuration settings
└── requirements.txt                # Python dependencies
```

---

## 🌈 Features in Detail

### 🎨 Farmer-Friendly Mode

**Visual Status Cards:**
```
😰 URGENT - Crops Need Water
🌾➡️💀 (Crop dying visual)
"Your crops are thirsty, like a person needs water in summer heat"
```

**Simple Actions:**
```
💧 Start watering TODAY
   Like giving water to thirsty person
   
⏰ Water for 2-3 hours
   Morning or evening time
   
👀 Check again tomorrow
   Visit field in morning
```

**Weather in Farmer's Terms:**
```
☀️ Hot          🌧️ Rain        💨 Wind
28°C            7 days ago      12 km/h
warm            No rain         light
```

### 📈 AI Risk Assessment

**Scoring Factors:**
1. NDVI Change (-1 to +1)
2. Absolute NDVI value
3. Weather context
4. Historical comparison
5. Confidence level

**Risk Levels:**
- 🔴 **High Risk** (Score < 50) - Immediate action needed
- 🟠 **Medium Risk** (50-79) - Monitor closely
- 🟢 **Stable** (80-100) - Maintain current care

### 🗺️ Interactive Maps

**Features:**
- Toggle Map/Satellite view
- NDVI overlay with color gradient
- Health classification zones
- Time comparison mode
- Zoom & pan controls

---

## 🔧 Configuration

### Sentinel Hub Setup

1. Sign up at [sentinel-hub.com](https://www.sentinel-hub.com/)
2. Create OAuth client
3. Copy Client ID & Secret
4. Enter in CropGuard sidebar

### Customization

Edit `config.py`:
```python
# NDVI Thresholds
NDVI_UNHEALTHY = 0.2
NDVI_MODERATE = 0.5

# Time Window
TIME_WINDOW_DAYS = 30

# Resolution
RESOLUTION = 10  # meters per pixel
```

---

## 📝 API Credits

- **Sentinel Hub** - Satellite imagery (Free tier: 30,000 processing units/month)
- **Open-Meteo** - Weather data (Completely free, no API key needed!)
- **Nominatim** - Geocoding (Free, rate-limited)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Sentinel Hub** for satellite imagery API
- **Open-Meteo** for free weather data
- **Streamlit** for the amazing framework
- **Indian farmers** for inspiration and feedback

---

## 📧 Contact

**Project Maintainer:** Vardhan Goud

- GitHub: [@vardhan4161](https://github.com/vardhan4161)
- Email: vardhangoud096@gmail.com

---

<div align="center">

**Made with ❤️ for Indian Farmers** 🇮🇳

**Star ⭐ this repo if you find it helpful!**

</div>
