import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Funnel Analysis", layout="wide")

st.title("🛒 E-commerce Funnel Analysis Dashboard")
st.caption("Source: REES46 E-commerce Dataset · 885K events · Sample of 20K used for performance")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw and cleaned data/funnel_clean.csv")
    df['event_time'] = pd.to_datetime(df['event_time'], utc=True)
    df['hour'] = df['event_time'].dt.hour
    df['day'] = pd.Categorical(
        df['event_time'].dt.day_name(),
        categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
        ordered=True
    )
    return df

df = load_data()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("🔍 Filters")

categories = sorted(df['category_code'].dropna().unique())
selected_category = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

hour_range = st.sidebar.slider(
    "Select Hour Range",
    0, 23, (0, 23)
)

# Apply filters
df = df[
    (df['category_code'].isin(selected_category)) &
    (df['hour'] >= hour_range[0]) &
    (df['hour'] <= hour_range[1])
]

# -------------------- USER-LEVEL FUNNEL METRICS --------------------
# Use user-level (did user X perform this action?) — consistent with notebook
funnel = df.pivot_table(
    index='user_id',
    columns='event_type',
    aggfunc='size',
    fill_value=0
)
funnel = funnel.map(lambda x: 1 if x > 0 else 0)
for col in ['view', 'cart', 'purchase']:
    if col not in funnel.columns:
        funnel[col] = 0

views     = int(funnel['view'].sum())
carts     = int(funnel['cart'].sum())
purchases = int(funnel['purchase'].sum())

view_to_cart     = carts / views if views else 0
cart_to_purchase = purchases / carts if carts else 0

# AOV from actual purchase events in filtered data
purchase_events = df[df['event_type'] == 'purchase']
aov = purchase_events['price'].mean() if len(purchase_events) > 0 else 135.28

# -------------------- KPI SECTION --------------------
st.markdown("### 📊 Funnel Overview")
st.caption("Metrics are user-level: each user counted once per stage regardless of how many times they acted.")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Users Viewed",    f"{views:,}")
col2.metric("Users Carted",    f"{carts:,}")
col3.metric("Users Purchased", f"{purchases:,}")
col4.metric("View → Cart",     f"{view_to_cart:.1%}")
col5.metric("Cart → Purchase", f"{cart_to_purchase:.1%}")

# -------------------- FUNNEL CHART --------------------
funnel_df = pd.DataFrame({
    "Stage": ["View", "Add to Cart", "Purchase"],
    "Users": [views, carts, purchases]
})

fig = px.funnel(funnel_df, x="Users", y="Stage", title="User Conversion Funnel")
fig.update_layout(font=dict(size=14))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------- DYNAMIC INSIGHTS --------------------
st.markdown("### 🧠 Insights")

if view_to_cart < 0.1:
    st.warning("⚠️ Low View → Cart conversion. Users are browsing but not engaging with products. Focus on product page quality, trust signals, and pricing.")

if cart_to_purchase > 0.5:
    st.success("✅ Strong Cart → Purchase conversion. Checkout process is efficient — optimisation effort is better spent earlier in the funnel.")

if 12 >= hour_range[0] and 17 <= hour_range[1]:
    st.info("📌 Peak traffic occurs between 12 PM – 5 PM. However, conversion does not spike proportionally — users are in browsing mode. Consider targeted promotions during high-intent hours.")

st.divider()

# -------------------- CATEGORY ANALYSIS --------------------
st.markdown("### 📦 Category Performance")

category = df.groupby(['category_code', 'event_type']).size().unstack(fill_value=0)
for col in ['view', 'cart', 'purchase']:
    if col not in category.columns:
        category[col] = 0

category['conversion'] = (category['purchase'] / category['view']).round(4)

# Category revenue from actual purchase prices
cat_revenue = df[df['event_type'] == 'purchase'].groupby('category_code')['price'].sum().round(2)
category = category.join(cat_revenue.rename('revenue'), how='left').fillna(0)
category = category.sort_values('conversion', ascending=False)

top_cat   = category.head(10).reset_index()
worst_cat = category.tail(10).reset_index()

col1, col2 = st.columns(2)

with col1:
    fig2 = px.bar(top_cat, x='category_code', y='conversion',
                  title="Top 10 Categories by Conversion",
                  color='conversion', color_continuous_scale='greens')
    fig2.update_layout(xaxis_tickangle=-30, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.bar(worst_cat, x='category_code', y='conversion',
                  title="Worst 10 Categories by Conversion",
                  color='conversion', color_continuous_scale='reds_r')
    fig3.update_layout(xaxis_tickangle=-30, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -------------------- TIME ANALYSIS --------------------
st.markdown("### ⏱ User Behavior by Time")

# Hourly
hour_grp = df.groupby(['hour', 'event_type']).size().unstack(fill_value=0)
for col in ['view', 'cart', 'purchase']:
    if col not in hour_grp.columns:
        hour_grp[col] = 0
hour_grp['conversion'] = (hour_grp['purchase'] / hour_grp['view']).round(4)

col1, col2 = st.columns(2)
with col1:
    fig4 = px.line(hour_grp.reset_index(), x='hour', y='conversion',
                   title="Conversion Rate by Hour of Day", markers=True)
    fig4.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    fig5 = px.bar(hour_grp.reset_index(), x='hour', y='view',
                  title="User Activity (Views) by Hour",
                  color='view', color_continuous_scale='blues')
    st.plotly_chart(fig5, use_container_width=True)

# Day of week — correctly ordered Mon to Sun
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_grp = df.groupby(['day', 'event_type']).size().unstack(fill_value=0)
for col in ['view', 'cart', 'purchase']:
    if col not in day_grp.columns:
        day_grp[col] = 0
day_grp['conversion'] = (day_grp['purchase'] / day_grp['view']).round(4)
day_grp = day_grp.reindex(day_order)

col1, col2 = st.columns(2)
with col1:
    fig6 = px.line(day_grp.reset_index(), x='day', y='conversion',
                   title="Conversion Rate by Day of Week", markers=True)
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    fig7 = px.bar(day_grp.reset_index(), x='day', y='view',
                  title="User Activity (Views) by Day of Week",
                  color='view', color_continuous_scale='purples')
    st.plotly_chart(fig7, use_container_width=True)

st.divider()

# -------------------- BUSINESS IMPACT --------------------
st.markdown("### 💰 Business Impact Simulation")
st.caption(f"Average Order Value: **${aov:,.2f}** — calculated from actual purchase events in the dataset")

col1, col2 = st.columns([2, 1])

with col1:
    target_conversion = st.slider(
        "Target View → Cart Conversion Rate",
        min_value=0.05,
        max_value=0.30,
        value=0.12,
        step=0.005,
        format="%.2f"
    )

improved_carts   = views * target_conversion
extra_carts      = improved_carts - carts
extra_purchases  = int(extra_carts * cart_to_purchase)
revenue_gain     = extra_purchases * aov
current_revenue  = purchases * aov

with col2:
    st.metric("Current Purchases",       f"{purchases:,}")
    st.metric("Potential Extra Purchases", f"+{extra_purchases:,}")
    st.metric("Estimated Revenue Gain",   f"${revenue_gain:,.0f}",
              delta=f"+{revenue_gain/current_revenue*100:.1f}% vs current" if current_revenue > 0 else None)

# Scenario comparison chart
scenarios = {
    'Current\n(7.6%)': (purchases, 0),
    'Conservative\n(9.5%)': (
        purchases + int((views * 0.095 - carts) * cart_to_purchase),
        int((views * 0.095 - carts) * cart_to_purchase) * aov
    ),
    'Target\n(12%)': (
        purchases + int((views * 0.12 - carts) * cart_to_purchase),
        int((views * 0.12 - carts) * cart_to_purchase) * aov
    ),
    'Optimistic\n(15%)': (
        purchases + int((views * 0.15 - carts) * cart_to_purchase),
        int((views * 0.15 - carts) * cart_to_purchase) * aov
    ),
}

scenario_df = pd.DataFrame([
    {'Scenario': k, 'Total Purchases': v[0], 'Revenue Gain ($)': round(v[1], 2)}
    for k, v in scenarios.items()
])

fig8 = px.bar(scenario_df, x='Scenario', y='Revenue Gain ($)',
              text='Revenue Gain ($)',
              title=f'Revenue Gain by Scenario (AOV = ${aov:,.2f} from real data)',
              color='Revenue Gain ($)', color_continuous_scale='greens')
fig8.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
fig8.update_layout(showlegend=False)
st.plotly_chart(fig8, use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("Built with Streamlit · Data: REES46 E-commerce Dataset · Sahana L")