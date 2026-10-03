import pandas as pd

HOURS_PER_DAY = 24


class DigitalTwin:
    """
    Monthly energy balance of the PV + BESS + AWE plant.

    Operating modes
    ---------------
    "grid_assisted" : the electrolyzer follows the production target
                      (13 t/day x availability, limited by rated power).
                      PV deficits are imported from the grid, PV surpluses
                      are exported (configuration described in the thesis).
    "pv_only"       : the electrolyzer only uses PV energy (direct + BESS).
                      Surplus PV that the electrolyzer cannot absorb is
                      exported, nothing is imported.

    Limitation: a monthly balance nets day/night flows inside each month,
    so grid import AND export are both underestimated compared with an
    hourly simulation.
    """

    def __init__(self, solar, battery, electrolyzer, months, days_per_month,
                 h2_target_kg_per_day=None):
        self.solar = solar
        self.battery = battery
        self.electrolyzer = electrolyzer
        self.months = list(months)
        self.days = list(days_per_month)
        self.h2_target_kg_per_day = h2_target_kg_per_day

    def run(self, mode="grid_assisted", year=1):
        if mode not in ("grid_assisted", "pv_only"):
            raise ValueError("mode must be 'grid_assisted' or 'pv_only'")

        rows = []
        pv_monthly = self.solar.monthly_energy_output(year)

        for month, days, pv in zip(self.months, self.days, pv_monthly):
            hours = days * HOURS_PER_DAY
            capacity = self.electrolyzer.max_energy_intake(hours)

            # BESS daily cycling (evening-peak bridging) -> conversion losses
            bess_in, bess_out, bess_loss = self.battery.monthly_shift(days, pv)
            pv_net = pv - bess_loss

            if mode == "grid_assisted" and self.h2_target_kg_per_day:
                target_energy = self.electrolyzer.energy_for_hydrogen(
                    self.h2_target_kg_per_day * days * self.electrolyzer.availability)
                demand = min(target_energy, capacity)
            else:
                demand = capacity

            from_pv = min(pv_net, demand)
            grid_import = demand - from_pv if mode == "grid_assisted" else 0.0
            grid_export = pv_net - from_pv
            to_stack = from_pv + grid_import

            rows.append({
                "Month": month,
                "PV_kWh": pv,
                "BESS_throughput_kWh": bess_out,
                "BESS_losses_kWh": bess_loss,
                "PV_to_electrolyzer_kWh": from_pv,
                "Grid_import_kWh": grid_import,
                "Grid_export_kWh": grid_export,
                "Electrolyzer_kWh": to_stack,
                "Hydrogen_kg": self.electrolyzer.produce_hydrogen(to_stack),
                "Load_factor": to_stack / (self.electrolyzer.rated_power_kw * hours),
            })

        return pd.DataFrame(rows)
