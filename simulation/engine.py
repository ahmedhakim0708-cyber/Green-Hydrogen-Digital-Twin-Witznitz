from pathlib import Path

import numpy as np
import pandas as pd

from data import parameters as p
from models.battery import Battery
from models.electrolyzer import Electrolyzer
from models.solar import SolarPlant
from simulation.economics import grid_cost_series, lcoh
from simulation.simulation import DigitalTwin

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "monthly_irradiation.csv"


def scaled_capex(pv_capacity_mwp, electrolyzer_power_kw, battery_capacity_kwh):
    """
    CAPEX scaled linearly from the thesis reference design
    (300 MWp / 35 MW / 160 MWh). Simple first-order assumption.
    """
    c = p.CAPEX_EUR
    pv = (c["PV system"] + c["PV balance of system"]) * pv_capacity_mwp / p.PV_CAPACITY_MWP
    awe = (c["AWE electrolyzer"] + c["H2 post-processing"]) \
        * electrolyzer_power_kw / p.ELECTROLYZER_POWER_KW
    bess = c["BESS + auxiliaries"] * battery_capacity_kwh / p.BATTERY_CAPACITY_KWH
    return pv + awe + bess


def run_simulation(pv_capacity_mwp=p.PV_CAPACITY_MWP,
                   battery_capacity_kwh=p.BATTERY_CAPACITY_KWH,
                   electrolyzer_power_kw=p.ELECTROLYZER_POWER_KW,
                   specific_energy=p.SPECIFIC_ENERGY_KWH_PER_KG,
                   mode="grid_assisted",
                   data_source=p.PV_DATA_SOURCE,
                   wacc=p.WACC,
                   export_price=p.GRID_EXPORT_PRICE_EUR_PER_MWH,
                   import_price=p.GRID_IMPORT_PRICE_EUR_PER_MWH):
    """Runs the GH2 digital twin (year 1 balance + 25-year LCOH)."""
    df = pd.read_csv(DATA_FILE)

    solar = SolarPlant(df[data_source] * 1_000_000,          # GWh -> kWh
                       capacity_mwp=pv_capacity_mwp,
                       reference_mwp=p.PV_REFERENCE_MWP,
                       degradation_per_year=p.PV_DEGRADATION_PER_YEAR)
    battery = Battery(battery_capacity_kwh, p.BATTERY_DOD,
                      p.BATTERY_CHARGE_EFFICIENCY,
                      p.BATTERY_DISCHARGE_EFFICIENCY,
                      p.BATTERY_CYCLES_PER_DAY)
    electrolyzer = Electrolyzer(electrolyzer_power_kw, specific_energy,
                                p.AVAILABILITY)
    twin = DigitalTwin(solar, battery, electrolyzer, df["Month"], df["Days"],
                       p.H2_TARGET_KG_PER_DAY)

    # Year-1 monthly results
    monthly = twin.run(mode=mode, year=1)

    # Lifetime loop (PV degradation changes the balance every year)
    h2, imp, exp = [], [], []
    for year in range(1, p.PROJECT_LIFETIME_YEARS + 1):
        r = twin.run(mode=mode, year=year)
        h2.append(r["Hydrogen_kg"].sum())
        imp.append(r["Grid_import_kWh"].sum() / 1_000)    # MWh
        exp.append(r["Grid_export_kWh"].sum() / 1_000)

    grid = grid_cost_series(np.array(imp), np.array(exp),
                            import_price=import_price, export_price=export_price)
    capex = scaled_capex(pv_capacity_mwp, electrolyzer_power_kw, battery_capacity_kwh)
    cost = lcoh(capex, np.array(h2), grid, wacc=wacc)

    return {
        "dataframe": monthly,
        "annual_h2": monthly["Hydrogen_kg"].sum(),
        "annual_energy": solar.annual_energy(),
        "capacity_factor": solar.capacity_factor(),
        "grid_import": monthly["Grid_import_kWh"].sum(),
        "grid_export": monthly["Grid_export_kWh"].sum(),
        "pv_share": monthly["PV_to_electrolyzer_kWh"].sum()
        / max(monthly["Electrolyzer_kWh"].sum(), 1e-9),
        "capex": capex,
        "lcoh": cost,
    }
