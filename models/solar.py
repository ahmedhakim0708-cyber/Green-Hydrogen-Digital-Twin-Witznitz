import pandas as pd


class SolarPlant:
    """PV plant based on monthly PVGIS / DWD energy yields."""

    def __init__(self, monthly_energy_kwh, capacity_mwp, reference_mwp,
                 degradation_per_year=0.0):
        self.reference_energy_kwh = pd.Series(monthly_energy_kwh, dtype=float).reset_index(drop=True)
        self.capacity_mwp = capacity_mwp
        self.reference_mwp = reference_mwp
        self.degradation_per_year = degradation_per_year

    def monthly_energy_output(self, year=1):
        """Monthly AC energy (kWh) in a given operating year (1 = first year)."""
        scale = self.capacity_mwp / self.reference_mwp
        degradation = (1 - self.degradation_per_year) ** (year - 1)
        return self.reference_energy_kwh * scale * degradation

    def annual_energy(self, year=1):
        return float(self.monthly_energy_output(year).sum())

    def capacity_factor(self, year=1):
        return self.annual_energy(year) / (self.capacity_mwp * 1_000 * 8_760)
