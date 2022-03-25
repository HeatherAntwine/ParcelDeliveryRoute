# Heather Antwine 000425323

# imports
from settings import *


# Class Truck deals with package deliveries
class Truck:
    # Initializing variables
    def __init__(self, sim, identifier, available, final_trip, buffer):
        self.simulation = sim
        self.identifier = identifier
        self.available = available  # Is the truck available
        self.final_trip = final_trip  # Note the final trip
        self.buffer = self.simulation.space(buffer)  # Buffer for style
        self.odometer = 0.000  # Current miles driven
        self.next_distance = 0
        self.current_location = 0  # Current Location
        self.bed_load = 0  # How many packages are loaded
        self.bed = []  # Package Data
        self.pkg_id = []
        self.next_pkg = []  # Which package is being delivered next
        self.locations = []  # Route
        self.distances = []  # Individual distances to be traveled
        self.sum_distances = 0.0  # Sum of the distances to be traveled

    # O(1) runtime for 1 second of truck drive time
    def drive(self):
        self.odometer = self.odometer + truck_mps
        self.next_distance = self.next_distance - truck_mps

    # O(N^2) runtime to deliver packages with addresses that match the location then remove it from the hashtable
    def deliver_pkg(self):
        self.next_pkg = []
        for package in self.bed[:]:
            if package[-1] == self.locations[0]:
                self.simulation.hash_table[int(package[0])][-1] = "Package delivered at: " + str(self.simulation.time)
                self.next_pkg.append(package[0])
                self.bed_load = self.bed_load - 1
                self.pkg_id.pop(0)
                self.bed.remove(package)

    # O(N) runtime for updating the truck's location and trajectory
    def next_destination(self):
        # The runtime is O(N)
        self.current_location = self.locations.pop(0)
        self.distances.pop(0)
        if self.distances:
            self.next_distance = self.next_distance + self.distances[0]
            self.sum_distances = sum(self.distances)
        else:
            self.sum_distances = 0.0
            if self.current_location == 0:
                self.available = True

    # O(N) runtime for printing data to console.
    def print_simulation(self):
        if self.available and self.current_location == 0:
            print(self.simulation.newline + self.buffer + "[Truck at warehouse]")
        else:
            print(self.simulation.newline + self.buffer + "[Package has been delivered: " + str(', '.join(self.next_pkg)) + "]")
        print(self.simulation)
        self.simulation.event = True

        # TODO