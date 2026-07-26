import streamlit as st
from simulation.engine import run_simulation
import plotly.express as px
st.set_page_config(
    page_title="GH2 Digital Twin",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GH2 Digital Twin")
st.markdown("---")
st.header("Simulation Parameters")

pv = st.slider("PV Capacity (MW)", 50, 500, 300)

electrolyzer = st.slider("Electrolyzer (MW)", 10, 100, 40)

battery = st.slider("Battery (MWh)", 10, 300, 120)

results = run_simulation(
    pv_capacity=pv,
    battery_capacity=battery * 1000,      # MWh → kWh
    electrolyzer_power=electrolyzer * 1000  # MW → kW
)
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Annual H₂",
    f"{results['annual_h2']/1000:.1f} t"
)

col2.metric(
    "PV Energy",
    f"{results['annual_energy']/1_000_000:.1f} GWh"
)

col3.metric(
    "Electrolyzer",
    f"{electrolyzer} MW"
)

col4.metric(
    "Battery",
    f"{battery} MWh"
)
st.markdown("---")

fig = px.bar(
    results["dataframe"],
    x="Month",
    y="Hydrogen_kg",
    title="Monthly Hydrogen Production"
)

st.plotly_chart(fig, use_container_width=True)
# ==========================
# Table of results
# ==========================
st.markdown("---")
st.subheader("Simulation Results")

st.dataframe(results["dataframe"])

# ==========================
# Download the results
# ==========================
st.download_button(
    "📥 Download CSV",
    results["dataframe"].to_csv(index=False),
    file_name="GH2_results.csv",
    mime="text/csv"
)
