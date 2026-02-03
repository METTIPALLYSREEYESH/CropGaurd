# 🚀 CropGuard - Quick Start Guide

## ✅ Installation Complete!

All dependencies are installed. You're ready to run the application!

---

## 🎯 Run the Application

### Option 1: Using Batch Script (Easiest)
```bash
cd D:\Hack\N1\CropGuard
run.bat
```

### Option 2: Using Command Line
```bash
cd D:\Hack\N1\CropGuard
streamlit run app.py
```

The app will open automatically in your browser at: **http://localhost:8501**

---

## 📋 Before First Use

### Get Sentinel Hub Credentials (Free - Takes 2 minutes)

1. Visit: **https://www.sentinel-hub.com/**
2. Click "Sign Up" (top-right)
3. Create free account
4. After login, go to: **Dashboard → User Settings → OAuth clients**
5. Click "**+ Create new OAuth client**"
6. Give it a name (e.g., "CropGuard")
7. Copy your **CLIENT_ID** and **CLIENT_SECRET**

---

## 🗺️ Using the Application

### Step 1: Enter Credentials
- Open the **sidebar** (left side)
- Paste your **Client ID**
- Paste your **Client Secret**

### Step 2: Select Your Area

**Three ways to do this:**

#### Method A: Interactive Map (Recommended)
1. Click the **location button** (📍 top-left) to find your position
2. Or use **search box** (🔍 top-right) to find any location
3. Use **drawing tools** (left sidebar) to draw your field
   - Click Rectangle tool
   - Draw on the map
   - Click Export button
4. Copy the GeoJSON
5. Paste in the text area
6. Click "Use Drawn Area"

#### Method B: Search Location
1. Select "🔍 Search Location" option
2. Type location: "Punjab, India" or "30.9010, 75.8573"
3. Enter area size (km²)
4. Click "Search & Confirm"

#### Method C: Manual Coordinates
1. Select "📍 Manual Coordinates" option
2. Enter Latitude (e.g., 30.9010)
3. Enter Longitude (e.g., 75.8573)
4. Enter Area (e.g., 5 km²)
5. Click "Confirm Coordinates"

### Step 3: Analyze
1. Click the big green button: **"🚀 Analyze Crop Health"**
2. Wait 10-30 seconds (progress bar shows status)
3. Switch to **"Results"** tab

### Step 4: View Results
- See health metrics at the top
- View NDVI histogram and pie chart
- Explore interactive result map
- Check detailed statistics

---

## 🌍 Test Locations

Try these for your first analysis:

**Punjab, India (Wheat)**
- Lat: `30.9010`, Lon: `75.8573`, Area: `5 km²`

**Iowa, USA (Corn)**
- Lat: `41.8780`, Lon: `-93.0977`, Area: `10 km²`

**Ukraine (Grain)**
- Lat: `48.3794`, Lon: `31.1656`, Area: `8 km²`

---

## 🎨 Map Features

### Buttons You'll See:

- **📍 Location** (top-left) - Find your GPS position
- **🔍 Search** (top-right) - Search any location
- **✏️ Rectangle** (left) - Draw rectangular area
- **✏️ Polygon** (left) - Draw custom shape
- **✏️ Edit** (left) - Modify drawn area
- **🗑️ Delete** (left) - Remove drawn area
- **💾 Export** (left) - Get GeoJSON data
- **⛶ Fullscreen** (top-right) - Expand map
- **🗺️ Layers** (top-right) - Toggle Map/Satellite

---

## 📊 Understanding Results

### Health Categories

🟢 **Healthy (NDVI ≥ 0.5)**
- Dense, vigorous vegetation
- Good crop health
- Optimal photosynthesis

🟡 **Moderate (0.2 ≤ NDVI < 0.5)**
- Sparse vegetation
- May need attention
- Monitor closely

🔴 **Unhealthy (NDVI < 0.2)**
- Bare soil or stressed crops
- Immediate action needed
- Check for pests, drought, nutrients

### NDVI Scale
- **-1 to 0**: Water, bare soil
- **0 to 0.2**: Sparse vegetation, stressed crops
- **0.2 to 0.5**: Moderate vegetation
- **0.5 to 1**: Dense, healthy vegetation

---

## ⚠️ Troubleshooting

### "Authentication failed"
→ Check your CLIENT_ID and CLIENT_SECRET are correct
→ Make sure you copied them completely

### "No data found"
→ Area might be 100% cloudy for last 30 days
→ Try a different location or time period

### "Map not loading"
→ Check internet connection
→ Refresh the browser page
→ Try a different browser

### "Analysis taking too long"
→ Large areas (>50 km²) take more time
→ Check internet speed
→ Try smaller area first

---

## 💡 Tips for Best Results

1. **Start Small**: Try 5-10 km² first
2. **Check Weather**: Avoid areas with constant cloud cover
3. **Agricultural Areas**: Works best on farmland
4. **Growing Season**: Results are clearer during growing season
5. **Compare Dates**: Run analysis multiple times to track changes

---

## 🎓 For Presentations/Demos

### Demo Flow (5 minutes)
1. **Show UI** (30 sec) - Clean interface
2. **Search Location** (30 sec) - Type "Punjab, India"
3. **Draw Area** (1 min) - Use rectangle tool
4. **Run Analysis** (2 min) - Live processing
5. **Show Results** (1 min) - Charts and map

### Key Points to Mention
- ✅ Real Sentinel-2 satellite data (10m resolution)
- ✅ Works anywhere in the world
- ✅ Free and open-source
- ✅ Automatic cloud filtering
- ✅ Interactive map with GPS

---

## 📁 Project Files

```
CropGuard/
├── app.py              ← Main application
├── config.py           ← Settings
├── requirements.txt    ← Dependencies
├── run.bat            ← Quick start
├── README.md          ← Full documentation
└── utils/
    ├── satellite.py   ← Data fetching
    ├── ndvi.py        ← NDVI computation
    └── visualization.py ← Maps & charts
```

---

## 🚀 Next Steps

1. **Run the app**: `streamlit run app.py`
2. **Get credentials**: sentinel-hub.com
3. **Test with sample location**: Punjab, India
4. **Explore features**: GPS, search, drawing
5. **Analyze your own field**: Use real coordinates

---

## 📞 Need Help?

1. Check **README.md** for detailed documentation
2. Review **walkthrough.md** for complete guide
3. Verify all dependencies are installed
4. Check Sentinel Hub account is active

---

**🎉 You're all set! Run the app and start monitoring crops!**

```bash
streamlit run app.py
```

**Happy Farming! 🌾**
