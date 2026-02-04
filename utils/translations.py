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
        
        # Farmer Mode
        'farmer_title': 'Field Health',
        'farmer_subtitle': 'In Simple Words',
        'farmer_urgent': 'URGENT',
        'farmer_watch': 'WATCH CAREFULLY',
        'farmer_good': 'ALL GOOD',
        'farmer_water_needed': 'Crops Need Water',
        'farmer_getting_weak': 'Crops Getting Weak',
        'farmer_healthy': 'Crops Are Healthy',
        'farmer_thirsty': 'Your crops are thirsty, like a person needs water in summer heat',
        'farmer_weak': 'Crops are a bit weak, like a sick child',
        'farmer_strong': 'Crops are strong, like a healthy child',
        'farmer_what_to_do': 'What To Do Today',
        'farmer_weather': 'Weather',
        'farmer_your_crop': 'Your Crop',
        'farmer_crop_name': 'Crop Name',
        'farmer_comparison': 'Comparison with Last Time',
        'farmer_weaker': 'Crops weaker than last time',
        'farmer_better': 'Crops better than last time',
        'farmer_same': 'Crops same as before',
        'farmer_help': 'Need Help?',
        'farmer_help_text': '**Contact Agriculture Department**\n\n📞 Toll Free: 1800-180-1551 (Kisan Call Center)\n\nOr ask your neighbor farmer\n\nOr meet village agriculture advisor',
        'farmer_check_next': 'When to check next:',
        'farmer_tomorrow': 'Tomorrow',
        'farmer_3days': 'After 3 days',
        'farmer_7days': 'After 7 days',
        'farmer_morning': 'Morning 7-8 AM',
        'farmer_anytime': 'Morning or evening',
        'farmer_weekly': 'Once a week',
        'farmer_hot': 'Hot',
        'farmer_rain': 'Rain',
        'farmer_wind': 'Wind',
        'farmer_no_rain': 'No',
        'farmer_light_wind': 'Light',
        'farmer_very_hot': 'Very hot - crops need more water',
        'farmer_noon_hot': 'Afternoon very hot',
        'farmer_no_rain_days': 'No rain for 15 days',
        'farmer_normal': 'Normal',
        # Actions - High Risk
        'farmer_action_water_today': 'Start watering TODAY',
        'farmer_action_water_hours': 'Water for 2-3 hours',
        'farmer_action_check_tomorrow': 'Check again tomorrow',
        'farmer_action_call_help': 'Call for help if needed',
        'farmer_detail_water': 'Like giving water to thirsty person',
        'farmer_detail_hours': 'Morning or evening time',
        'farmer_detail_tomorrow': 'Visit field in morning',
        'farmer_detail_help': 'Agriculture dept or neighbor',
        # Actions - Medium Risk
        'farmer_action_walk': 'Walk through field',
        'farmer_action_look_yellow': 'Look for yellow/brown leaves',
        'farmer_action_water_dry': 'Water if soil is dry',
        'farmer_action_check_3days': 'Check again in 3 days',
        'farmer_detail_walk': 'Morning or evening',
        'farmer_detail_yellow': 'Signs of sickness',
        'farmer_detail_dry': 'Touch soil with hand',
        'farmer_detail_monitor': 'Regular monitoring',
        # Actions - Low Risk
        'farmer_action_keep_doing': 'Keep doing what you\'re doing',
        'farmer_action_looks_good': 'Crops look good',
        'farmer_action_check_7days': 'Check again in 7 days',
        'farmer_action_no_action': 'No action needed now',
        'farmer_detail_doing_right': 'You\'re doing right',
        'farmer_detail_green': 'Green and strong',
        'farmer_detail_weekly': 'Once a week',
        'farmer_detail_relax': 'Relax',
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
        
        # Farmer Mode
        'farmer_title': 'खेत की सेहत',
        'farmer_subtitle': 'आसान भाषा में',
        'farmer_urgent': 'तुरंत ध्यान दें',
        'farmer_watch': 'ध्यान रखें',
        'farmer_good': 'सब ठीक है',
        'farmer_water_needed': 'फसल को पानी चाहिए',
        'farmer_getting_weak': 'फसल कमजोर हो रही है',
        'farmer_healthy': 'फसल स्वस्थ है',
        'farmer_thirsty': 'आपकी फसल प्यासी है, जैसे गर्मी में इंसान को पानी चाहिए',
        'farmer_weak': 'फसल थोड़ी कमजोर है, जैसे बीमार बच्चा',
        'farmer_strong': 'फसल मजबूत है, जैसे स्वस्थ बच्चा',
        'farmer_what_to_do': 'आज क्या करें',
        'farmer_weather': 'मौसम',
        'farmer_your_crop': 'आपकी फसल',
        'farmer_crop_name': 'फसल का नाम',
        'farmer_comparison': 'पिछली बार से तुलना',
        'farmer_weaker': 'फसल पिछली बार से कमजोर हुई है',
        'farmer_better': 'फसल पिछली बार से बेहतर हुई है',
        'farmer_same': 'फसल वैसी ही है जैसी थी',
        'farmer_help': 'मदद चाहिए?',
        'farmer_help_text': '**कृषि विभाग से संपर्क करें**\\n\\n📞 टोल फ्री: 1800-180-1551 (किसान कॉल सेंटर)\\n\\nया अपने पड़ोसी किसान से पूछें\\n\\nया गांव के कृषि सलाहकार से मिलें',
        'farmer_check_next': 'अगली बार कब देखें:',
        'farmer_tomorrow': 'कल',
        'farmer_3days': '3 दिन बाद',
        'farmer_7days': '7 दिन बाद',
        'farmer_morning': 'सुबह 7-8 बजे',
        'farmer_anytime': 'सुबह या शाम',
        'farmer_weekly': 'हफ्ते में एक बार',
        'farmer_hot': 'गर्मी',
        'farmer_rain': 'बारिश',
        'farmer_wind': 'हवा',
        'farmer_no_rain': 'नहीं',
        'farmer_light_wind': 'हल्की',
        'farmer_very_hot': 'बहुत गर्मी है, फसल को ज्यादा पानी चाहिए',
        'farmer_noon_hot': 'दोपहर बहुत गर्म',
        'farmer_no_rain_days': '15 दिन से नहीं',
        'farmer_normal': 'सामान्य',
        # Actions
        'farmer_action_water_today': 'आज ही पानी दें',
        'farmer_action_water_hours': '2-3 घंटे पानी चलाएं',
        'farmer_action_check_tomorrow': 'कल फिर देखें',
        'farmer_action_call_help': 'मदद चाहिए तो फोन करें',
        'farmer_detail_water': 'जैसे प्यासे को पानी देते हैं',
        'farmer_detail_hours': 'सुबह या शाम को',
        'farmer_detail_tomorrow': 'सुबह खेत में जाएं',
        'farmer_detail_help': 'कृषि विभाग या पड़ोसी किसान',
        'farmer_action_walk': 'खेत में घूमें',
        'farmer_action_look_yellow': 'पीले या भूरे पत्ते देखें',
        'farmer_action_water_dry': 'मिट्टी सूखी हो तो पानी दें',
        'farmer_action_check_3days': '3 दिन बाद फिर जांचें',
        'farmer_detail_walk': 'सुबह या शाम को',
        'farmer_detail_yellow': 'बीमारी के लक्षण',
        'farmer_detail_dry': 'हाथ से मिट्टी छूकर देखें',
        'farmer_detail_monitor': 'नियमित निगरानी',
        'farmer_action_keep_doing': 'वही करते रहें जो कर रहे हैं',
        'farmer_action_looks_good': 'फसल अच्छी है',
        'farmer_action_check_7days': '7 दिन बाद फिर देखें',
        'farmer_action_no_action': 'कोई काम नहीं',
        'farmer_detail_doing_right': 'आप सही काम कर रहे हैं',
        'farmer_detail_green': 'हरी और मजबूत',
        'farmer_detail_weekly': 'हफ्ते में एक बार',
        'farmer_detail_relax': 'आराम करें',
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
