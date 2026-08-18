import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.battery import Battery
from models.electrolyzer import Electrolyzer
from models.solar import SolarPlant
from simulation.simulation import DigitalTwin
from simulation.engine import run_simulation
print("=" * 50)
print("GREEN HYDROGEN DIGITAL TWIN")
print("=" * 50)

# Load monthly irradiation dataset
df = pd.read_csv("data/monthly_irradiation.csv")
solar = SolarPlant(df["PVGIS_GWh"])
annual_energy = solar.annual_energy()

print(f"Annual PV Energy : {annual_energy:.2f} GWh")

print("\nMonthly PV dataset:\n")
print(df)

Hydrogen Production 

Electrolyzer specific energy consumption
specific_energy = 55      # kWh per kg H2

Convert PV energy from GWh to kWh
solar = SolarPlant(df["PVGIS_GWh"] * 1_000_000)

battery = Battery(capacity_kwh=120_000)

electrolyzer = Electrolyzer(
    specific_energy=specific_energy,
    rated_power_kw=40_000
)

digital_twin = DigitalTwin(solar, battery, electrolyzer)

hydrogen_kg = digital_twin.run()

# Add results to the DataFrame
df["Hydrogen_kg"] = hydrogen_kg

print("\nHydrogen Production:\n")
print(df)
# ==================================================
# NumPy Statistics
# ==================================================

annual_h2 = np.sum(df["Hydrogen_kg"])

average_h2 = np.mean(df["Hydrogen_kg"])

maximum_h2 = np.max(df["Hydrogen_kg"])

minimum_h2 = np.min(df["Hydrogen_kg"])

print("\n==============================")
print("Simulation Results")
print("==============================")

print(f"Annual hydrogen production : {annual_h2:,.0f} kg")

print(f"Average monthly production : {average_h2:,.0f} kg")

print(f"Maximum monthly production : {maximum_h2:,.0f} kg")

print(f"Minimum monthly production : {minimum_h2:,.0f} kg")
# ==================================================
# Visualization
# ==================================================

plt.figure(figsize=(10, 5))

plt.bar(df["Month"], df["Hydrogen_kg"]/1000)

plt.title("Monthly Hydrogen Production")

plt.xlabel("Month")

plt.ylabel("Hydrogen Production (tonnes)")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig("results/hydrogen_production.png", dpi=300)

plt.show()
battery = Battery(capacity_kwh=120000)

print("\nBattery Test")
print("----------------")

battery.charge(50000)
print("SOC =", battery.get_soc())

battery.charge(90000)
print("SOC =", battery.get_soc())

battery.discharge(30000)
print("SOC =", battery.get_soc())
print("\n===== ENGINE TEST =====")

results = run_simulation()

print(results)
