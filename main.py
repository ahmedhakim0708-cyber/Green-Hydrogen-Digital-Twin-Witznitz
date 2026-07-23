import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("=" * 50)
print("GREEN HYDROGEN DIGITAL TWIN")
print("=" * 50)

# Load monthly irradiation dataset
df = pd.read_csv("data/monthly_irradiation.csv")

print("\nMonthly PV dataset:\n")
print(df)
# ==================================================
# Hydrogen Production Calculation
# ==================================================

# Electrolyzer specific energy consumption
specific_energy = 55      # kWh per kg H2

# Convert PV energy from GWh to kWh
pv_energy_kWh = df["PVGIS_GWh"] * 1_000_000

# Calculate hydrogen production
hydrogen_kg = pv_energy_kWh / specific_energy

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
