class Battery:
    """
    Battery Energy Storage System (BESS)
    """

    def __init__(self, capacity_kwh, efficiency=0.95):

        self.capacity_kwh = capacity_kwh
        self.efficiency = efficiency

        # State of Charge
        self.soc = 0

    def charge(self, energy_kwh):

        stored = min(
            energy_kwh * self.efficiency,
            self.capacity_kwh - self.soc
        )

        self.soc += stored

        return stored

    def discharge(self, demand_kwh):

        available = min(demand_kwh, self.soc)

        self.soc -= available

        return available

    def get_soc(self):

        return self.soc
