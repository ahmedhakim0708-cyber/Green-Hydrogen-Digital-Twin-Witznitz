class Battery:
    """
    LFP Battery Energy Storage System.

    Two uses:
    * charge() / discharge(): step-by-step operation (ready for an hourly model)
    * monthly_shift(): monthly approximation - the BESS performs one daily
      cycle (evening-peak bridging) and therefore shifts at most
      usable_capacity x cycles_per_day x days per month. It does NOT carry
      energy from one month to the next (no seasonal storage).
    """

    def __init__(self, capacity_kwh, dod=0.9, charge_efficiency=0.95,
                 discharge_efficiency=0.97, cycles_per_day=1):
        self.capacity_kwh = capacity_kwh
        self.dod = dod
        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency
        self.cycles_per_day = cycles_per_day
        self.min_soc_kwh = capacity_kwh * (1 - dod)
        self.soc_kwh = self.min_soc_kwh

    @property
    def usable_capacity_kwh(self):
        return self.capacity_kwh * self.dod

    @property
    def round_trip_efficiency(self):
        return self.charge_efficiency * self.discharge_efficiency

    def charge(self, energy_in_kwh):
        """Charge from the AC bus. Returns the energy taken from the bus (kWh)."""
        room = self.capacity_kwh - self.soc_kwh
        stored = min(energy_in_kwh * self.charge_efficiency, room)
        self.soc_kwh += stored
        return stored / self.charge_efficiency

    def discharge(self, demand_kwh):
        """Discharge to the AC bus. Returns the energy delivered (kWh)."""
        available = (self.soc_kwh - self.min_soc_kwh) * self.discharge_efficiency
        delivered = min(demand_kwh, available)
        self.soc_kwh -= delivered / self.discharge_efficiency
        return delivered

    def monthly_shift(self, days, pv_energy_kwh):
        """
        Monthly approximation.
        Returns (energy charged from PV, energy delivered, losses) in kWh.
        """
        if self.capacity_kwh <= 0:
            return 0.0, 0.0, 0.0
        delivered_max = (self.usable_capacity_kwh * self.cycles_per_day * days
                         * self.discharge_efficiency)
        charged = min(delivered_max / self.round_trip_efficiency, pv_energy_kwh)
        delivered = charged * self.round_trip_efficiency
        return charged, delivered, charged - delivered

    def get_soc(self):
        return self.soc_kwh
