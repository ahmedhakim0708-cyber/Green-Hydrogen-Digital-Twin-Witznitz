class Electrolyzer:
    """Alkaline water electrolyzer (system level, AC side)."""

    def __init__(self, rated_power_kw, specific_energy_kwh_per_kg,
                 availability=1.0):
        self.rated_power_kw = rated_power_kw
        self.specific_energy = specific_energy_kwh_per_kg
        self.availability = availability

    def max_energy_intake(self, hours):
        """Maximum electrical energy (kWh) the plant can absorb in `hours`."""
        return self.rated_power_kw * hours * self.availability

    def produce_hydrogen(self, energy_kwh):
        """Hydrogen produced (kg) from AC energy (kWh)."""
        return energy_kwh / self.specific_energy

    def energy_for_hydrogen(self, hydrogen_kg):
        """AC energy (kWh) needed for a given hydrogen mass (kg)."""
        return hydrogen_kg * self.specific_energy
