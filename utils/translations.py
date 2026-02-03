"""
Multilingual Support for CropGuard
Translations for English, Hindi, and Telugu
"""

TRANSLATIONS = {
    'en': {
        # App Title & Headers
        'app_title': '🌾 CropGuard - Crop Health Monitoring',
        'app_subtitle': 'Automated crop health assessment using Sentinel-2 satellite imagery',
        'select_area_tab': 'Select Area',
        'results_tab': 'Analysis Results',
        
        # Sidebar
        'sidebar_title': '📍 Field Selection',
        'location_method': 'Location Input Method',
        'manual_coords': 'Manual Coordinates',
        'search_location': 'Search Location',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'area_size': 'Field Area (km²)',
        'run_analysis': '🚀 Run Analysis',
        'language_selector': 'Language / भाषा / భాష',
        
        # Risk Levels
        'high_risk': 'HIGH RISK',
        'medium_risk': 'MEDIUM RISK',
        'stable': 'STABLE',
        
        # AI Analysis
        'ai_analysis': '🤖 AI Analysis:',
        'action': '🚜 Action:',
        'ndvi_change': '📉 NDVI Change:',
        'ai_health_score': '🧠 AI Health Score',
        'detected_crop': 'Detected Crop',
        
        # Recommendations
        'high_risk_action': '🚨 **URGENT**: Increase irrigation immediately and inspect field for pest/disease outbreaks.',
        'medium_risk_action': '👀 **Advice**: Monitor soil moisture closely and check for early signs of yellowing.',
        'stable_action': '✅ **Advice**: Maintain current care schedule. No immediate action required.',
        
        # Explanations
        'high_risk_explanation': '⚠️ Significant vegetation decline detected. Potential causes include severe water stress, pest infestation, or disease outbreak. Immediate inspection recommended.',
        'medium_risk_explanation': '⚠️ Early signs of stress detected. Vegetation vigor is slightly lower than previous weeks. Monitor soil moisture and check for early pest signs.',
        'stable_explanation': '✅ Crop condition is stable or improving. No significant stress anomalies detected compared to the previous period.',
        
        # Maps & Visualizations
        'interactive_maps': '🗺️ Interactive Analysis Maps',
        'select_map_view': 'Select Map View:',
        'recent_analysis': 'Recent Analysis (Current Health)',
        'time_comparison': 'Time Comparison (Before vs Now)',
        'toggle_map_view': 'Toggle between Map/Satellite view to see the NDVI overlay',
        
        # PDF Report
        'download_report': '📄 Download Field Report (PDF)',
        'generating_report': 'Generating report...',
        
        # Messages
        'analysis_complete': '✅ Analysis complete! Check the **Results** tab.',
        'no_analysis': '👈 Please complete the analysis in the **Select Area** tab first.',
    },
    
    'hi': {
        # App Title & Headers
        'app_title': '🌾 क्रॉपगार्ड - फसल स्वास्थ्य निगरानी',
        'app_subtitle': 'सेंटिनल-2 उपग्रह इमेजरी का उपयोग करके स्वचालित फसल स्वास्थ्य मूल्यांकन',
        'select_area_tab': 'क्षेत्र चुनें',
        'results_tab': 'विश्लेषण परिणाम',
        
        # Sidebar
        'sidebar_title': '📍 खेत चयन',
        'location_method': 'स्थान इनपुट विधि',
        'manual_coords': 'मैनुअल निर्देशांक',
        'search_location': 'स्थान खोजें',
        'latitude': 'अक्षांश',
        'longitude': 'देशांतर',
        'area_size': 'खेत का क्षेत्रफल (km²)',
        'run_analysis': '🚀 विश्लेषण चलाएं',
        'language_selector': 'Language / भाषा / భాష',
        
        # Risk Levels
        'high_risk': 'उच्च जोखिम',
        'medium_risk': 'मध्यम जोखिम',
        'stable': 'स्थिर',
        
        # AI Analysis
        'ai_analysis': '🤖 AI विश्लेषण:',
        'action': '🚜 कार्रवाई:',
        'ndvi_change': '📉 NDVI परिवर्तन:',
        'ai_health_score': '🧠 AI स्वास्थ्य स्कोर',
        'detected_crop': 'पहचानी गई फसल',
        
        # Recommendations
        'high_risk_action': '🚨 **तत्काल**: तुरंत सिंचाई बढ़ाएं और कीट/रोग के प्रकोप के लिए खेत का निरीक्षण करें।',
        'medium_risk_action': '👀 **सलाह**: मिट्टी की नमी की बारीकी से निगरानी करें और पीलेपन के शुरुआती संकेतों की जांच करें।',
        'stable_action': '✅ **सलाह**: वर्तमान देखभाल कार्यक्रम बनाए रखें। कोई तत्काल कार्रवाई की आवश्यकता नहीं।',
        
        # Explanations
        'high_risk_explanation': '⚠️ महत्वपूर्ण वनस्पति गिरावट का पता चला। संभावित कारणों में गंभीर जल तनाव, कीट संक्रमण, या रोग का प्रकोप शामिल हैं। तत्काल निरीक्षण की सिफारिश की जाती है।',
        'medium_risk_explanation': '⚠️ तनाव के शुरुआती संकेत का पता चला। वनस्पति शक्ति पिछले हफ्तों की तुलना में थोड़ी कम है। मिट्टी की नमी की निगरानी करें और कीटों के शुरुआती संकेतों की जांच करें।',
        'stable_explanation': '✅ फसल की स्थिति स्थिर या सुधर रही है। पिछली अवधि की तुलना में कोई महत्वपूर्ण तनाव विसंगति का पता नहीं चला।',
        
        # Maps & Visualizations
        'interactive_maps': '🗺️ इंटरैक्टिव विश्लेषण मानचित्र',
        'select_map_view': 'मानचित्र दृश्य चुनें:',
        'recent_analysis': 'हाल का विश्लेषण (वर्तमान स्वास्थ्य)',
        'time_comparison': 'समय तुलना (पहले बनाम अब)',
        'toggle_map_view': 'NDVI ओवरले देखने के लिए मानचित्र/उपग्रह दृश्य के बीच टॉगल करें',
        
        # PDF Report
        'download_report': '📄 खेत रिपोर्ट डाउनलोड करें (PDF)',
        'generating_report': 'रिपोर्ट तैयार की जा रही है...',
        
        # Messages
        'analysis_complete': '✅ विश्लेषण पूर्ण! **परिणाम** टैब देखें।',
        'no_analysis': '👈 कृपया पहले **क्षेत्र चुनें** टैब में विश्लेषण पूरा करें।',
    },
    
    'te': {
        # App Title & Headers
        'app_title': '🌾 క్రాప్‌గార్డ్ - పంట ఆరోగ్య పర్యవేక్షణ',
        'app_subtitle': 'సెంటినెల్-2 ఉపగ్రహ చిత్రాలను ఉపయోగించి స్వయంచాలక పంట ఆరోగ్య అంచనా',
        'select_area_tab': 'ప్రాంతాన్ని ఎంచుకోండి',
        'results_tab': 'విశ్లేషణ ఫలితాలు',
        
        # Sidebar
        'sidebar_title': '📍 పొలం ఎంపిక',
        'location_method': 'స్థాన ఇన్‌పుట్ పద్ధతి',
        'manual_coords': 'మాన్యువల్ కోఆర్డినేట్‌లు',
        'search_location': 'స్థానాన్ని శోధించండి',
        'latitude': 'అక్షాంశం',
        'longitude': 'రేఖాంశం',
        'area_size': 'పొలం విస్తీర్ణం (km²)',
        'run_analysis': '🚀 విశ్లేషణ అమలు చేయండి',
        'language_selector': 'Language / भाषा / భాష',
        
        # Risk Levels
        'high_risk': 'అధిక ప్రమాదం',
        'medium_risk': 'మధ్యస్థ ప్రమాదం',
        'stable': 'స్థిరమైన',
        
        # AI Analysis
        'ai_analysis': '🤖 AI విశ్లేషణ:',
        'action': '🚜 చర్య:',
        'ndvi_change': '📉 NDVI మార్పు:',
        'ai_health_score': '🧠 AI ఆరోగ్య స్కోర్',
        'detected_crop': 'గుర్తించిన పంట',
        
        # Recommendations
        'high_risk_action': '🚨 **అత్యవసరం**: వెంటనే నీటిపారుదల పెంచండి మరియు తెగులు/వ్యాధి వ్యాప్తి కోసం పొలాన్ని తనిఖీ చేయండి।',
        'medium_risk_action': '👀 **సలహా**: నేల తేమను నిశితంగా పర్యవేక్షించండి మరియు పసుపు రంగు యొక్క ప్రారంభ సంకేతాల కోసం తనిఖీ చేయండి।',
        'stable_action': '✅ **సలహా**: ప్రస్తుత సంరక్షణ షెడ్యూల్‌ను కొనసాగించండి। తక్షణ చర్య అవసరం లేదు।',
        
        # Explanations
        'high_risk_explanation': '⚠️ గణనీయమైన వృక్షసంపద క్షీణత గుర్తించబడింది। సంభావ్య కారణాలలో తీవ్రమైన నీటి ఒత్తిడి, తెగులు సోకడం లేదా వ్యాధి వ్యాప్తి ఉన్నాయి। తక్షణ తనిఖీ సిఫార్సు చేయబడింది।',
        'medium_risk_explanation': '⚠️ ఒత్తిడి యొక్క ప్రారంభ సంకేతాలు గుర్తించబడ్డాయి। వృక్షసంపద శక్తి మునుపటి వారాల కంటే కొంచెం తక్కువగా ఉంది। నేల తేమను పర్యవేక్షించండి మరియు తెగుల ప్రారంభ సంకేతాల కోసం తనిఖీ చేయండి।',
        'stable_explanation': '✅ పంట పరిస్థితి స్థిరంగా లేదా మెరుగుపడుతోంది। మునుపటి కాలంతో పోలిస్తే ఎటువంటి ముఖ్యమైన ఒత్తిడి అసాధారణతలు గుర్తించబడలేదు।',
        
        # Maps & Visualizations
        'interactive_maps': '🗺️ ఇంటరాక్టివ్ విశ్లేషణ మ్యాప్‌లు',
        'select_map_view': 'మ్యాప్ వీక్షణను ఎంచుకోండి:',
        'recent_analysis': 'ఇటీవలి విశ్లేషణ (ప్రస్తుత ఆరోగ్యం)',
        'time_comparison': 'సమయ పోలిక (ముందు vs ఇప్పుడు)',
        'toggle_map_view': 'NDVI ఓవర్‌లేను చూడటానికి మ్యాప్/శాటిలైట్ వీక్షణ మధ్య టోగుల్ చేయండి',
        
        # PDF Report
        'download_report': '📄 పొలం నివేదికను డౌన్‌లోడ్ చేయండి (PDF)',
        'generating_report': 'నివేదిక రూపొందించబడుతోంది...',
        
        # Messages
        'analysis_complete': '✅ విశ్లేషణ పూర్తయింది! **ఫలితాలు** ట్యాబ్ చూడండి।',
        'no_analysis': '👈 దయచేసి ముందుగా **ప్రాంతాన్ని ఎంచుకోండి** ట్యాబ్‌లో విశ్లేషణను పూర్తి చేయండి।',
    }
}

def get_text(key, lang='en'):
    """
    Get translated text for a given key and language.
    
    Args:
        key (str): Translation key
        lang (str): Language code ('en', 'hi', 'te')
        
    Returns:
        str: Translated text (fallback to English if not found)
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
