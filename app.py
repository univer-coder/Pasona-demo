import streamlit as st
import time
import math
from datetime import datetime, timedelta

# =====================================
# Page configuration
# =====================================
st.set_page_config(
    page_title="Awaji Island Travel Planner & Q&A",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# Language dictionary and helper
# =====================================
LANG_DICT = {
    "EN": {
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "prefer_not_say": "Prefer not to say",
        "travel_purpose": "Travel Purpose",
        "solo": "Solo",
        "couple": "Couple",
        "family": "Family",
        "friends": "Friends",
        "generate_itinerary": "Generate 3 Personalized Plans",
        "num_days": "Number of Days",
        "plans_label": "Plans",
        "plan_standard": "Plan A: Standard",
        "plan_relaxing": "Plan B: Relaxing",
        "plan_active": "Plan C: Active",
        "app_title": "Awaji Island Itinerary Planner",
        "plan_instruction": "Choose plans comparing 3 different themes",
        "generating": "Generating...",
        "tab_itinerary": "🛠️ Create Itinerary",
        "tab_chat": "💬 AI Chat",
        "recommended_course": "💡 Recommended Model Course",
        "course_family": "Perfect Family Adventure Course",
        "course_couple": "Romantic Scenic Couple's Escape",
        "course_women_friends": "Instagram-Ready Girl's Trip",
        "course_luxury": "Luxury Relaxation & Fine Dining",
        "course_standard": "Classic Heritage Experience",
        "customize_itinerary": "Customize itinerary",
        "back_to_itinerary": "Back to itinerary",
        "view_map": "View map",
        "close_map": "Close map",
        "time_required": "Time Required",
        "cost": "Cost",
        "schedule": "Schedule",
        "activity": "Activity",
        "restaurant": "Restaurant",
        "hotel": "Hotel",
        "view_details": "View Details",
        "home_label": "Home",
        "chat_label": "Chat",
        "news_label": "News",
        "account_label": "Account",
        "language_label": "Language",
    },
    "JA": {
        "age": "年齢",
        "gender": "性別",
        "male": "男性",
        "female": "女性",
        "other": "その他",
        "prefer_not_say": "回答しない",
        "travel_purpose": "旅行の目的",
        "solo": "一人",
        "couple": "カップル",
        "family": "家族",
        "friends": "友達",
        "generate_itinerary": "3つのパーソナライズプランを生成",
        "num_days": "宿泊日数",
        "plans_label": "プラン",
        "plan_standard": "プランA: スタンダード",
        "plan_relaxing": "プランB: リラックス",
        "plan_active": "プランC: アクティブ",
        "app_title": "淡路島旅程プランナー",
        "plan_instruction": "3つの異なるテーマのプランを比較して選びましょう",
        "generating": "生成中...",
        "tab_itinerary": "🛠️ 旅程作成",
        "tab_chat": "💬 AIチャット",
        "recommended_course": "💡 推奨モデルコース",
        "course_family": "子どもが喜ぶ淡路島家族旅行コース",
        "course_couple": "カップル向けロマンティック絶景コース",
        "course_women_friends": "インスタ映え女子旅コース",
        "course_luxury": "上質な検花と紅葉コース",
        "course_standard": "淡路山三年室錦を愛でる史跡コース",
        "customize_itinerary": "旅程をカスタマイズ",
        "back_to_itinerary": "旅程に戻る",
        "view_map": "地図を見る",
        "close_map": "地図を閉じる",
        "time_required": "所要時間",
        "cost": "費用",
        "schedule": "スケジュール",
        "activity": "アクティビティ",
        "restaurant": "レストラン",
        "hotel": "ホテル",
        "view_details": "詳細を見る",
        "home_label": "ホーム",
        "chat_label": "チャット",
        "news_label": "ニュース",
        "account_label": "アカウント",
        "language_label": "言語",
    }
}

def t(key):
    lang = st.session_state.get("lang", "EN")
    return LANG_DICT.get(lang, LANG_DICT["EN"]).get(key, key)

# =====================================
# Global CSS style injection
# =====================================
def inject_custom_css():
    """
    ネイティブスマホアプリに近いデザインのカスタムCSSを注入
    """
    custom_css = """
    <style>
    /* ========== base styles ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background-color: #f5f5f5;
    }
    
    /* ========== Streamlit default overrides ========== */
    .stApp {
        padding-bottom: 80px !important;
    }
    
    /* ========== main header ========== */
    .main-header {
        background: linear-gradient(135deg, #1a7f8f 0%, #2a9fa9 100%);
        color: white;
        padding: 24px 16px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(26, 127, 143, 0.15);
    }
    
    .main-header h1 {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        font-size: 13px;
        margin: 6px 0 0 0;
        opacity: 0.9;
    }
    
    /* ========== action button ========== */
    .main-action-btn {
        width: 100%;
        padding: 16px;
        margin: 16px 0;
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.25);
    }
    
    .main-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(23, 162, 184, 0.35);
    }
    
    .main-action-btn:active {
        transform: translateY(0);
    }
    
    /* ========== card style ========== */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin: 16px 0;
    }
    
    .card {
        position: relative;
        height: 280px;
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* overlay gradient */
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.5) 100%);
        z-index: 1;
    }
    
    /* card title text */
    .card-title {
        position: absolute;
        bottom: 70px;
        left: 16px;
        right: 16px;
        font-size: 20px;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        z-index: 2;
        line-height: 1.3;
    }
    
    /* card button */
    .card-button {
        position: absolute;
        bottom: 12px;
        left: 16px;
        right: 16px;
        padding: 10px 16px;
        background: white;
        color: #17a2b8;
        border: none;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 3;
        text-align: center;
    }
    
    .card-button:hover {
        background: #f8f8f8;
        transform: scale(1.02);
    }
    
    /* ========== bottom navigation ========== */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 70px;
        background: white;
        border-top: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 100;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .nav-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        text-decoration: none;
        color: #999;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        background: none;
    }
    
    .nav-item:hover {
        color: #17a2b8;
    }
    
    .nav-item.active {
        color: #17a2b8;
        font-weight: 600;
    }
    
    .nav-icon {
        font-size: 24px;
        margin-bottom: 4px;
    }
    
    .nav-label {
        font-size: 11px;
    }
    
    /* ========== padding adjustment ========== */
    .bottom-padding {
        height: 80px;
    }
    
    /* ========== tab styles ========== */
    .stTabs {
        margin-top: 16px;
    }
    
    /* ========== alert box ========== */
    .plan-summary {
        background: linear-gradient(135deg, #e8f4f8 0%, #d4f1f9 100%);
        border-left: 4px solid #17a2b8;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    .plan-summary-title {
        font-size: 14px;
        font-weight: 600;
        color: #17a2b8;
        margin-bottom: 8px;
    }
    
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# カスタムCSSを注入
inject_custom_css()

# =====================================
# Facility data with bilingual descriptions (model course)
# =====================================

ACTIVITIES = [
    {
        "name": {"EN": "Nijigen no Mori", "JA": "ニジゲンノモリ"},
        "price": 2500,
        "lat": 34.5562,
        "lon": 134.8117,
        "time_required_hours": 3,
        "description": {
            "EN": "Anime theme park full of family-friendly attractions.",
            "JA": "ファミリーや若者に人気のアニメテーマパーク。多彩なアトラクションがあります。"
        },
        "tags": ["Family", "Youth"],
        "points": {
            "EN": ["Great for anime fans", "Outdoor activities", "Family friendly"],
            "JA": ["アニメファンに最適", "屋外アクティビティ", "家族向け"]
        }
    },
    {
        "name": {"EN": "Zenbo Seinei", "JA": "禅坊 靖寧"},
        "price": 8000,
        "lat": 34.5740,
        "lon": 134.8335,
        "time_required_hours": 2,
        "description": {
            "EN": "Luxury wellness retreat ideal for seniors and women.",
            "JA": "シニアや女性向けのラグジュアリーなウェルネス寺泊体験。"
        },
        "tags": ["Senior", "Luxury", "Female"],
        "points": {
            "EN": ["Calming atmosphere", "High-end service", "Scenic gardens"],
            "JA": ["落ち着いた雰囲気", "高級サービス", "景色の良い庭園"]
        }
    },
    {
        "name": {"EN": "Awaji Hanasajiki", "JA": "あわじ花さじき"},
        "price": 500,
        "lat": 34.5950,
        "lon": 134.8250,
        "time_required_hours": 1.5,
        "description": {
            "EN": "Flower field with panoramic views; popular among couples and friends.",
            "JA": "カップルや友人向けの花畑。パノラマビューが楽しめます。"
        },
        "tags": ["Couple", "Friends"],
        "points": {
            "EN": ["Instagrammable", "Seasonal blooms", "Picnic spots"],
            "JA": ["インスタ映え", "季節の花々", "ピクニックに最適"]
        }
    }
]

RESTAURANTS = [
    {
        "name": {"EN": "Miele", "JA": "ミエレ"},
        "price": 3000,
        "lat": 34.5681,
        "lon": 134.8112,
        "time_required_hours": 1,
        "description": {
            "EN": "Trendy cafe known for Awaji beef burgers, popular with youth and couples.",
            "JA": "淡路牛バーガーで有名なトレンディなカフェ。若者やカップルに人気です。"
        },
        "tags": ["Youth", "Couple", "Friends"],
        "points": {
            "EN": ["Stylish interior", "Local beef", "Great for photos"],
            "JA": ["おしゃれな内装", "地元産牛肉", "写真映え"]
        }
    },
    {
        "name": {"EN": "Auberge French no Mori", "JA": "オーベルジュ フレンチの森"},
        "price": 15000,
        "lat": 34.5805,
        "lon": 134.8250,
        "time_required_hours": 2,
        "description": {
            "EN": "Fine dining auberge for anniversaries and luxury seekers.",
            "JA": "記念日やラグジュアリー志向の方に最適なフレンチオーベルジュ。"
        },
        "tags": ["Senior", "Luxury"],
        "points": {
            "EN": ["Michelin-level cuisine", "Intimate setting", "Wine pairings"],
            "JA": ["ミシュラン級の料理", "落ち着いた空間", "ワインペアリング"]
        }
    },
    {
        "name": {"EN": "HELLO KITTY SMILE", "JA": "ハローキティスマイル"},
        "price": 2500,
        "lat": 34.5700,
        "lon": 134.8165,
        "time_required_hours": 1.5,
        "description": {
            "EN": "Family-friendly restaurant with Hello Kitty theme.",
            "JA": "ハローキティをテーマにした家族向けレストラン。"
        },
        "tags": ["Family"],
        "points": {
            "EN": ["Kids menu", "Cute decor", "Themed desserts"],
            "JA": ["キッズメニュー", "かわいい内装", "テーマデザート"]
        }
    }
]

HOTELS = [
    {
        "name": {"EN": "GRAND CHARIOT Hokuto Shichisei 135°", "JA": "グランドチャリオット 北斗七星135°"},
        "price": 50000,
        "lat": 34.5623,
        "lon": 134.8080,
        "time_required_hours": 0,
        "description": {
            "EN": "Extravagant resort perfect for families and luxury travelers.",
            "JA": "ファミリーや贅沢志向の旅行者にぴったりの豪華リゾート。"
        },
        "tags": ["Family", "Luxury"],
        "points": {
            "EN": ["Observation room", "Ocean view", "Kids facilities"],
            "JA": ["展望ルーム", "オーシャンビュー", "キッズ施設"]
        }
    },
    {
        "name": {"EN": "Resort with Private Bath", "JA": "貸切露天風呂付きリゾートホテル"},
        "price": 20000,
        "lat": 34.5690,
        "lon": 134.8200,
        "time_required_hours": 0,
        "description": {
            "EN": "Cozy resort hotel with private open-air bath, romantic for couples.",
            "JA": "カップル向けの貸切露天風呂付きリゾートホテル。"
        },
        "tags": ["Couple"],
        "points": {
            "EN": ["Private rotisserie", "Romantic ambiance", "Secluded"],
            "JA": ["貸切風呂", "ロマンチック", "静か"]
        }
    },
    {
        "name": {"EN": "Budget Guesthouse", "JA": "リーズナブルなゲストハウス"},
        "price": 5000,
        "lat": 34.5740,
        "lon": 134.8410,
        "time_required_hours": 0,
        "description": {
            "EN": "Affordable guesthouse popular with young solo travelers.",
            "JA": "若者のソロ旅行者に人気のリーズナブルなゲストハウス。"
        },
        "tags": ["Youth", "Solo"],
        "points": {
            "EN": ["Community kitchen", "Dorm rooms", "Cheap"],
            "JA": ["共同キッチン", "ドミトリー", "安い"]
        }
    }
]


# =====================================
# Utility functions for schedule calculation
# =====================================

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula (in km)."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def time_to_minutes(h, m):
    """Convert hours and minutes to total minutes."""
    return h * 60 + m

def minutes_to_time(minutes):
    """Convert minutes to (h, m) tuple."""
    h = int(minutes // 60)
    m = int(minutes % 60)
    return (h, m)

def format_time(h, m):
    """Format time as HH:MM string."""
    return f"{h:02d}:{m:02d}"

def add_hours(h, m, hours_to_add):
    """Add hours to a time, returning (h, m) tuple."""
    total_min = h * 60 + m + int(hours_to_add * 60)
    return minutes_to_time(total_min)

def next_bus_time(hour, minute):
    """Round up to next :00 or :30 mark (30-minute intervals)."""
    total_min = hour * 60 + minute
    remainder = total_min % 30
    if remainder == 0:
        next_total_min = total_min + 30
    else:
        next_total_min = ((total_min // 30) + 1) * 30
    h, m = minutes_to_time(next_total_min)
    return (h, m)

def calculate_schedule(activity, restaurant, hotel, num_days):
    """
    Generate a detailed timeline schedule using datetime.
    
    Returns a dict with timeline events (start_time, end_time, name, type).
    """
    shuttle_move_minutes = 30  # Fixed 30-minute shuttle travel time
    
    timeline = []
    total_cost = activity["price"] + restaurant["price"] + hotel["price"]
    
    # Start time: 09:00
    current_time = datetime.strptime("09:00", "%H:%M")
    
    # === Activity ===
    activity_duration_min = int(activity["time_required_hours"] * 60)
    activity_start = current_time
    activity_end = current_time + timedelta(minutes=activity_duration_min)
    timeline.append({
        "start": activity_start.strftime("%H:%M"),
        "end": activity_end.strftime("%H:%M"),
        "name": activity["name"],
        "type": "activity"
    })
    
    # After activity, find next bus at :00 or :30
    after_activity = activity_end
    minute = after_activity.minute
    if minute <= 30:
        bus_depart = after_activity.replace(minute=30, second=0, microsecond=0)
        if minute > 30:
            bus_depart = bus_depart + timedelta(hours=1)
    else:
        bus_depart = (after_activity + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    
    # Round up to next bus if exactly at the hour
    if after_activity.minute == 0 and after_activity.second == 0:
        bus_depart = after_activity
    elif after_activity.minute <= 30:
        bus_depart = after_activity.replace(minute=30 if after_activity.minute < 30 else 0)
        if after_activity.minute > 30:
            bus_depart = bus_depart + timedelta(hours=1)
    else:
        bus_depart = (after_activity + timedelta(hours=1)).replace(minute=0)
    
    # Simplified: round to next 30-min mark
    total_min = after_activity.hour * 60 + after_activity.minute
    remainder = total_min % 30
    if remainder == 0:
        bus_depart_min = total_min + 30
    else:
        bus_depart_min = ((total_min // 30) + 1) * 30
    bus_depart = datetime.strptime(f"{bus_depart_min // 60:02d}:{bus_depart_min % 60:02d}", "%H:%M")
    
    bus_arrive = bus_depart + timedelta(minutes=shuttle_move_minutes)
    timeline.append({
        "start": bus_depart.strftime("%H:%M"),
        "end": bus_arrive.strftime("%H:%M"),
        "name": {"EN": "Shuttle Bus", "JA": "シャトルバス"},
        "type": "shuttle"
    })
    
    # === Restaurant ===
    rest_duration_min = int(restaurant["time_required_hours"] * 60)
    rest_start = bus_arrive
    rest_end = rest_start + timedelta(minutes=rest_duration_min)
    timeline.append({
        "start": rest_start.strftime("%H:%M"),
        "end": rest_end.strftime("%H:%M"),
        "name": restaurant["name"],
        "type": "restaurant"
    })
    
    # Next shuttle to hotel
    after_rest = rest_end
    total_min = after_rest.hour * 60 + after_rest.minute
    remainder = total_min % 30
    if remainder == 0:
        bus2_depart_min = total_min + 30
    else:
        bus2_depart_min = ((total_min // 30) + 1) * 30
    bus2_depart = datetime.strptime(f"{bus2_depart_min // 60:02d}:{bus2_depart_min % 60:02d}", "%H:%M")
    bus2_arrive = bus2_depart + timedelta(minutes=shuttle_move_minutes)
    timeline.append({
        "start": bus2_depart.strftime("%H:%M"),
        "end": bus2_arrive.strftime("%H:%M"),
        "name": {"EN": "Shuttle Bus", "JA": "シャトルバス"},
        "type": "shuttle"
    })
    
    # === Hotel (check-in only) ===
    hotel_checkin = bus2_arrive
    timeline.append({
        "start": hotel_checkin.strftime("%H:%M"),
        "end": None,  # No checkout time for display
        "name": hotel["name"],
        "type": "hotel"
    })
    
    return {
        "activity": activity,
        "restaurant": restaurant,
        "hotel": hotel,
        "timeline": timeline,  # New: detailed timeline
        "schedule": [],  # Keep empty for backwards compatibility
        "total_cost": total_cost,
        "num_days": num_days
    }


def determine_model_course(age, gender, purpose, num_days):
    """
    Determine the recommended model course based on user attributes.
    Returns: {
        'course_key': str,  # Translation key for course name
        'course_name_ja': str,  # Japanese course name
        'course_name_en': str,  # English course name
        'priority_tags': list,  # Facility tags to prioritize
        'variations': list  # ['standard', 'fun', 'relaxing'] etc
    }
    """
    # Family with kids
    if purpose == "Family":
        return {
            "course_key": "course_family",
            "course_name_ja": "子どもが喜ぶ淡路島家族旅行コース",
            "course_name_en": "Perfect Family Adventure Course",
            "priority_tags": [["Family", "Youth"], ["Family"], ["Family", "Luxury"]],
            "variations": ["standard", "fun", "relaxing"]
        }
    # Couple
    elif purpose == "Couple":
        return {
            "course_key": "course_couple",
            "course_name_ja": "カップル向けロマンティック絶景コース",
            "course_name_en": "Romantic Scenic Couple's Escape",
            "priority_tags": [["Couple", "Friends"], ["Couple"], ["Couple", "Luxury"]],
            "variations": ["romantic", "scenic", "luxury"]
        }
    # Young women friends
    elif purpose == "Friends" and gender == "Female" and age < 40:
        return {
            "course_key": "course_women_friends",
            "course_name_ja": "インスタ映え女子旅コース",
            "course_name_en": "Instagram-Ready Girl's Trip",
            "priority_tags": [["Youth", "Friends"], ["Youth", "Couple"], ["Luxury"]],
            "variations": ["trendy", "scenic", "luxury"]
        }
    # Mature/luxury seekers
    elif age >= 40 and num_days >= 2:
        return {
            "course_key": "course_luxury",
            "course_name_ja": "上質な検花と紅葉コース",
            "course_name_en": "Luxury Relaxation & Fine Dining",
            "priority_tags": [["Senior", "Luxury"], ["Luxury"], ["Luxury"]],
            "variations": ["luxury", "relaxing", "gourmet"]
        }
    # Default/standard
    else:
        return {
            "course_key": "course_standard",
            "course_name_ja": "淡路山三年室錦を愛でる史跡コース",
            "course_name_en": "Classic Heritage Experience",
            "priority_tags": [[], [], []],  # No priority filtering
            "variations": ["standard", "active", "relaxing"]
        }

def generate_plans(age, gender, purpose, num_days):
    """
    Generate 3 personalized plans based on model course determination.
    Uses Haversine-based nearest neighbor selection within course priorities.
    Returns list of 3 plan dicts with timeline and course info.
    """
    plans = []
    
    # Determine recommended model course
    model_course = determine_model_course(age, gender, purpose, num_days)
    
    # For each of 3 plan variations
    for plan_idx in range(3):
        priority_tags = model_course["priority_tags"][plan_idx] if plan_idx < len(model_course["priority_tags"]) else []
        variation_name = model_course["variations"][plan_idx] if plan_idx < len(model_course["variations"]) else "standard"
        
        # Select activity based on priority tags
        if priority_tags:
            matching_activities = [a for a in ACTIVITIES if any(tag in a.get("tags", []) for tag in priority_tags)]
        else:
            matching_activities = ACTIVITIES
        
        if not matching_activities:
            matching_activities = ACTIVITIES
        
        # Pick first matching activity for this plan (could randomize for more variety)
        activity = matching_activities[plan_idx % len(matching_activities)]
        
        # Find nearest restaurant to activity
        nearest_restaurant = min(RESTAURANTS, key=lambda r: haversine_distance(activity["lat"], activity["lon"], r["lat"], r["lon"]))
        
        # Find nearest hotel to restaurant
        nearest_hotel = min(HOTELS, key=lambda h: haversine_distance(nearest_restaurant["lat"], nearest_restaurant["lon"], h["lat"], h["lon"]))
        
        # Calculate detailed timeline schedule
        schedule_data = calculate_schedule(activity, nearest_restaurant, nearest_hotel, num_days)
        
        # Add course and variation info
        schedule_data["theme"] = ["Standard", "Relaxing", "Active"][plan_idx]  # Keep for backwards compatibility
        schedule_data["variation"] = variation_name
        schedule_data["model_course_key"] = model_course["course_key"]
        schedule_data["model_course_name_ja"] = model_course["course_name_ja"]
        schedule_data["model_course_name_en"] = model_course["course_name_en"]
        
        plans.append(schedule_data)
    
    return plans


# =====================================
# Initialize session state
# =====================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# routing page
if "page" not in st.session_state:
    st.session_state.page = "main"

# language default
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

# stored choices for plans generation
if "plans_generated" not in st.session_state:
    st.session_state.plans_generated = False

# generated plans
if "current_plans" not in st.session_state:
    st.session_state.current_plans = None

# chosen items for custom itinerary
for key in ["chosen_activity", "chosen_rest", "chosen_hotel"]:
    if key not in st.session_state:
        st.session_state[key] = None


# =====================================
# Mock AI staff response function
# =====================================
def get_ai_response(user_question):
    """
    Keyword-based mock AI response with delay and language support.
    """
    lang = st.session_state.get("lang", "EN")
    question_lower = user_question.lower()
    time.sleep(1.5)
    if any(k in question_lower for k in ["recommend", "sightseeing", "tour", "おすすめ", "観光"]):
        if lang == "JA":
            return "淡路島のおすすめですね。西海岸の夕日スポットや、ニジゲンノモリの自然体験が人気です！どんな体験をお探しですか？"
        else:
            return "Looking for recommendations in Awaji? The West Coast area is famous for beautiful sunsets, and 'Nijigen no Mori' is great for nature and anime fans! What kind of experience are you looking for?"
    elif any(k in question_lower for k in ["hotel", "stay", "accommodation", "宿"]):
        if lang == "JA":
            return "宿泊先をお探しですか？海の見えるリゾートからアットホームなゲストハウスまで揃っています。ご予算はいかがでしょうか？"
        else:
            return "Looking for a place to stay? Awaji offers everything from ocean-view resorts to cozy guesthouses. What is your budget?"
    elif any(k in question_lower for k in ["food", "restaurant", "eat", "食"]):
        if lang == "JA":
            return "淡路牛バーガーや新鮮なしらす丼が有名です！海沿いのオシャレなカフェも多数あります。"
        else:
            return "Awaji is famous for its Awaji Beef burgers and fresh whitebait (shirasu) bowls! There are also many stylish cafes along the coast."
    else:
        if lang == "JA":
            return "ご質問ありがとうございます！現在その内容について学習中です。他に何かお手伝いできることはありますか？"
        else:
            return "Thank you for your question! Our AI staff is currently learning more about that. Is there anything else I can help you with today?"


# =====================================
# Bottom navigation rendering function
# =====================================
def render_bottom_navigation():
    """
    画面下部に固定されたボトムナビゲーションバーを描画
    """
    # labels pulled from translation helper
    nav_html = f"""
    <div class=\"bottom-nav\">
        <button class=\"nav-item\" onclick=\"document.location.href='#home'\">
            <div class=\"nav-icon\">🏠</div>
            <div class=\"nav-label\">{t('home_label')}</div>
        </button>
        <button class=\"nav-item\" onclick=\"document.location.href='#plans'\">
            <div class=\"nav-icon\">📋</div>
            <div class=\"nav-label\">{t('plans_label')}</div>
        </button>
        <button class=\"nav-item\" onclick=\"document.location.href='#chat'\">
            <div class=\"nav-icon\">💬</div>
            <div class=\"nav-label\">{t('chat_label')}</div>
        </button>
        <button class=\"nav-item\" onclick=\"document.location.href='#news'\">
            <div class=\"nav-icon\">📢</div>
            <div class=\"nav-label\">{t('news_label')}</div>
        </button>
        <button class=\"nav-item\" onclick=\"document.location.href='#mypage'\">
            <div class=\"nav-icon\">👤</div>
            <div class=\"nav-label\">{t('account_label')}</div>
        </button>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

# =====================================
# UI layout
# =====================================

# ====== language selector ======
with st.sidebar:
    st.selectbox(t('language_label'), ["EN", "JA"], index=["EN", "JA"].index(st.session_state.lang), key="lang")

# ====== user profile inputs ======
with st.container():
    col_age, col_gender, col_purpose, col_days, col_button = st.columns([1,1,1,0.8,1])
    age = col_age.number_input(t('age'), min_value=0, max_value=120, value=25, step=1)
    # use indices so we can map back to English values for logic
    gender_options = ["Male","Female","Other","Prefer not to say"]
    gender_labels = [t('male'), t('female'), t('other'), t('prefer_not_say')]
    # restore previous index if exists
    raw_g = st.session_state.get('gender_idx', 0)
    try:
        default_gidx = int(raw_g)
    except Exception:
        default_gidx = 0
    gender_idx = col_gender.selectbox(t('gender'), list(range(len(gender_options))),
                                      format_func=lambda i: gender_labels[i],
                                      index=default_gidx,
                                      key='gender_idx')
    gender = gender_options[gender_idx]
    purpose_options = ["Solo","Couple","Family","Friends"]
    purpose_labels = [t('solo'), t('couple'), t('family'), t('friends')]
    raw_p = st.session_state.get('purpose_idx', 0)
    try:
        default_pidx = int(raw_p)
    except Exception:
        default_pidx = 0
    purpose_idx = col_purpose.selectbox(t('travel_purpose'), list(range(len(purpose_options))),
                                        format_func=lambda i: purpose_labels[i],
                                        index=default_pidx,
                                        key='purpose_idx')
    purpose = purpose_options[purpose_idx]
    num_days = col_days.number_input(t('num_days'), min_value=1, max_value=10, value=1, step=1)
    gen_button = col_button.button(t('generate_itinerary'))

# Main header
header_html = f"""
<div class="main-header">
    <h1>🏝️ {t('app_title')}</h1>
    <p>{t('plan_instruction')}</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# routing between main and detail
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "detail":
    # show detail view for currently selected item
    item = st.session_state.get("detail_item")
    if item:
        # choose translated name, description, points
        name = item['name'].get(st.session_state.lang, next(iter(item['name'].values())))
        st.header(name)
        img_url = f"https://via.placeholder.com/600x400.png?text={name}"
        st.image(img_url, use_column_width=True)
        # description
        desc = item.get('description', {}).get(st.session_state.lang, '')
        if desc:
            st.markdown(desc)
        st.markdown(f"**{t('time_required')}:** {item.get('time_required','N/A')}")
        st.markdown(f"**{t('cost')}:** ¥{item.get('price',0)}")
        # show map button for Nijigen no Mori
        if item.get('name',{}).get('EN','').lower() == "nijigen no mori":
            if st.button(t('view_map')):
                st.session_state.show_nijigen_map = True
        if st.session_state.get('show_nijigen_map'):
            lat = item.get('lat')
            lon = item.get('lon')
            map_url = f"https://www.google.com/maps?q={lat},{lon}&z=15&output=embed"
            st.components.v1.iframe(map_url, width=700, height=500)
            if st.button(t('close_map')):
                st.session_state.show_nijigen_map = False
        st.markdown(f"**{t('schedule')}**")
        st.markdown(f"**{t('customize_itinerary')}**")
        st.markdown("**Recommended Points:**")
        for p in item.get("points",{}).get(st.session_state.lang, item.get("points",[])):
            st.markdown(f"- {p}")
    if st.button(t('back_to_itinerary')):
        st.session_state.page = "main"
        st.session_state.show_nijigen_map = False
        st.rerun()  # immediately refresh to show main page


    # stop further rendering
    st.stop()
else:
    tab1, tab2 = st.tabs([t('tab_itinerary'), t('tab_chat')])

# =====================================
# Tab1: Itinerary creation - 3 personalized plans
# =====================================
if st.session_state.page != "detail":
    with tab1:
        st.markdown('<a id="plans"></a>', unsafe_allow_html=True)
        st.subheader(f"🎯 {t('generate_itinerary')}")
        st.markdown("Choose plans comparing 3 different themes")

        # Generate plans when button is clicked
        if gen_button:
            with st.spinner(t('generating')):
                plans = generate_plans(int(age), gender, purpose, int(num_days))
                st.session_state.plans_generated = True
                st.session_state.current_plans = plans

        # Display 3 plans in tabs if generated
        if st.session_state.get("plans_generated") and st.session_state.get("current_plans"):
            plans = st.session_state.current_plans
            
            # Display recommended model course at the top
            if plans and len(plans) > 0:
                first_plan = plans[0]
                course_name = (first_plan.get("model_course_name_ja") 
                              if st.session_state.lang == "JA" 
                              else first_plan.get("model_course_name_en", "Recommended Course"))
                st.info(f"💡 {t('recommended_course')}: **{course_name}**")
            
            # Map theme names to translation keys
            theme_to_key = {
                "Standard": "plan_standard",
                "Relaxing": "plan_relaxing",
                "Active": "plan_active"
            }
            plan_titles = [t(theme_to_key.get(p['theme'], 'plan_standard')) for p in plans]
            plan_tabs = st.tabs(plan_titles)
            
            for plan_idx, (ptab, plan) in enumerate(zip(plan_tabs, plans)):
                with ptab:
                    # 3-column layout: Activity | Restaurant | Hotel
                    col1, col2, col3 = st.columns(3)
                    
                    # Activity
                    with col1:
                        st.markdown("## 🎪 " + t('activity'))
                        act = plan['activity']
                        act_name = act['name'].get(st.session_state.lang, next(iter(act['name'].values())))
                        st.markdown(f"**{act_name}**")
                        st.markdown(f"💰 ¥{act['price']:,}")
                        st.markdown(f"⏱️ {act['time_required_hours']}h")
                        desc = act.get('description', {}).get(st.session_state.lang, '')
                        if desc:
                            st.markdown(f"_{desc}_")
                        if st.button(t('view_details'), key=f"detail_act_{plan_idx}"):
                            st.session_state.page = "detail"
                            st.session_state.detail_item = act
                            st.session_state.detail_type = "activity"
                            st.session_state.show_nijigen_map = False
                            st.rerun()


                    
                    # Restaurant
                    with col2:
                        st.markdown("## 🍴 " + t('restaurant'))
                        rst = plan['restaurant']
                        rst_name = rst['name'].get(st.session_state.lang, next(iter(rst['name'].values())))
                        st.markdown(f"**{rst_name}**")
                        st.markdown(f"💰 ¥{rst['price']:,}")
                        st.markdown(f"⏱️ {rst['time_required_hours']}h")
                        desc = rst.get('description', {}).get(st.session_state.lang, '')
                        if desc:
                            st.markdown(f"_{desc}_")
                        if st.button(t('view_details'), key=f"detail_rst_{plan_idx}"):
                            st.session_state.page = "detail"
                            st.session_state.detail_item = rst
                            st.session_state.detail_type = "restaurant"
                            st.session_state.show_nijigen_map = False
                            st.rerun()


                    
                    # Hotel
                    with col3:
                        st.markdown("## 🏨 " + t('hotel'))
                        htl = plan['hotel']
                        htl_name = htl['name'].get(st.session_state.lang, next(iter(htl['name'].values())))
                        st.markdown(f"**{htl_name}**")
                        st.markdown(f"💰 ¥{htl['price']:,}")
                        st.markdown(f"🌜 {plan['num_days']} day(s)")
                        desc = htl.get('description', {}).get(st.session_state.lang, '')
                        if desc:
                            st.markdown(f"_{desc}_")
                        if st.button(t('view_details'), key=f"detail_htl_{plan_idx}"):
                            st.session_state.page = "detail"
                            st.session_state.detail_item = htl
                            st.session_state.detail_type = "hotel"
                            st.session_state.show_nijigen_map = False
                            st.rerun()


                    
                    # Timeline Schedule section
                    st.divider()
                    st.markdown("### 🕒 Detailed Timeline")
                    
                    for event in plan.get('timeline', []):
                        # Determine icon based on type
                        icon_map = {
                            "activity": "🎪",
                            "restaurant": "🍴",
                            "shuttle": "🚌",
                            "hotel": "🏨"
                        }
                        icon = icon_map.get(event['type'], "📍")
                        
                        # Get display name (handle bilingual names)
                        event_name = event['name']
                        if isinstance(event_name, dict):
                            event_name = event_name.get(st.session_state.lang, event_name.get('EN', 'Unknown'))
                        
                        # Format time display
                        if event['end']:
                            time_display = f"{event['start']} - {event['end']}"
                        else:  # Hotel check-in only
                            time_display = f"{event['start']} -"
                        
                        st.markdown(f"**{icon} {time_display}** {event_name}")
                    
                    # Total cost
                    st.divider()
                    st.markdown(f"### 💰 Total Cost: ¥{plan['total_cost']:,}")
        else:
            st.info("プロフィールを入力して「プランを生成」をクリックしてください")


# =====================================
# タブ2：AIスタッフQ&A
# =====================================
with tab2:
    st.markdown('<a id="chat"></a>', unsafe_allow_html=True)
    st.subheader(t('ai_chat_header'))
    st.markdown("")  # description could be empty or localized

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 履歴描画
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    user_input = st.chat_input(t('ask_anything'))
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_reply = get_ai_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# ボトムナビゲーション描画
render_bottom_navigation()

# 下部パディング
st.markdown('<div class="bottom-padding"></div>', unsafe_allow_html=True)

# フッター
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    {t('footer')}
</div>
""", unsafe_allow_html=True)
