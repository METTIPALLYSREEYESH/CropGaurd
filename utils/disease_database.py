"""
Disease Database & Detection
Contains information about common crop diseases and their characteristics
"""

# Disease Database with indicators, treatments, and information
DISEASE_DATABASE = {
    'Powdery Mildew': {
        'icon': '🔴',
        'crops': ['Rice', 'Wheat', 'Cotton', 'Maize', 'Soybean'],
        'description': 'White powdery coating on leaves',
        'indicators': {
            'ndvi_drop': 0.15,  # NDVI drops by this amount when present
            'optimal_humidity': (70, 100),  # Humidity range that encourages disease
            'optimal_temp': (15, 25),  # Temperature range for disease spread
            'spectral_signature': 'high_blue_low_red'  # Spectral characteristic
        },
        'severity_levels': {
            'mild': {'threshold': 0.05, 'description': 'Early stage infection'},
            'moderate': {'threshold': 0.15, 'description': 'Visible white coating'},
            'severe': {'threshold': 0.30, 'description': 'Widespread infection affecting yield'}
        },
        'treatments': [
            '🔬 Apply sulfur-based fungicide (10-14 day interval)',
            '💨 Improve air circulation - thin dense foliage',
            '🌡️ Reduce field humidity through drainage',
            '🚫 Remove infected leaves to prevent spread',
            '🧴 Use neem oil spray (organic alternative)'
        ],
        'prevention': [
            'Maintain proper plant spacing for air flow',
            'Avoid overhead irrigation in evenings',
            'Select resistant crop varieties',
            'Monitor humidity levels closely',
            'Regular field inspections'
        ],
        'local_names': {
            'en': 'Powdery Mildew',
            'hi': 'सफेद चूर्ण रोग',
            'te': 'తెల్ల పొడిపూత'
        }
    },
    
    'Leaf Rust': {
        'icon': '🟠',
        'crops': ['Wheat', 'Rice', 'Maize'],
        'description': 'Reddish-brown pustules on leaves',
        'indicators': {
            'ndvi_drop': 0.20,
            'optimal_humidity': (65, 95),
            'optimal_temp': (10, 25),
            'spectral_signature': 'high_red_low_nir'
        },
        'severity_levels': {
            'mild': {'threshold': 0.08, 'description': 'Few pustules visible'},
            'moderate': {'threshold': 0.18, 'description': 'Significant pustule coverage'},
            'severe': {'threshold': 0.35, 'description': 'Heavy rust affecting photosynthesis'}
        },
        'treatments': [
            '🔬 Apply rust fungicide (Propiconazole/Tebuconazole)',
            '✂️ Remove heavily infected leaves',
            '🌬️ Ensure good air circulation',
            '💧 Optimize irrigation - avoid leaf wetness',
            '🧴 Early intervention is critical for rust'
        ],
        'prevention': [
            'Use resistant wheat varieties',
            'Plant at optimum time for season',
            'Avoid high nitrogen fertilizer',
            'Monitor weather conditions for disease spread',
            'Early scouting and detection'
        ],
        'local_names': {
            'en': 'Leaf Rust',
            'hi': 'पत्ती दाद',
            'te': 'ఆకు తుప్పు'
        }
    },
    
    'Blast Disease': {
        'icon': '🔴',
        'crops': ['Rice'],
        'description': 'Diamond-shaped gray lesions on leaves and panicles',
        'indicators': {
            'ndvi_drop': 0.25,
            'optimal_humidity': (80, 100),
            'optimal_temp': (25, 30),
            'spectral_signature': 'gray_lesion_pattern'
        },
        'severity_levels': {
            'mild': {'threshold': 0.10, 'description': 'Leaf blast stage'},
            'moderate': {'threshold': 0.20, 'description': 'Panicle blast emerging'},
            'severe': {'threshold': 0.35, 'description': 'Complete panicle necrosis - yield loss'}
        },
        'treatments': [
            '🔬 Apply Triazole fungicides (Tebuconazole/Propiconazole)',
            '💧 Drain excess water from fields',
            '🌬️ Avoid high nitrogen - reduces plant defense',
            '🚫 Remove infected plant material',
            '💊 Use silicon-rich fertilizers (strengthens plant)'
        ],
        'prevention': [
            'Use blast-resistant rice varieties',
            'Proper water management - avoid waterlogging',
            'Balanced fertilizer use',
            'Crop rotation practiced',
            'Early detection and monitoring'
        ],
        'local_names': {
            'en': 'Blast Disease',
            'hi': 'धान ब्लास्ट',
            'te': 'బ్లాస్ట్ వ్యాధి'
        }
    },
    
    'Bacterial Wilt': {
        'icon': '🔴',
        'crops': ['Cotton', 'Tomato', 'Chick Pea'],
        'description': 'Wilting of leaves despite soil moisture',
        'indicators': {
            'ndvi_drop': 0.30,
            'optimal_humidity': (60, 85),
            'optimal_temp': (25, 35),
            'spectral_signature': 'rapid_wilting_pattern'
        },
        'severity_levels': {
            'mild': {'threshold': 0.10, 'description': 'Wilting in afternoon sun'},
            'moderate': {'threshold': 0.22, 'description': 'Persistent wilting throughout day'},
            'severe': {'threshold': 0.40, 'description': 'Complete plant death - no recovery'}
        },
        'treatments': [
            '🔬 No direct cure - manage symptoms with copper fungicides',
            '💧 Increase irrigation despite wilting',
            '🚫 Remove and destroy infected plants',
            '🔥 Sterilize equipment to prevent spread',
            '🌱 Plant resistant varieties next season'
        ],
        'prevention': [
            'Use disease-resistant varieties',
            'Crop rotation (3-4 years)',
            'Control insect vectors',
            'Remove infected plant debris',
            'Avoid overhead irrigation'
        ],
        'local_names': {
            'en': 'Bacterial Wilt',
            'hi': 'जीवाणु मुरझान',
            'te': 'బ్యాక్టీరియల్ విల్ట్'
        }
    },
    
    'Early Blight': {
        'icon': '🟠',
        'crops': ['Tomato', 'Cotton'],
        'description': 'Concentric rings on lower leaves',
        'indicators': {
            'ndvi_drop': 0.18,
            'optimal_humidity': (85, 100),
            'optimal_temp': (20, 28),
            'spectral_signature': 'circular_lesion_pattern'
        },
        'severity_levels': {
            'mild': {'threshold': 0.08, 'description': 'Target-like lesions on lower leaves'},
            'moderate': {'threshold': 0.16, 'description': 'Lesions spreading to mid-canopy'},
            'severe': {'threshold': 0.30, 'description': 'Severe defoliation affecting yield'}
        },
        'treatments': [
            '🔬 Apply Mancozeb or Chlorothalonil fungicide',
            '✂️ Remove lower infected leaves (sanitation)',
            '💨 Improve air circulation by pruning',
            '💧 Avoid overhead watering - keep leaves dry',
            '🧴 Weekly spray schedule in humid conditions'
        ],
        'prevention': [
            'Use certified disease-free seeds',
            'Proper spacing for air flow',
            'Mulching to prevent soil splash',
            'Resistant tomato varieties available',
            'Regular field scouting'
        ],
        'local_names': {
            'en': 'Early Blight',
            'hi': 'प्रारंभिक अंगमारी',
            'te': 'ప్రారంభ చిత్తలు'
        }
    },
    
    'Septoria Leaf Spot': {
        'icon': '🟡',
        'crops': ['Wheat', 'Rice'],
        'description': 'Small circular lesions with dark borders',
        'indicators': {
            'ndvi_drop': 0.12,
            'optimal_humidity': (85, 100),
            'optimal_temp': (15, 22),
            'spectral_signature': 'small_spot_pattern'
        },
        'severity_levels': {
            'mild': {'threshold': 0.05, 'description': 'Few lesions on lower leaves'},
            'moderate': {'threshold': 0.12, 'description': 'Multiple lesions across plant'},
            'severe': {'threshold': 0.25, 'description': 'Extensive defoliation'}
        },
        'treatments': [
            '🔬 Apply Pyraclostrobin or Fluquinconazole',
            '✂️ Remove affected leaves promptly',
            '🌬️ Ensure good air circulation',
            '💧 Reduce leaf wetness duration',
            '🗑️ Remove crop residue after harvest'
        ],
        'prevention': [
            'Use resistant wheat varieties',
            'Avoid overhead irrigation',
            'Crop rotation with non-host crops',
            'Clean equipment between fields',
            'Early scouting and monitoring'
        ],
        'local_names': {
            'en': 'Septoria Leaf Spot',
            'hi': 'सेप्टोरिया पत्ती दाग',
            'te': 'సెప్టోరియా ఆకు చిత్తలు'
        }
    },
    
    'Anthracnose': {
        'icon': '🔴',
        'crops': ['Cotton', 'Maize', 'Soybean'],
        'description': 'Dark lesions with yellowish halo',
        'indicators': {
            'ndvi_drop': 0.22,
            'optimal_humidity': (75, 95),
            'optimal_temp': (22, 28),
            'spectral_signature': 'dark_lesion_pattern'
        },
        'severity_levels': {
            'mild': {'threshold': 0.08, 'description': 'Few lesions on leaves'},
            'moderate': {'threshold': 0.18, 'description': 'Moderate lesion coverage'},
            'severe': {'threshold': 0.32, 'description': 'Pod/seed damage - significant yield loss'}
        },
        'treatments': [
            '🔬 Apply Carbendazim or Mancozeb fungicide',
            '✂️ Remove and burn infected plant parts',
            '💨 Improve air circulation',
            '💧 Avoid leaf wetness - manage irrigation',
            '🔄 Repeat sprays at 10-14 day intervals'
        ],
        'prevention': [
            'Use certified disease-free seeds',
            'Resistant crop varieties',
            'Crop rotation (2-3 years)',
            'Proper field sanitation',
            'Monitor during humid seasons'
        ],
        'local_names': {
            'en': 'Anthracnose',
            'hi': 'एन्थ्रेक्नोज',
            'te': 'అన్థ్రాక్నోస్'
        }
    },
}

def get_disease_by_name(disease_name):
    """Get disease information by name"""
    return DISEASE_DATABASE.get(disease_name, None)

def get_diseases_for_crop(crop_name):
    """Get all possible diseases for a crop"""
    diseases = []
    for disease_name, disease_info in DISEASE_DATABASE.items():
        if crop_name in disease_info['crops']:
            diseases.append((disease_name, disease_info))
    return diseases

def get_all_diseases():
    """Get all diseases in database"""
    return list(DISEASE_DATABASE.keys())

def get_treatment_recommendations(disease_name, lang='en'):
    """Get treatment recommendations for a disease"""
    disease = get_disease_by_name(disease_name)
    if not disease:
        return []
    return disease.get('treatments', [])

def get_prevention_tips(disease_name, lang='en'):
    """Get prevention tips for a disease"""
    disease = get_disease_by_name(disease_name)
    if not disease:
        return []
    return disease.get('prevention', [])

def get_disease_local_name(disease_name, lang='en'):
    """Get localized disease name"""
    disease = get_disease_by_name(disease_name)
    if not disease:
        return disease_name
    return disease.get('local_names', {}).get(lang, disease_name)
