"""
Farmer Mode Helper Functions
Provides simplified farmer-friendly UI components
"""

def get_farmer_status(risk_level, lang, get_text_func):
    """Get farmer-friendly status based on risk level"""
    if risk_level == 'High Risk':
        return {
            'icon': '🚨',
            'emoji': '😰',
            'text': get_text_func('farmer_urgent', lang),
            'subtitle': get_text_func('farmer_water_needed', lang),
            'color': '#dc2626',
            'message': get_text_func('farmer_thirsty', lang),
            'visual': '🌾➡️💀'
        }
    elif risk_level == 'Medium Risk':
        return {
            'icon': '⚠️',
            'emoji': '😐',
            'text': get_text_func('farmer_watch', lang),
            'subtitle': get_text_func('farmer_getting_weak', lang),
            'color': '#ea580c',
            'message': get_text_func('farmer_weak', lang),
            'visual': '🌾➡️😐'
        }
    else:
        return {
            'icon': '✅',
            'emoji': '😊',
            'text': get_text_func('farmer_good', lang),
            'subtitle': get_text_func('farmer_healthy', lang),
            'color': '#16a34a',
            'message': get_text_func('farmer_strong', lang),
            'visual': '🌾➡️💪'
        }

def get_farmer_actions(risk_level, lang, get_text_func):
    """Get farmer-friendly action list based on risk level"""
    if risk_level == 'High Risk':
        return [
            ('💧', get_text_func('farmer_action_water_today', lang), get_text_func('farmer_detail_water', lang)),
            ('⏰', get_text_func('farmer_action_water_hours', lang), get_text_func('farmer_detail_hours', lang)),
            ('👀', get_text_func('farmer_action_check_tomorrow', lang), get_text_func('farmer_detail_tomorrow', lang)),
            ('📞', get_text_func('farmer_action_call_help', lang), get_text_func('farmer_detail_help', lang))
        ]
    elif risk_level == 'Medium Risk':
        return [
            ('🚶', get_text_func('farmer_action_walk', lang), get_text_func('farmer_detail_walk', lang)),
            ('👀', get_text_func('farmer_action_look_yellow', lang), get_text_func('farmer_detail_yellow', lang)),
            ('💧', get_text_func('farmer_action_water_dry', lang), get_text_func('farmer_detail_dry', lang)),
            ('📅', get_text_func('farmer_action_check_3days', lang), get_text_func('farmer_detail_monitor', lang))
        ]
    else:
        return [
            ('✅', get_text_func('farmer_action_keep_doing', lang), get_text_func('farmer_detail_doing_right', lang)),
            ('🌾', get_text_func('farmer_action_looks_good', lang), get_text_func('farmer_detail_green', lang)),
            ('📅', get_text_func('farmer_action_check_7days', lang), get_text_func('farmer_detail_weekly', lang)),
            ('😊', get_text_func('farmer_action_no_action', lang), get_text_func('farmer_detail_relax', lang))
        ]

def get_check_schedule(risk_level, lang, get_text_func):
    """Get when to check again based on risk level"""
    if risk_level == 'High Risk':
        return (get_text_func('farmer_tomorrow', lang), get_text_func('farmer_morning', lang))
    elif risk_level == 'Medium Risk':
        return (get_text_func('farmer_3days', lang), get_text_func('farmer_anytime', lang))
    else:
        return (get_text_func('farmer_7days', lang), get_text_func('farmer_weekly', lang))

def get_comparison_text(ndvi_change, lang, get_text_func):
    """Get comparison text based on NDVI change"""
    if ndvi_change < -0.1:
        return {
            'icon': '📉',
            'text': get_text_func('farmer_weaker', lang),
            'color': '#dc2626',
            'emoji': '😟'
        }
    elif ndvi_change > 0.1:
        return {
            'icon': '📈',
            'text': get_text_func('farmer_better', lang),
            'color': '#16a34a',
            'emoji': '😊'
        }
    else:
        return {
            'icon': '➡️',
            'text': get_text_func('farmer_same', lang),
            'color': '#ea580c',
            'emoji': '😐'
        }
