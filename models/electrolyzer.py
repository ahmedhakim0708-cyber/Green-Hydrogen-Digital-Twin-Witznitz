class Electrolyzer:
    def __init__(self, specific_energy, rated_power_kw=None):
        self.specific_energy = specific_energy
        self.rated_power_kw = rated_power_kw

    def max_energy_intake(self, hours):
        if self.rated_power_kw is None:
            return float("inf")
        return self.rated_power_kw * hours

    def produce_hydrogen(self, energy_kwh):
        return energy_kwh / self.specific_energy
