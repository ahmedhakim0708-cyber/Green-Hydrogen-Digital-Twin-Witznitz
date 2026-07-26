from models.solar import SolarPlant
from models.battery import Battery
from models.electrolyzer import Electrolyzer


class DigitalTwin:

    def __init__(self, solar, battery, electrolyzer):
        self.solar = solar
        self.battery = battery
        self.electrolyzer = electrolyzer

    def run(self, hours_per_month=None):
        """
        PV feeds the electrolyzer directly.
        The battery only buffers surplus / covers deficit.
        """
        if hours_per_month is None:
            hours_per_month = [744, 672, 744, 720, 744, 720,
                               744, 744, 720, 744, 720, 744]

        hydrogen = []

        for energy, hours in zip(self.solar.monthly_energy_output(), hours_per_month):

            capacity = self.electrolyzer.max_energy_intake(hours)

            to_stack = min(energy, capacity)     # direct PV -> electrolyzer
            surplus = energy - to_stack         # PV the stack cannot absorb
            deficit = capacity - to_stack       # stack headroom PV did not fill

            if surplus > 0:
                self.battery.charge(surplus)
            elif deficit > 0:
                to_stack += self.battery.discharge(deficit)

            hydrogen.append(self.electrolyzer.produce_hydrogen(to_stack))

        return hydrogen
