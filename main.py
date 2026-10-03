"""
Green Hydrogen Digital Twin - Witznitz (Saxony)
Run:  python main.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # save figures without opening windows

from data import parameters as p
from simulation.economics import thesis_reproduction
from simulation.engine import run_simulation
from visualization.plots import (plot_lcoh_breakdown, plot_monthly_balance,
                                 plot_tornado)

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(exist_ok=True)


def print_lcoh(title, breakdown):
    print(f"\n{title}")
    print("-" * 50)
    for key, value in breakdown.items():
        if key != "LCOH":
            print(f"  {key:<28}: {value:6.2f} EUR/kg")
    print(f"  {'LCOH':<28}: {breakdown['LCOH']:6.2f} EUR/kg")


def main():
    print("=" * 50)
    print("GREEN HYDROGEN DIGITAL TWIN - WITZNITZ")
    print("=" * 50)
    print(f"PV {p.PV_CAPACITY_MWP:.0f} MWp | AWE {p.ELECTROLYZER_POWER_KW/1000:.0f} MW | "
          f"BESS {p.BATTERY_CAPACITY_KWH/1000:.0f} MWh | {p.SPECIFIC_ENERGY_KWH_PER_KG} kWh/kg")

    # 1) Reproduction of thesis Table 13 (inputs of Table 12)
    print_lcoh("1) Thesis reproduction (Table 12 inputs)", thesis_reproduction())

    # 2) Simulated plant, both operating modes
    for mode in ("grid_assisted", "pv_only"):
        res = run_simulation(mode=mode)
        df = res["dataframe"]
        print(f"\n2) Simulation - mode: {mode}")
        print("-" * 50)
        print(f"  PV energy (year 1)        : {res['annual_energy']/1e6:8.2f} GWh")
        print(f"  PV capacity factor        : {res['capacity_factor']*100:8.1f} %")
        print(f"  Electrolyzer consumption  : {df['Electrolyzer_kWh'].sum()/1e6:8.2f} GWh")
        print(f"  Grid import               : {res['grid_import']/1e6:8.2f} GWh")
        print(f"  Grid export               : {res['grid_export']/1e6:8.2f} GWh")
        print(f"  PV share of electrolyzer  : {res['pv_share']*100:8.1f} %")
        print(f"  Hydrogen production       : {res['annual_h2']/1000:8.0f} t/year "
              f"({res['annual_h2']/365/1000:.1f} t/day)")
        print_lcoh(f"  LCOH ({mode})", res["lcoh"])

        df.to_csv(RESULTS / f"monthly_results_{mode}.csv", index=False)
        plot_monthly_balance(df, RESULTS / f"energy_balance_{mode}.png")
        plot_lcoh_breakdown(res["lcoh"], RESULTS / f"lcoh_{mode}.png",
                            title=f"LCOH ({mode})")

    # 3) Sensitivity analysis (grid-assisted mode, +/- 20 %)
    base = run_simulation()["lcoh"]["LCOH"]
    cases = {
        "PV capacity (MWp)": "pv_capacity_mwp",
        "BESS capacity (kWh)": "battery_capacity_kwh",
        "WACC": "wacc",
        "Grid export price": "export_price",
        "Grid import price": "import_price",
    }
    defaults = {
        "pv_capacity_mwp": p.PV_CAPACITY_MWP,
        "battery_capacity_kwh": p.BATTERY_CAPACITY_KWH,
        "wacc": p.WACC,
        "export_price": p.GRID_EXPORT_PRICE_EUR_PER_MWH,
        "import_price": p.GRID_IMPORT_PRICE_EUR_PER_MWH,
    }
    tornado = []
    print("\n3) Sensitivity analysis (+/- 20 %)")
    print("-" * 50)
    for label, key in cases.items():
        low = run_simulation(**{key: defaults[key] * 0.8})["lcoh"]["LCOH"]
        high = run_simulation(**{key: defaults[key] * 1.2})["lcoh"]["LCOH"]
        tornado.append((label, low, high))
        print(f"  {label:<22}: {low:5.2f} / {high:5.2f} EUR/kg")
    plot_tornado(tornado, base, RESULTS / "sensitivity.png")

    print(f"\nResults and figures saved in: {RESULTS}")


if __name__ == "__main__":
    main()
