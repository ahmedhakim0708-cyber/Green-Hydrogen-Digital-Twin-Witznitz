from data.parameters import (
    INVERTER_EFFICIENCY,
    CABLE_EFFICIENCY,
    PV_DEGRADATION
)


class SolarPlant:
    """
    Solar PV plant model.
    """

    def __init__(self, monthly_energy):
        self.monthly_energy = monthly_energy

    def annual_energy(self):
        annual_energy = self.monthly_energy.sum()

        usable_energy = (
            annual_energy
            * INVERTER_EFFICIENCY
            * CABLE_EFFICIENCY
            * PV_DEGRADATION
        )

        return usable_energy

    def monthly_energy_output(self):
        usable_monthly_energy = (
            self.monthly_energy
            * INVERTER_EFFICIENCY
            * CABLE_EFFICIENCY
            * PV_DEGRADATION
        )

        return usable_monthly_energy
