import streamlit as st
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Car Sharing Dashboard",
    page_icon="🚗",
    layout="wide",
)

# ── Futuristic CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
    --bg:        #050810;
    --surface:   #0d1117;
    --border:    #1a2535;
    --neon-cyan: #00f5ff;
    --neon-pink: #ff006e;
    --neon-lime: #b8ff00;
    --neon-violet:#9b5de5;
    --text:      #c9d6e3;
    --muted:     #4a5568;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.08em;
}

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--neon-cyan);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.7rem; letter-spacing: 0.15em; }
[data-testid="stMetricValue"] { color: var(--neon-cyan) !important; font-family: 'Orbitron', monospace !important; }

[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; }

.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--muted);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    trips  = pd.read_csv("datasets/trips.csv")
    cars   = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

# ── Merge ─────────────────────────────────────────────────────────────────────
trips_merged = trips.merge(cars,   left_on="car_id",  right_on="id",      suffixes=("", "_car"))
trips_merged = trips_merged.merge(cities, on="city_id", suffixes=("", "_city"))

# ── Drop id columns ───────────────────────────────────────────────────────────
drop_cols = [c for c in ["id_car", "city_id", "id_customer", "id"] if c in trips_merged.columns]
trips_merged = trips_merged.drop(columns=drop_cols)

# ── Date formatting ───────────────────────────────────────────────────────────
trips_merged['pickup_date'] = pd.to_datetime(trips_merged['pickup_time']).dt.date

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🔭 FILTERS")
brand_col = 'brand' if 'brand' in trips_merged.columns else trips_merged.columns[0]
all_brands = sorted(trips_merged[brand_col].unique())
cars_brand = st.sidebar.multiselect("Select Car Brand", all_brands, default=all_brands)

if cars_brand:
    trips_merged = trips_merged[trips_merged[brand_col].isin(cars_brand)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🚗 CAR SHARING DASHBOARD")
st.markdown('<p style="color:#4a5568;font-size:0.75rem;letter-spacing:0.2em">REAL-TIME ANALYTICS INTERFACE</p>', unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
price_col    = 'price'    if 'price'    in trips_merged.columns else None
distance_col = 'distance' if 'distance' in trips_merged.columns else None
model_col    = 'model'    if 'model'    in trips_merged.columns else brand_col

total_trips    = len(trips_merged)
total_distance = trips_merged[distance_col].sum() if distance_col else 0
top_car        = trips_merged.groupby(model_col)[price_col].sum().idxmax() if price_col else "N/A"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Trips", f"{total_trips:,}")
with col2:
    st.metric("Top Car by Revenue", top_car)
with col3:
    st.metric("Total Distance (km)", f"{total_distance:,.0f}")

# ── Chart helpers ─────────────────────────────────────────────────────────────
def section(title):
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)

# ── 1. Trips Over Time ────────────────────────────────────────────────────────
section("01 — TRIPS OVER TIME")
trips_by_date = (
    trips_merged.groupby('pickup_date')
    .size()
    .reset_index(name='trips')
    .set_index('pickup_date')
)
st.line_chart(trips_by_date, color="#00f5ff", height=220)

# ── 2. Revenue per Car Model ──────────────────────────────────────────────────
if price_col:
    section("02 — REVENUE PER CAR MODEL")
    rev_by_model = (
        trips_merged.groupby(model_col)[price_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .set_index(model_col)
    )
    st.bar_chart(rev_by_model, color="#ff006e", height=280)

# ── 3. Number of Trips per Car Model ─────────────────────────────────────────
section("03 — TRIPS PER CAR MODEL")
trips_by_model = (
    trips_merged.groupby(model_col)
    .size()
    .sort_values(ascending=False)
    .reset_index(name='trips')
    .set_index(model_col)
)
st.bar_chart(trips_by_model, color="#b8ff00", height=280)

# ── 4. Revenue by City ────────────────────────────────────────────────────────
city_col = 'city_name' if 'city_name' in trips_merged.columns else None
if price_col and city_col:
    section("04 — REVENUE BY CITY")
    rev_by_city = (
        trips_merged.groupby(city_col)[price_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .set_index(city_col)
    )
    st.bar_chart(rev_by_city, color="#9b5de5", height=260)

# ── 5. Cumulative Revenue Over Time ──────────────────────────────────────────
if price_col:
    section("05 — CUMULATIVE REVENUE GROWTH")
    cumrev = (
        trips_merged.groupby('pickup_date')[price_col]
        .sum()
        .cumsum()
        .reset_index()
        .set_index('pickup_date')
    )
    st.area_chart(cumrev, color="#ff006e", height=220)

# ── Dataframe preview ─────────────────────────────────────────────────────────
section("DATA PREVIEW")
st.write(trips_merged.head(10))
