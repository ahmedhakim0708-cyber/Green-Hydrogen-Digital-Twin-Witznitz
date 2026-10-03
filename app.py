"""
Interactive dashboard.
Run:  streamlit run app.py
"""
import plotly.express as px
import streamlit as st

from data import parameters as p
from simulation.economics import thesis_reproduction
from simulation.engine import run_simulation

st.set_page_config(page_title="GH2 Digital Twin - Witznitz", page_icon="⚡",
                   layout="wide")
st.title("⚡ Green Hydrogen Digital Twin - Witznitz")
st.caption("PV + LFP BESS + alkaline electrolyzer - monthly energy balance "
           "and 25-year LCOH (IRENA DCF method)")

with st.sidebar:
    st.header("Design parameters")
    pv = st.slider("PV capacity (MWp)", 100, 600, int(p.PV_CAPACITY_MWP), 10)
    ely = st.slider("Electrolyzer (MW)", 10, 100, int(p.ELECTROLYZER_POWER_KW / 1000))
    bess = st.slider("BESS (MWh)", 0, 400, int(p.BATTERY_CAPACITY_KWH / 1000), 10)
    mode = st.radio("Operating mode", ["grid_assisted", "pv_only"])
    source = st.radio("PV data source", ["PVGIS_GWh", "DWD_GWh"])
    st.header("Economic parameters")
    wacc = st.slider("WACC (%)", 3.0, 12.0, p.WACC * 100, 0.5) / 100
    exp_price = st.slider("Export price (EUR/MWh)", 0, 150,
                          int(p.GRID_EXPORT_PRICE_EUR_PER_MWH))
    imp_price = st.slider("Import price (EUR/MWh)", 0, 250,
                          int(p.GRID_IMPORT_PRICE_EUR_PER_MWH))

res = run_simulation(pv_capacity_mwp=pv, battery_capacity_kwh=bess * 1000,
                     electrolyzer_power_kw=ely * 1000, mode=mode,
                     data_source=source, wacc=wacc,
                     export_price=exp_price, import_price=imp_price)
df = res["dataframe"]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Annual H₂", f"{res['annual_h2']/1000:,.0f} t")
c2.metric("PV energy", f"{res['annual_energy']/1e6:.1f} GWh")
c3.metric("Grid import", f"{res['grid_import']/1e6:.1f} GWh")
c4.metric("PV share", f"{res['pv_share']*100:.0f} %")
c5.metric("LCOH", f"{res['lcoh']['LCOH']:.2f} €/kg",
          delta=f"{res['lcoh']['LCOH'] - 4.5:+.2f} vs 4.50 target",
          delta_color="inverse")

st.markdown("---")
left, right = st.columns(2)
energy = df.melt(id_vars="Month",
                 value_vars=["PV_to_electrolyzer_kWh", "Grid_import_kWh",
                             "Grid_export_kWh"],
                 var_name="Flow", value_name="kWh")
energy["GWh"] = energy["kWh"] / 1e6
left.plotly_chart(px.bar(energy, x="Month", y="GWh", color="Flow",
                         barmode="group", title="Monthly energy balance"),
                  width="stretch")
right.plotly_chart(px.bar(df, x="Month", y=df["Hydrogen_kg"] / 1000,
                          labels={"y": "Hydrogen (t)"},
                          title="Monthly hydrogen production"),
                   width="stretch")

st.subheader("LCOH decomposition (EUR/kg)")
lc = {k: v for k, v in res["lcoh"].items() if k != "LCOH"}
st.plotly_chart(px.bar(x=list(lc.values()), y=list(lc.keys()), orientation="h",
                       labels={"x": "EUR/kg", "y": ""}), width="stretch")

with st.expander("Thesis reproduction (Table 13)"):
    st.json({k: round(v, 2) for k, v in thesis_reproduction().items()})

st.subheader("Monthly results")
st.dataframe(df, width="stretch")
st.download_button("📥 Download CSV", df.to_csv(index=False),
                   file_name="GH2_results.csv", mime="text/csv")
