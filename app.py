import math
import time
from datetime import datetime, timedelta

import streamlit as st


st.set_page_config(
    page_title="Awaji Island Travel Planner",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


LANG = {
    "JA": {
        "title": "淡路島観光アプリ",
        "subtitle": "あなたに最適な1つのモデルコースを提案します",
        "language": "言語",
        "age": "年齢",
        "gender": "性別",
        "purpose": "旅行の目的",
        "days": "滞在日数",
        "generate": "モデルコースを生成",
        "male": "男性",
        "female": "女性",
        "other": "その他",
        "no_answer": "回答しない",
        "solo": "一人旅",
        "couple": "カップル",
        "family": "家族",
        "friends": "友達",
        "tab_itinerary": "🛠️ 旅程作成",
        "tab_chat": "💬 AIチャット",
        "tab_benefits": "🎁 ポイント特典",
        "recommended": "提案されたモデルコース",
        "timeline": "縦型タイムライン",
        "total_cost": "合計費用",
        "editor": "旅程編集パネル",
        "order": "順番",
        "name": "施設名",
        "category": "カテゴリ",
        "move_up": "↑",
        "move_down": "↓",
        "remove": "削除",
        "add_facility": "施設を追加",
        "add": "追加",
        "add_target": "追加する施設",
        "shuttle": "シャトルバス移動",
        "wait_shuttle": "シャトルバス待機",
        "cat_activity": "アクティビティ",
        "cat_restaurant": "レストラン",
        "cat_hotel": "ホテル",
        "cat_move": "移動",
        "empty": "まず「モデルコースを生成」を押してください。",
        "map_notice": "ニジゲンノモリが旅程に含まれています。園内マップを表示します。",
        "map_url_label": "園内マップURL",
        "chat_help": "旅行に関する質問を入力してください",
        "chat_placeholder": "例: おすすめのランチは？",
        "thinking": "回答を考えています...",
        "benefit_1": "淡路島西海岸アプリ連携：ポイント10%進呈",
        "benefit_2": "会員限定：フレンチの森 冬の特別宿泊優待",
        "benefit_3": "会員証バーコードを表示する",
    },
    "EN": {
        "title": "Awaji Island Tourism App",
        "subtitle": "We suggest one best-fit model course for you",
        "language": "Language",
        "age": "Age",
        "gender": "Gender",
        "purpose": "Travel Purpose",
        "days": "Trip Duration (days)",
        "generate": "Generate Model Course",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "no_answer": "Prefer not to say",
        "solo": "Solo",
        "couple": "Couple",
        "family": "Family",
        "friends": "Friends",
        "tab_itinerary": "🛠️ Itinerary Builder",
        "tab_chat": "💬 AI Chat",
        "tab_benefits": "🎁 Point Benefits",
        "recommended": "Recommended Model Course",
        "timeline": "Vertical Timeline",
        "total_cost": "Total Cost",
        "editor": "Itinerary Edit Panel",
        "order": "Order",
        "name": "Name",
        "category": "Category",
        "move_up": "↑",
        "move_down": "↓",
        "remove": "Remove",
        "add_facility": "Add Facility",
        "add": "Add",
        "add_target": "Facility to add",
        "shuttle": "Shuttle Bus",
        "wait_shuttle": "Wait for Shuttle",
        "cat_activity": "Activity",
        "cat_restaurant": "Restaurant",
        "cat_hotel": "Hotel",
        "cat_move": "Move",
        "empty": "Click 'Generate Model Course' first.",
        "map_notice": "Nijigen no Mori is included in your itinerary. Park map is shown below.",
        "map_url_label": "Park map URL",
        "chat_help": "Ask questions about your trip",
        "chat_placeholder": "e.g. What lunch do you recommend?",
        "thinking": "Thinking...",
        "benefit_1": "Awaji West Coast App Link: 10% point bonus",
        "benefit_2": "Members Only: French no Mori winter special stay offer",
        "benefit_3": "Show member barcode",
    },
}


FACILITIES = [
    {
        "id": "act_nijigen",
        "category": "activity",
        "name": {"JA": "ニジゲンノモリ", "EN": "Nijigen no Mori"},
        "price": 2500,
        "lat": 34.5562,
        "lon": 134.8117,
        "time_required_hours": 3.0,
    },
    {
        "id": "act_zenbo",
        "category": "activity",
        "name": {"JA": "禅坊 靖寧", "EN": "Zenbo Seinei"},
        "price": 8000,
        "lat": 34.5740,
        "lon": 134.7712,
        "time_required_hours": 2.0,
    },
    {
        "id": "act_yumebutai",
        "category": "activity",
        "name": {"JA": "淡路夢舞台", "EN": "Awaji Yumebutai"},
        "price": 0,
        "lat": 34.5475,
        "lon": 134.7972,
        "time_required_hours": 1.5,
    },
    {
        "id": "rst_seafood",
        "category": "restaurant",
        "name": {"JA": "淡路鮮魚", "EN": "Fresh Awaji Seafood"},
        "price": 3000,
        "lat": 34.5678,
        "lon": 134.7988,
        "time_required_hours": 1.0,
    },
    {
        "id": "rst_udon",
        "category": "restaurant",
        "name": {"JA": "かわにしうどん", "EN": "Kawanishi Udon"},
        "price": 1200,
        "lat": 34.5510,
        "lon": 134.8101,
        "time_required_hours": 1.0,
    },
    {
        "id": "rst_bbq",
        "category": "restaurant",
        "name": {"JA": "海鮮バーベキュー", "EN": "Seafood BBQ"},
        "price": 3800,
        "lat": 34.5607,
        "lon": 134.8053,
        "time_required_hours": 1.5,
    },
    {
        "id": "rst_cafe",
        "category": "restaurant",
        "name": {"JA": "海辺のカフェ", "EN": "Seaside Cafe"},
        "price": 1800,
        "lat": 34.5489,
        "lon": 134.7924,
        "time_required_hours": 1.0,
    },
    {
        "id": "htl_grandview",
        "category": "hotel",
        "name": {"JA": "淡路リゾートグランビュー", "EN": "Awaji Resort Grandview"},
        "price": 15000,
        "lat": 34.5633,
        "lon": 134.8031,
        "time_required_hours": 0.0,
    },
    {
        "id": "htl_budget",
        "category": "hotel",
        "name": {"JA": "ビジェットイン淡路", "EN": "Budget Inn Awaji"},
        "price": 6000,
        "lat": 34.5702,
        "lon": 134.7905,
        "time_required_hours": 0.0,
    },
    {
        "id": "htl_glamping",
        "category": "hotel",
        "name": {"JA": "グランピングリゾート", "EN": "Glamping Resort"},
        "price": 18000,
        "lat": 34.5551,
        "lon": 134.7868,
        "time_required_hours": 0.0,
    },
    {
        "id": "htl_ryokan",
        "category": "hotel",
        "name": {"JA": "伝統的な温泉旅館", "EN": "Traditional Hot Spring Ryokan"},
        "price": 22000,
        "lat": 34.5784,
        "lon": 134.7993,
        "time_required_hours": 0.0,
    },
]


def tr(key: str) -> str:
    lang = st.session_state.get("lang", "JA")
    return LANG.get(lang, LANG["JA"]).get(key, key)


def display_name(item: dict) -> str:
    lang = st.session_state.get("lang", "JA")
    return item["name"].get(lang, item["name"]["EN"])


def category_label(category_code: str) -> str:
    key_map = {
        "activity": "cat_activity",
        "restaurant": "cat_restaurant",
        "hotel": "cat_hotel",
        "move": "cat_move",
    }
    return tr(key_map.get(category_code, "cat_move"))


def event_icon(event_type: str) -> str:
    icon_map = {
        "activity": "🎪",
        "restaurant": "🍽️",
        "hotel": "🏨",
        "wait": "⏳",
        "shuttle": "🚌",
    }
    return icon_map.get(event_type, "📍")


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def nearest_order(items: list[dict]) -> list[dict]:
    if len(items) <= 2:
        return items.copy()

    remaining = items.copy()
    ordered = [remaining.pop(0)]

    while remaining:
        last = ordered[-1]
        next_index = min(
            range(len(remaining)),
            key=lambda i: haversine_distance(
                last["lat"],
                last["lon"],
                remaining[i]["lat"],
                remaining[i]["lon"],
            ),
        )
        ordered.append(remaining.pop(next_index))

    return ordered


def align_to_next_30min(current: datetime) -> datetime:
    if current.minute % 30 == 0 and current.second == 0 and current.microsecond == 0:
        return current

    if current.minute < 30:
        return current.replace(minute=30, second=0, microsecond=0)

    return (current + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)


def determine_model_course(age: int, gender: str, purpose: str, num_days: int) -> str:
    if purpose == "family" or age < 15:
        return "family"
    if purpose == "couple":
        return "couple"
    if gender == "female" and purpose == "friends":
        return "friends"
    if purpose == "solo" and num_days >= 3:
        return "luxury"
    return "standard"


def create_initial_itinerary(age: int, gender: str, purpose: str, num_days: int) -> list[dict]:
    course = determine_model_course(age, gender, purpose, num_days)

    if course == "family":
        selected_ids = ["act_nijigen", "rst_bbq", "htl_glamping"]
    elif course == "couple":
        selected_ids = ["act_yumebutai", "rst_cafe", "htl_ryokan"]
    elif course == "friends":
        selected_ids = ["act_nijigen", "rst_cafe", "htl_budget"]
    elif course == "luxury":
        selected_ids = ["act_zenbo", "rst_seafood", "htl_ryokan"]
    else:
        selected_ids = ["act_yumebutai", "rst_udon", "htl_grandview"]

    selected = [next(item for item in FACILITIES if item["id"] == fid) for fid in selected_ids]

    activities = [item for item in selected if item["category"] == "activity"]
    restaurants = [item for item in selected if item["category"] == "restaurant"]
    hotels = [item for item in selected if item["category"] == "hotel"]

    return nearest_order(activities) + nearest_order(restaurants) + nearest_order(hotels)


def calculate_schedule_from_itinerary(itinerary: list[dict]) -> tuple[list[dict], int]:
    if not itinerary:
        return [], 0

    events = []
    total_cost = 0
    current_time = datetime(2026, 1, 1, 9, 0)
    shuttle_travel_minutes = 30

    for idx, place in enumerate(itinerary):
        stay_minutes = int(place["time_required_hours"] * 60)
        end_time = current_time + timedelta(minutes=stay_minutes)

        events.append(
            {
                "start": current_time,
                "end": end_time,
                "title": display_name(place),
                "type": place["category"],
                "category": category_label(place["category"]),
            }
        )

        total_cost += int(place["price"])
        current_time = end_time

        if idx < len(itinerary) - 1:
            next_departure = align_to_next_30min(current_time)
            if next_departure > current_time:
                events.append(
                    {
                        "start": current_time,
                        "end": next_departure,
                        "title": tr("wait_shuttle"),
                        "type": "wait",
                        "category": category_label("move"),
                    }
                )

            shuttle_arrival = next_departure + timedelta(minutes=shuttle_travel_minutes)
            events.append(
                {
                    "start": next_departure,
                    "end": shuttle_arrival,
                    "title": tr("shuttle"),
                    "type": "shuttle",
                    "category": category_label("move"),
                }
            )
            current_time = shuttle_arrival

    return events, total_cost


def get_mock_ai_response(user_message: str, lang: str) -> str:
    msg = user_message.lower().strip()

    if lang == "JA":
        if "ランチ" in msg or "昼" in msg:
            return "淡路島バーガーや新鮮な海鮮BBQがおすすめです。海沿いにはおしゃれなカフェもありますよ！"
        if "雨" in msg:
            return "屋内施設のHELLO KITTY SMILEや、屋根付きの施設がおすすめです。"
        if "シャトル" in msg or "バス" in msg:
            return "シャトルバスは各施設を約30分間隔で運行しています。スケジュールタブから旅程に合わせて確認できます。"
        return "ご質問ありがとうございます！詳細については現在学習中ですが、淡路島の西海岸エリアは夕日がとても綺麗でおすすめです！"

    if "lunch" in msg:
        return "Awaji burgers and fresh seafood BBQ are highly recommended. You can also enjoy stylish seaside cafes!"
    if "rain" in msg:
        return "Indoor spots like HELLO KITTY SMILE and covered facilities are great on rainy days."
    if "shuttle" in msg or "bus" in msg:
        return "Shuttle buses run about every 30 minutes between facilities. You can check it with your schedule on the itinerary tab."
    return "Thank you for your question! We are still learning details, but Awaji’s west coast area is highly recommended for beautiful sunsets."


# ===== itinerary operations =====
def move_item_up(index: int) -> None:
    itinerary = st.session_state.custom_itinerary
    if 0 < index < len(itinerary):
        itinerary[index - 1], itinerary[index] = itinerary[index], itinerary[index - 1]


def move_item_down(index: int) -> None:
    itinerary = st.session_state.custom_itinerary
    if 0 <= index < len(itinerary) - 1:
        itinerary[index + 1], itinerary[index] = itinerary[index], itinerary[index + 1]


def remove_item(index: int) -> None:
    itinerary = st.session_state.custom_itinerary
    if 0 <= index < len(itinerary):
        itinerary.pop(index)


def add_item_by_id(facility_id: str) -> None:
    item = next((f for f in FACILITIES if f["id"] == facility_id), None)
    if item:
        st.session_state.custom_itinerary.append(item)


# ===== UI drawing =====
def draw_vertical_timeline(events: list[dict]) -> None:
    st.markdown(
        """
        <style>
        .vt-wrap { position: relative; margin-left: 6px; }
        .vt-item { position: relative; padding-left: 54px; padding-bottom: 18px; }
        .vt-item:last-child { padding-bottom: 4px; }
        .vt-item::before {
            content: '';
            position: absolute;
            left: 17px;
            top: 0;
            bottom: -6px;
            width: 2px;
            background: #d9d9d9;
        }
        .vt-dot {
            position: absolute;
            left: 6px;
            top: 2px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #ffffff;
            border: 2px solid #2a9fa9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            z-index: 2;
        }
        .vt-card {
            border: 1px solid #e7e7e7;
            border-radius: 12px;
            padding: 10px 12px;
            background: #ffffff;
        }
        .vt-time {
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }
        .vt-title {
            font-weight: 600;
            margin-bottom: 2px;
        }
        .vt-cat {
            font-size: 12px;
            color: #2a9fa9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html_parts = ["<div class='vt-wrap'>"]
    for event in events:
        start = event["start"].strftime("%H:%M")
        end = event["end"].strftime("%H:%M")
        icon = event_icon(event["type"])

        html_parts.append(
            f"""
            <div class='vt-item'>
                <div class='vt-dot'>{icon}</div>
                <div class='vt-card'>
                    <div class='vt-time'>{start} - {end}</div>
                    <div class='vt-title'>{event['title']}</div>
                    <div class='vt-cat'>{event['category']}</div>
                </div>
            </div>
            """
        )
    html_parts.append("</div>")

    st.markdown("".join(html_parts), unsafe_allow_html=True)


def draw_timeline_and_summary() -> None:
    events, base_cost = calculate_schedule_from_itinerary(st.session_state.custom_itinerary)
    total_cost = base_cost * int(st.session_state.num_days)

    st.metric(tr("total_cost"), f"¥{total_cost:,}")

    st.subheader(tr("timeline"))
    if events:
        draw_vertical_timeline(events)

    contains_nijigen = any(item["name"]["EN"] == "Nijigen no Mori" for item in st.session_state.custom_itinerary)
    if contains_nijigen:
        st.success(tr("map_notice"))
        st.markdown(f"**{tr('map_url_label')}:** [https://map.nijigennomori.com/](https://map.nijigennomori.com/)")
        st.components.v1.iframe("https://map.nijigennomori.com/", width=700, height=500)


def draw_editor_panel() -> None:
    st.subheader(tr("editor"))

    if st.session_state.custom_itinerary:
        header_cols = st.columns([1, 4, 2, 1, 1, 1])
        header_cols[0].write(f"**{tr('order')}**")
        header_cols[1].write(f"**{tr('name')}**")
        header_cols[2].write(f"**{tr('category')}**")

        for idx, item in enumerate(st.session_state.custom_itinerary):
            row_cols = st.columns([1, 4, 2, 1, 1, 1])
            row_cols[0].write(str(idx + 1))
            row_cols[1].write(display_name(item))
            row_cols[2].write(category_label(item["category"]))

            if row_cols[3].button(tr("move_up"), key=f"up_{idx}"):
                move_item_up(idx)
                st.rerun()

            if row_cols[4].button(tr("move_down"), key=f"down_{idx}"):
                move_item_down(idx)
                st.rerun()

            if row_cols[5].button(tr("remove"), key=f"remove_{idx}"):
                remove_item(idx)
                st.rerun()

    st.markdown("---")
    st.write(f"**{tr('add_facility')}**")

    option_map = {f"{display_name(item)} ({category_label(item['category'])})": item["id"] for item in FACILITIES}
    option_label = st.selectbox(tr("add_target"), list(option_map.keys()), key="add_select")

    if st.button(tr("add"), key="add_button"):
        add_item_by_id(option_map[option_label])
        st.rerun()


def draw_benefits_tab() -> None:
    st.info(f"🎉 {tr('benefit_1')}")
    st.info(f"🏨 {tr('benefit_2')}")

    st.markdown(
        """
        <div style='border:1px solid #e5e5e5; border-radius:12px; padding:14px; background:#fff;'>
            <div style='font-weight:600; margin-bottom:6px;'>
                Member Benefit
            </div>
            <div style='font-size:13px; color:#666;'>
                Barcode mock action
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button(tr("benefit_3"), type="primary")


# ===== session state =====
if "lang" not in st.session_state:
    st.session_state.lang = "JA"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "custom_itinerary" not in st.session_state:
    st.session_state.custom_itinerary = []
if "num_days" not in st.session_state:
    st.session_state.num_days = 1


# ===== header =====
icon_col, title_col = st.columns([1, 9])
with icon_col:
    st.image("mascot.png", width=70)
with title_col:
    st.title(f"🏝️ {tr('title')}")
    st.caption(tr("subtitle"))


# ===== profile controls =====
ctrl_cols = st.columns([1, 1, 1, 1, 1, 1.2])

with ctrl_cols[0]:
    st.selectbox(tr("language"), ["JA", "EN"], key="lang")

with ctrl_cols[1]:
    age = st.number_input(tr("age"), min_value=0, max_value=120, value=25, step=1)

with ctrl_cols[2]:
    gender = st.selectbox(
        tr("gender"),
        ["male", "female", "other", "no_answer"],
        format_func=tr,
    )

with ctrl_cols[3]:
    purpose = st.selectbox(
        tr("purpose"),
        ["solo", "couple", "family", "friends"],
        format_func=tr,
    )

with ctrl_cols[4]:
    num_days = st.number_input(tr("days"), min_value=1, max_value=10, value=int(st.session_state.num_days), step=1)
    st.session_state.num_days = int(num_days)

with ctrl_cols[5]:
    generate_clicked = st.button(tr("generate"), width="stretch")


if generate_clicked:
    st.session_state.custom_itinerary = create_initial_itinerary(int(age), gender, purpose, int(num_days))


tab_itinerary, tab_chat, tab_benefits = st.tabs([tr("tab_itinerary"), tr("tab_chat"), tr("tab_benefits")])

with tab_itinerary:
    st.subheader(tr("recommended"))
    if not st.session_state.custom_itinerary:
        st.info(tr("empty"))
    else:
        left_col, right_col = st.columns([1.1, 1])
        with left_col:
            draw_timeline_and_summary()
        with right_col:
            draw_editor_panel()

with tab_chat:
    st.caption(tr("chat_help"))
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)

    user_msg = st.chat_input(tr("chat_placeholder"))
    if user_msg:
        st.session_state.chat_history.append(("user", user_msg))
        with st.spinner(tr("thinking")):
            time.sleep(1.5)
            reply = get_mock_ai_response(user_msg, st.session_state.lang)
        st.session_state.chat_history.append(("assistant", reply))
        st.rerun()

with tab_benefits:
    draw_benefits_tab()
