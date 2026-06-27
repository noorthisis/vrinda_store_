import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vrinda Store Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/vrinda_store_cleaned.csv", parse_dates=["Date"])
    return df

df = load_data()

# ─── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=70)
st.sidebar.title("🔎 Filters")

months_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
available_months = [m for m in months_order if m in df["Month"].unique()]

selected_months = st.sidebar.multiselect("Month", available_months, default=available_months)
selected_channels = st.sidebar.multiselect("Channel", df["Channel"].unique(), default=df["Channel"].unique())
selected_categories = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
selected_gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())

# ─── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df[
    df["Month"].isin(selected_months) &
    df["Channel"].isin(selected_channels) &
    df["Category"].isin(selected_categories) &
    df["Gender"].isin(selected_gender)
]

# ─── Title ─────────────────────────────────────────────────────────────────────
st.title("🛍️ Vrinda Store — Annual Sales Dashboard (2022)")
st.caption("An interactive sales analysis dashboard built with Python & Streamlit.")
st.markdown("---")

# ─── KPI Cards ─────────────────────────────────────────────────────────────────
total_revenue = filtered["Amount"].sum()
total_orders  = filtered["Order ID"].nunique()
avg_order_val = filtered["Amount"].mean()
delivery_rate = (filtered["Status"] == "Delivered").sum() / len(filtered) * 100 if len(filtered) > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Revenue",   f"₹{total_revenue:,.0f}")
k2.metric("📦 Total Orders",    f"{total_orders:,}")
k3.metric("🧾 Avg Order Value", f"₹{avg_order_val:,.0f}")
k4.metric("✅ Delivery Rate",   f"{delivery_rate:.1f}%")

st.markdown("---")

# ─── Row 1: Monthly Revenue + Order Status ─────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Monthly Revenue vs Orders")
    monthly = (
        filtered.groupby(["Month_Num", "Month"])
        .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Month_Num")
    )
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=monthly["Month"], y=monthly["Revenue"], name="Revenue (₹)", marker_color="#6366f1"))
    fig1.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Orders"], name="Orders", yaxis="y2",
                              line=dict(color="#f59e0b", width=3), mode="lines+markers"))
    fig1.update_layout(
        yaxis=dict(title="Revenue (₹)"),
        yaxis2=dict(title="Orders", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.1),
        height=350, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Order Status")
    status_counts = filtered["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig2 = px.pie(status_counts, names="Status", values="Count",
                  color_discrete_sequence=["#6366f1","#10b981","#f59e0b","#ef4444"],
                  hole=0.4)
    fig2.update_layout(height=350, margin=dict(t=20, b=20), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig2, use_container_width=True)

# ─── Row 2: Gender + Channel ───────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("👥 Sales by Gender")
    gender_data = filtered.groupby("Gender")["Amount"].sum().reset_index()
    fig3 = px.bar(gender_data, x="Gender", y="Amount",
                  color="Gender", color_discrete_sequence=["#8b5cf6","#06b6d4"],
                  labels={"Amount": "Revenue (₹)"})
    fig3.update_layout(height=320, showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🛒 Channel Contribution")
    channel_data = filtered.groupby("Channel")["Amount"].sum().reset_index().sort_values("Amount", ascending=True)
    fig4 = px.bar(channel_data, x="Amount", y="Channel", orientation="h",
                  color="Amount", color_continuous_scale="Purples",
                  labels={"Amount": "Revenue (₹)"})
    fig4.update_layout(height=320, coloraxis_showscale=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

# ─── Row 3: Top States + Age Group ────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("📍 Top 10 States by Revenue")
    state_data = (
        filtered.groupby("Ship State")["Amount"].sum()
        .reset_index().sort_values("Amount", ascending=False).head(10)
    )
    fig5 = px.bar(state_data, x="Ship State", y="Amount",
                  color="Amount", color_continuous_scale="Viridis",
                  labels={"Amount": "Revenue (₹)", "Ship State": "State"})
    fig5.update_layout(height=350, coloraxis_showscale=False,
                       xaxis_tickangle=-30, margin=dict(t=10, b=10))
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("🎂 Orders by Age Group & Gender")
    age_gender = (
        filtered.groupby(["Age Group", "Gender"])["Order ID"]
        .nunique().reset_index().rename(columns={"Order ID": "Orders"})
    )
    age_order = ["Teenager (< 25)", "Young Adult (25-34)", "Adult (35-49)", "Senior (50+)"]
    age_gender["Age Group"] = pd.Categorical(age_gender["Age Group"], categories=age_order, ordered=True)
    age_gender = age_gender.sort_values("Age Group")
    fig6 = px.bar(age_gender, x="Age Group", y="Orders", color="Gender",
                  barmode="group", color_discrete_sequence=["#8b5cf6","#06b6d4"])
    fig6.update_layout(height=350, margin=dict(t=10, b=10), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig6, use_container_width=True)

# ─── Row 4: Category Breakdown ────────────────────────────────────────────────
st.subheader("👗 Category-wise Revenue")
cat_data = filtered.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
fig7 = px.bar(cat_data, x="Category", y="Amount",
              color="Category",
              labels={"Amount": "Revenue (₹)"},
              color_discrete_sequence=px.colors.qualitative.Pastel)
fig7.update_layout(height=320, showlegend=False, margin=dict(t=10, b=10))
st.plotly_chart(fig7, use_container_width=True)

# ─── Raw Data Table ───────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered[["Order ID","Date","Gender","Age Group","Channel","Category","Amount","Status","Ship State"]].head(500), use_container_width=True)

st.caption("Built by Noor | Vrinda Store Sales Analysis 2022 | Data: Kaggle")
