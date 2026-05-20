import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Load Data ─────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('olist_master_cleaned.csv')
    return df

df = load_data()

# ── Title ─────────────────────────────────────
st.title("🛒 E-Commerce Sales Dashboard")
st.markdown("**Analyzing 110,000+ real Brazilian e-commerce orders**")
st.divider()

# ── Sidebar Filters ───────────────────────────
st.sidebar.header("🔍 Filters")

year = st.sidebar.multiselect(
    "Select Year",
    options=df['order_year'].unique(),
    default=df['order_year'].unique()
)

state = st.sidebar.multiselect(
    "Select State",
    options=sorted(df['state'].dropna().unique()),
    default=sorted(df['state'].dropna().unique())
)

df_filtered = df[
    (df['order_year'].isin(year)) &
    (df['state'].isin(state))
]

# ── KPI Cards ─────────────────────────────────
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue",
              f"R$ {df_filtered['revenue'].sum():,.0f}")
with col2:
    st.metric("📦 Total Orders",
              f"{df_filtered['order_id'].nunique():,}")
with col3:
    st.metric("🚚 Avg Delivery Days",
              f"{df_filtered['delivery_days'].mean():.1f} days")
with col4:
    top_state = df_filtered.groupby('state')['revenue'].sum().idxmax()
    st.metric("🏆 Top State", top_state)

st.divider()

# ── Row 1 ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly = df_filtered.groupby(
        ['order_year','order_month'])['revenue'].sum().reset_index()
    monthly['period'] = monthly['order_year'].astype(str) + '-' + \
                        monthly['order_month'].astype(str).str.zfill(2)
    fig1 = px.line(monthly, x='period', y='revenue',
                   color='order_year',
                   labels={'revenue':'Revenue (BRL)','period':'Month'})
    fig1.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏙️ Top 10 States by Revenue")
    top_states = df_filtered.groupby('state')['revenue'] \
                            .sum().sort_values(ascending=False) \
                            .head(10).reset_index()
    fig2 = px.bar(top_states, x='revenue', y='state',
                  orientation='h',
                  color='revenue',
                  color_continuous_scale='Blues',
                  labels={'revenue':'Revenue (BRL)','state':'State'})
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Row 2 ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Revenue by Payment Type")
    pay = df_filtered.groupby('payment_type')['revenue'].sum().reset_index()
    fig3 = px.pie(pay, values='revenue', names='payment_type',
                  hole=0.4,
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📅 Orders by Day of Week")
    day_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    day = df_filtered.groupby('order_day')['order_id'] \
                     .nunique().reindex(day_order).reset_index()
    day.columns = ['day','orders']
    fig4 = px.bar(day, x='day', y='orders',
                  color='orders',
                  color_continuous_scale='Blues',
                  labels={'orders':'Total Orders','day':'Day'})
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Row 3 ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚚 Avg Delivery Days by State")
    delivery = df_filtered.groupby('state')['delivery_days'] \
                          .mean().sort_values() \
                          .head(10).reset_index()
    fig5 = px.bar(delivery, x='delivery_days', y='state',
                  orientation='h',
                  color='delivery_days',
                  color_continuous_scale='RdYlGn_r',
                  labels={'delivery_days':'Avg Days','state':'State'})
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("🏙️ Top 10 Cities by Revenue")
    cities = df_filtered.groupby('city')['revenue'] \
                        .sum().sort_values(ascending=False) \
                        .head(10).reset_index()
    fig6 = px.bar(cities, x='revenue', y='city',
                  orientation='h',
                  color='revenue',
                  color_continuous_scale='Blues',
                  labels={'revenue':'Revenue (BRL)','city':'City'})
    fig6.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ── Key Insights ──────────────────────────────
st.subheader("💡 Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.success("📈 Revenue grew **8x** from 2016 to 2018")
    st.success("🏙️ São Paulo drives **40%** of total revenue")
    st.success("💳 Credit card used in **66%** of all orders")

with col2:
    st.info("📅 Tuesday is the **highest revenue** day")
    st.info("🚚 Average delivery time is **12 days**")
    st.info("👤 Top customer spent **R$1,09,312** in one order")

st.divider()
st.markdown("**Made by Shreya Thakre** | "
            "Data Source: Olist Brazilian E-Commerce Dataset")