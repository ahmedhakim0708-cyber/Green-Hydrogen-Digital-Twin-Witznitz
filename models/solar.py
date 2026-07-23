class SolarPlant:
    """
    Solar PV plant model.
    """

    def __init__(self, monthly_energy):
        self.monthly_energy = monthly_energy

    def annual_energy(self):
        return self.monthly_energy.sum()

    def monthly_energy_output(self):
        return self.monthly_energy
