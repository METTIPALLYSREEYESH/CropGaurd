# 🌾 CropGuard - Crop Health Monitoring System

**Satellite-based crop health assessment using Sentinel-2 imagery and NDVI analysis**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🚀 Features

- **📍 Interactive Map** - GPS location detection and global search
- **✏️ Drawing Tools** - Draw your field area directly on the map
- **🛰️ Real Satellite Data** - Sentinel-2 L2A imagery (10m resolution)
- **🧮 NDVI Analysis** - Automated vegetation index computation
- **📊 Health Classification** - 3-tier system (Healthy/Moderate/Unhealthy)
- **🗺️ Visual Results** - Interactive maps with color-coded overlays
- **📈 Statistics** - Detailed metrics and distribution charts

---

## 📋 Prerequisites

- Python 3.8 or higher
- Sentinel Hub account (free tier available)

---

## 🔧 Installation

### 1. Clone or Download

```bash
cd D:\Hack\N1\CropGuard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Sentinel Hub Credentials

1. Visit: https://www.sentinel-hub.com/
2. Create a free account
3. Go to: Dashboard → User Settings → OAuth clients
4. Click "Create new OAuth client"
5. Copy your **CLIENT_ID** and **CLIENT_SECRET**

---

## 🎯 Usage

### Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Workflow

1. **Enter Credentials**
   - Paste your Sentinel Hub Client ID and Secret in the sidebar

2. **Select Area** (Choose one method)
   - **Option A**: Click location button → Draw on map
   - **Option B**: Search for location → Enter area size
   - **Option C**: Manually enter coordinates

3. **Run Analysis**
   - Click "🚀 Analyze Crop Health" button
   - Wait 10-30 seconds for processing

4. **View Results**
   - Switch to "Results" tab
   - Explore charts, maps, and statistics

---

## 📊 How It Works

### 1. Data Acquisition
- Fetches Sentinel-2 L2A satellite imagery
- Last 30 days of data
- 10-meter spatial resolution
- Automatic cloud filtering

### 2. NDVI Computation
```
NDVI = (NIR - Red) / (NIR + Red)
```
- NIR: Near-Infrared band (B08)
- Red: Red band (B04)
- Temporal averaging for accuracy

### 3. Health Classification
- 🟢 **Healthy**: NDVI ≥ 0.5 (Dense vegetation)
- 🟡 **Moderate**: 0.2 ≤ NDVI < 0.5 (Sparse vegetation)
- 🔴 **Unhealthy**: NDVI < 0.2 (Bare soil/stressed crops)

---

## 🗂️ Project Structure

```
CropGuard/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file
├── utils/
│   ├── __init__.py
│   ├── satellite.py       # Sentinel Hub data fetching
│   ├── ndvi.py            # NDVI computation
│   └── visualization.py   # Map and chart generation
└── README.md              # This file
```

---

## 🎨 Screenshots

### Interactive Map
- GPS location detection
- Global location search
- Drawing tools (rectangle/polygon)
- Satellite/map layer toggle

### Results Dashboard
- NDVI histogram with thresholds
- Pie chart of health distribution
- Interactive result map with overlay
- Detailed statistics table

---

## 🌍 Example Locations

Try these coordinates for testing:

**Punjab, India (Wheat fields)**
- Lat: 30.9010, Lon: 75.8573, Area: 5 km²

**Iowa, USA (Corn belt)**
- Lat: 41.8780, Lon: -93.0977, Area: 10 km²

**Ukraine (Grain region)**
- Lat: 48.3794, Lon: 31.1656, Area: 8 km²

---

## ⚙️ Configuration

Edit `config.py` to customize:

- Default map location and zoom
- NDVI thresholds
- Time window (default: 30 days)
- Resolution (default: 10m)
- Health category colors

---

## 🐛 Troubleshooting

### "No data found"
- Check coordinates are correct
- Try different time period (area might be cloudy)
- Verify Sentinel Hub credentials

### "Authentication failed"
- Ensure CLIENT_ID and CLIENT_SECRET are correct
- Check Sentinel Hub account is active

### "Area too large"
- Keep area under 100 km² for best performance
- Larger areas take longer to process

### Map not loading
- Check internet connection
- Ensure all dependencies are installed
- Try refreshing the browser

---

## 📚 Technologies Used

- **Streamlit** - Web framework
- **Folium** - Interactive maps
- **sentinelhub** - Satellite data API
- **NumPy** - Numerical processing
- **Matplotlib** - Visualizations
- **Shapely** - Geometry processing
- **geopy** - Geocoding

---

## 🎓 Scientific Background

### NDVI (Normalized Difference Vegetation Index)
- Widely used vegetation index since 1970s
- Measures photosynthetic activity
- Range: -1 to +1
- Higher values = healthier vegetation

### Sentinel-2
- European Space Agency (ESA) satellite
- 10-meter resolution (best free data)
- 5-day revisit time
- 13 spectral bands
- Free and open data

---

## 🚀 Deployment Options

### Local
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit: https://streamlit.io/cloud
3. Connect repository
4. Deploy!

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 📈 Performance

- **Small field (1 km²)**: ~5-10 seconds
- **Medium field (10 km²)**: ~15-30 seconds
- **Large area (100 km²)**: ~2-5 minutes

*Times include data download (depends on internet speed)*

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Multi-temporal analysis (track changes over time)
- [ ] Additional vegetation indices (EVI, SAVI, NDWI)
- [ ] Export results (PDF reports, GeoTIFF)
- [ ] Mobile app version
- [ ] Machine learning integration
- [ ] Weather data overlay

---

## 📄 License

MIT License - Free for educational and research use

---

## 🙏 Acknowledgments

- **ESA Copernicus** - Sentinel-2 satellite data
- **Sentinel Hub** - Data access API
- **Streamlit** - Web framework
- **Folium** - Interactive maps

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Sentinel Hub documentation
3. Verify all dependencies are installed

---

## 🎯 Use Cases

- **Precision Agriculture** - Identify stress areas early
- **Crop Monitoring** - Track vegetation health over time
- **Yield Prediction** - Correlate NDVI with crop yields
- **Irrigation Planning** - Detect water stress
- **Research** - Analyze vegetation patterns

---

**🌾 CropGuard - Empowering farmers with satellite intelligence**

*Built with ❤️ for sustainable agriculture*
