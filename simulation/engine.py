import pandas as pd
import numpy as np

from models.battery import Battery
from models.electrolyzer import Electrolyzer
from models.solar import SolarPlant
from simulation.simulation import DigitalTwin


def run_simulation(
    pv_capacity=300,
    battery_capacity=120000,
    electrolyzer_power=40000,
    specific_energy=55
):
    """
    Runs the GH2 Digital Twin simulation.
    """
    # Load monthly irradiation dataset
    df = pd.read_csv("data/monthly_irradiation.csv")

    # Convert PV production from GWh to kWh
    base_pv_capacity = 300  # MW (cas de référence)


scaled_energy = (
    df["PVGIS_GWh"]
    * (pv_capacity / base_pv_capacity)
    * 1_000_000
)

solar = SolarPlant(scaled_energy)

# Create system components
battery = Battery(capacity_kwh=battery_capacity)

electrolyzer = Electrolyzer(
    specific_energy=specific_energy,
    rated_power_kw=electrolyzer_power
)

# Run Digital Twin simulation
digital_twin = DigitalTwin(solar, battery, electrolyzer)

hydrogen_kg = digital_twin.run()

# Store results
df["Hydrogen_kg"] = hydrogen_kg
# Statistics
annual_h2 = np.sum(df["Hydrogen_kg"])
average_h2 = np.mean(df["Hydrogen_kg"])
maximum_h2 = np.max(df["Hydrogen_kg"])
minimum_h2 = np.min(df["Hydrogen_kg"])

# Return results
return {
    "annual_h2": annual_h2,
    "average_h2": average_h2,
    "maximum_h2": maximum_h2,
    "minimum_h2": minimum_h2,
    "annual_energy": solar.annual_energy(),
    "monthly_h2": df["Hydrogen_kg"],
    "months": df["Month"],
    "dataframe": df,
}
