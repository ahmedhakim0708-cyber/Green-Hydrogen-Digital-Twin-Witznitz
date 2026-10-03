"""
Central parameter file - every value is taken from the project thesis
"Techno-Economic Optimization of a Solar-Powered Electrolyzer System for
Green Hydrogen Production in Germany" (TH Rosenheim, 2026).
Section / table references are given next to each value.
"""

# ---------------------------------------------------------------- PV plant
PV_CAPACITY_MWP = 300.0            # Tab. 5 / Tab. 6
PV_REFERENCE_MWP = 300.0           # capacity behind the PVGIS monthly values (Tab. 7)
PV_DATA_SOURCE = "PVGIS_GWh"       # "PVGIS_GWh" (used in thesis results) or "DWD_GWh"
PV_DEGRADATION_PER_YEAR = 0.004    # 0.40 %/yr, section 4.3
# NOTE: PVGIS E_m values already include system losses (inverter, cabling,
# temperature, soiling). No additional loss factor is applied to avoid
# double counting.

# ------------------------------------------------------------ Electrolyzer
ELECTROLYZER_POWER_KW = 35_000     # 7 x 5 MW John Cockerill AWE, section 4.5 / 4.6
SPECIFIC_ENERGY_KWH_PER_KG = 55.6  # system level (AC), section 4.5 Step 1
AVAILABILITY = 0.95                # section 5.1
H2_TARGET_KG_PER_DAY = 13_000      # section 4.2 / Tab. 5

# ------------------------------------------------------------------- BESS
BATTERY_CAPACITY_KWH = 160_000     # 32 x 5 MWh LFP containers, Tab. 4
BATTERY_DOD = 0.90                 # section 4.5 Step 3
BATTERY_CHARGE_EFFICIENCY = 0.95   # -> round trip ~0.92 (thesis: ~90 %)
BATTERY_DISCHARGE_EFFICIENCY = 0.97  # section 4.5 Step 3
BATTERY_CYCLES_PER_DAY = 1         # daily evening-peak bridging (4 h)

# --------------------------------------------------------------- Economics
PROJECT_LIFETIME_YEARS = 25        # Tab. 12
WACC = 0.07                        # Tab. 12 (2030 scenario)
CAPEX_EUR = {                      # section 4.7.1, total 247.51 M EUR
    "PV system": 125.50e6,
    "PV balance of system": 23.50e6,
    "AWE electrolyzer": 65.00e6,
    "H2 post-processing": 6.60e6,
    "BESS + auxiliaries": 26.91e6,
}
OPEX_EUR_PER_YEAR = 5.08e6         # section 4.7.2
OPEX_ESCALATION = 0.02             # section 4.7.2
REPLACEMENTS = [                   # Tab. 12: (year, cost EUR, label)
    (12, 7.0e6, "AWE stack replacement"),
    (12, 20.0e6, "BESS replacement"),
]
GRID_EXPORT_PRICE_EUR_PER_MWH = 58.0   # Tab. 12
GRID_IMPORT_PRICE_EUR_PER_MWH = 50.0   # Tab. 12
GRID_PRICE_ESCALATION = 0.005          # Tab. 12

# Grid flows and H2 output as stated in the thesis (Tab. 12) - used to reproduce Tab. 13
THESIS_EXPORT_GWH = 89.8
THESIS_IMPORT_GWH = 29.9
THESIS_H2_T_PER_YEAR = 4_508
