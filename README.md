# Green Hydrogen Digital Twin – Witznitz (Saxony, Germany)

Python digital twin accompanying the project thesis
**"Techno-Economic Optimization of a Solar-Powered Electrolyzer System for Green Hydrogen Production in Germany"**
(MSc Hydrogen Technology, TH Rosenheim, 2026).

It models a **300 MWp ground-mounted PV plant**, a **160 MWh LFP battery (BESS)** and a
**35 MW John Cockerill pressurized alkaline electrolyzer (7 × 5 MW)** at Witznitz near Leipzig,
and computes the monthly energy balance, the hydrogen output and the
**Levelized Cost of Hydrogen (LCOH)** over 25 years (IRENA discounted-cash-flow method).
   ![Streamlit dashboard](dashboard.png)
## Features
- Monthly PV yield from **PVGIS-SARAH3** (or DWD for comparison), scalable to any PV size
- LFP BESS with depth of discharge, charge/discharge efficiency and daily cycling
- Two operating modes:
  - `grid_assisted`: electrolyzer follows the 13 t/day target, deficits imported, surplus exported
  - `pv_only`: electrolyzer runs on PV (+BESS) only, no grid import
- 25-year LCOH with CAPEX, escalated OPEX, grid import/export, stack and BESS replacement, PV degradation
- Exact reproduction of the thesis LCOH (Table 13: **5.62 €/kg**)
- One-at-a-time sensitivity analysis (±20 %) with tornado chart
- Interactive Streamlit dashboard

## Project structure
```
├── app.py                   # Streamlit dashboard
├── main.py                  # command-line run, saves CSV + figures in results/
├── data/
│   ├── parameters.py        # ALL input parameters (with thesis references)
│   └── monthly_irradiation.csv
├── models/
│   ├── solar.py             # SolarPlant
│   ├── battery.py           # Battery (LFP BESS)
│   └── electrolyzer.py      # Electrolyzer (AWE)
├── simulation/
│   ├── simulation.py        # DigitalTwin – monthly energy balance
│   ├── economics.py         # LCOH (DCF), thesis reproduction, sensitivity
│   └── engine.py            # run_simulation() – used by main.py and app.py
├── visualization/plots.py
└── results/
```

## Installation and use
```bash
git clone https://github.com/ahmedhakim0708-cyber/Green-Hydrogen-Digital-Twin-Witznitz.git
cd Green-Hydrogen-Digital-Twin-Witznitz
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python main.py          # results in the terminal + results/*.csv, *.png
streamlit run app.py    # interactive dashboard
```

## Main assumptions (see `data/parameters.py`)
| Parameter | Value |
|---|---|
| PV capacity / yield (PVGIS) | 300 MWp / 265.37 GWh/yr (CF ≈ 10.1 %) |
| Electrolyzer | 35 MW AWE, 55.6 kWh/kg H₂ (system, AC), 95 % availability |
| Production target | 13 t H₂/day |
| BESS | 160 MWh LFP, DoD 90 %, η_ch 95 %, η_dis 97 %, 1 cycle/day |
| CAPEX | 247.51 M€ |
| OPEX | 5.08 M€/yr, +2 %/yr |
| WACC / lifetime | 7 % / 25 years |
| Grid prices | export 58 €/MWh, import 50 €/MWh, +0.5 %/yr |
| Replacements (year 12) | AWE stacks 7 M€, BESS 20 M€ |

## Example results (`python main.py`)
| Case | H₂ (t/yr) | Grid import | Grid export | LCOH |
|---|---|---|---|---|
| Thesis reproduction (Table 12 inputs) | 4,508 | 29.9 GWh | 89.8 GWh | 5.62 €/kg |
| Simulated, `grid_assisted` | 4,508 | 67.7 GWh | 78.1 GWh | 6.14 €/kg |
| Simulated, `pv_only` | 3,647 | 0 | 58.3 GWh | 7.01 €/kg |

The simulated energy balance needs more grid import than assumed in the thesis
(PV alone cannot supply 250.6 GWh/yr), which explains the difference to 5.62 €/kg.

## Limitations
- **Monthly time step**: day/night flows are netted within each month, so grid import
  and export are underestimated and the BESS is represented only through its daily
  throughput and losses. An hourly model (PVGIS hourly series) is the next step.
- Electrolyzer at constant specific consumption (no part-load efficiency, minimum load or ramping).
- CAPEX scaled linearly when PV/AWE/BESS sizes are changed in the dashboard.
- RFNBO compliance (hourly temporal correlation of grid electricity) is not checked.
- Oxygen and waste-heat revenues are not included.

## License
MIT – see `LICENSE`.
