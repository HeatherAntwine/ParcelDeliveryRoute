# Heather Antwine 000425323

# Imports
import collections
import random
from settings import *


# Class Warehouse where all packages are stored until ready to be loaded
class Warehouse:
    # Initializing variables
    def __init__(self, sim, import_packages):
        self.simulation = sim
        self.truck = None
        self.fastest_route = [max_int, [max_int], max_int]
        self.subset_matrix = []
        self.basecase = []
        self.urgent_addresses = []
        self.unique_count = 0
        self.do_not_ship_packages = []
        self.do_not_ship_addresses = []
        self.do_not_ship(import_packages[:])
        self.warehouse = [x for x in import_packages if
                          x not in self.do_not_ship_packages]
        self.reset = False

    # O(N^2) runtime for locating the packages with incorrect addresses or constraints.
    def do_not_ship(self, packages):
        # O(N) runtime to remove invalid data
        for package in packages:
            for index in [9, 6, 4, 3, 2, 1]:
                package.pop(index)

        # O(N) runtime to remove any invalid packages from the warehouse
        for package in packages[:]:
            if package[2] == "Dropped 9:05":
                self.do_not_ship_packages.append(package)
                self.do_not_ship_addresses.append(package[-1])
                packages.remove(package)

        # O(N) runtime to remove constrained packages from the warehouse
        for package in packages[:]:
            if package[-1] in self.do_not_ship_addresses:
                package[3] = "Unavailable at WHS"
                self.do_not_ship_packages.append(package)
                packages.remove(package)

        # O(N) runtime to remove invalid packages from the warehouse
        for package in packages[:]:
            if package[2] == "Invalid Address":
                self.do_not_ship_packages.append(package)
                self.do_not_ship_addresses.append(package[-1])
                packages.remove(package)

    # O(M*N) runtime to hold the functions for the truck
    def load_truck(self, truck):

        # Truck arriving at warehouse
        self.truck_final_trip(truck)
        bed, ids, indexes, warehouse, count = self.setup_variables()
        bed, ids, indexes, warehouse, count = self.truck_specific_packages(bed, ids, indexes, warehouse, count)

        # Truck loaded with packages that have time constraints (deadlines)
        bed, ids, indexes, warehouse, count = self.load_urgent_packages(bed, ids, indexes, warehouse, count)
        bed, ids, indexes, warehouse, count = self.load_address_pairs(bed, ids, indexes, warehouse, count)
        bed, ids, indexes, warehouse, count = self.unique_max_load(bed, ids, indexes, warehouse, count, True)
        bed, ids, indexes, warehouse, count = self.duplicate_max_load(bed, ids, indexes, warehouse, count)

        # More packages loaded to truck
        bed, ids, indexes, warehouse, count = self.seed_package_selector(bed, ids, indexes, warehouse, count)

        # Use the Hamiltonian Circuit Method of determining the best route to take.
        uniques = self.hamiltonian_circuit_setup(indexes, count, False)

        # Truck departing warehouse, packages now out for delivery
        self.finalize_variables(uniques, bed)
        self.finalize_truck(count, bed)

    # O(1) runtime for defining if truck will not make another trip.
    def truck_final_trip(self, truck):
        self.truck = truck
        if self.truck.identifier == 1 or len(self.warehouse) <= truck_max_load:
            self.truck.final_trip = True

    # O(K) runtime to re-setup the variables for the class and construct the variables for the functions again
    def setup_variables(self):
        self.basecase = []
        self.subset_matrix = []
        self.basecase = []
        self.urgent_addresses = []
        self.unique_count = 0
        self.fastest_route = [max_int, [max_int], max_int]
        self.reset = False
        count = 0
        bed = []
        ids = []
        indexes = []
        warehouse = self.warehouse[:]
        return bed, ids, indexes, warehouse, count

    # This will remove all packages specific to truck 2 from available packages if Truck ID is 1.
    # O(N^3) runtime to remove packages/addresses from the bed for truck 1 if the packages have the 'truck2' constraint
    def truck_specific_packages(self, bed, ids, indexes, warehouse, count):
        if self.truck.identifier == 1:
            for package in warehouse[:]:
                if package[2] == "Truck 2":
                    warehouse.remove(package)
                    for pair in warehouse[:]:
                        if pair[-1] == package[-1]:
                            warehouse.remove(pair)

        return bed, ids, indexes, warehouse, count

    # O(N^2) runtime to load up the addresses with various constraints
    def load_urgent_packages(self, bed, ids, indexes, warehouse, count):
        for package in warehouse[:]:
            if package[1] != "EOD" or package[2] == "Group":
                bed, ids, indexes, warehouse, count = self.loading(package, bed, ids, indexes, warehouse, count)
                self.urgent_addresses.append(package[-1])
        return bed, ids, indexes, warehouse, count

    # O(N^2) runtime to load the packages matching the addresses from load_urgent_packages
    def load_address_pairs(self, bed, ids, indexes, warehouse, count):
        if count > 0:
            for package in warehouse[:]:
                if package[-1] in indexes:
                    bed, ids, indexes, warehouse, count = self.loading(package, bed, ids, indexes, warehouse, count)

        return bed, ids, indexes, warehouse, count

    # O(N^2) runtime to remove packages if the truck is at its max load
    def unique_max_load(self, bed, ids, indexes, warehouse, count, urgent):
        if count > truck_max_load:
            duplicate = [k for k, v in collections.Counter(indexes).items() if v > 1]
            for package in bed[:]:
                if package[2] != "Group" and package[-1] not in duplicate and urgent:
                    bed, ids, indexes, warehouse, count = self.unloading(package, bed, ids, indexes, warehouse, count)
                elif package[1] == 'EOD' and package[2] != "Group" and package[-1] not in duplicate:
                    bed, ids, indexes, warehouse, count = self.unloading(package, bed, ids, indexes, warehouse, count)
                if count <= truck_max_load:
                    break
        return bed, ids, indexes, warehouse, count

    # Remove packages if the truck is at its max load - matches addresses found in unique_max_load
    def duplicate_max_load(self, bed, ids, indexes, warehouse, count):
        while count > truck_max_load:
            for package in bed[:]:
                if package[2] != "Group":
                    for pair in bed[:]:
                        if pair[-1] == package[-1]:
                            bed, ids, indexes, warehouse, count = self.unloading(pair, bed, ids, indexes, warehouse, count)
                    break
        return bed, ids, indexes, warehouse, count

    # O(M*N!) runtime for seeding the packages - randomly selects a package and then use the function for distance
    def seed_package_selector(self, bed, ids, indexes, warehouse, bed_load):
        if bed_load == 16:
            return bed, ids, indexes, warehouse, bed_load
        print("\nSelecting the most optimal packages to load onto truck " + str(self.truck.identifier) + ".")

        # O(K) runtime for reset and best variables declaration
        reset_bed, reset_ids, reset_indexes, reset_warehouse, reset_count = bed[:], ids[:], indexes[:], warehouse[:], bed_load
        best, best_bed, best_ids, best_indexes, best_warehouse, best_count = [max_int], None, None, None, None, None

        # O(M*N!) runtime for the seeding
        for seed in range(1, seed_count + 1):
            bed, ids, indexes, warehouse, bed_load = reset_bed[:], reset_ids[:], reset_indexes[:], reset_warehouse[:], reset_count
            bed, ids, indexes, warehouse, bed_load = self.seed_random_sample(bed, ids, indexes, warehouse, bed_load)
            bed, ids, indexes, warehouse, bed_load = self.load_address_pairs(bed, ids, indexes, warehouse, bed_load)
            bed, ids, indexes, warehouse, bed_load = self.unique_max_load(bed, ids, indexes, warehouse, bed_load, False)
            bed, ids, indexes, warehouse, bed_load = self.duplicate_max_load(bed, ids, indexes, warehouse, bed_load)
            bed, ids, indexes, warehouse, bed_load, best, record = self.seed_minimum(bed, ids, indexes, warehouse, bed_load, best, seed)
            if record:
                best_bed, best_ids, best_indexes, best_warehouse, best_count = bed, ids, indexes, warehouse, bed_load
            if len(warehouse) == 0:
                break

        return best_bed, best_ids, best_indexes, best_warehouse, best_count

    # O(N^2) runtime for loading the truck with the random packages seeded in
    def seed_random_sample(self, bed, ids, indexes, warehouse, bed_load):
        try:
            random_sample = random.sample(warehouse, truck_max_load - bed_load)
        except ValueError:
            random_sample = random.sample(warehouse, len(warehouse))
        for package in random_sample:
            bed, ids, indexes, warehouse, bed_load = self.loading(package, bed, ids, indexes, warehouse, bed_load)
        return bed, ids, indexes, warehouse, bed_load

    # O(K) runtime for determining the lowest possible distance for the packages being delivered - Hamiltonian Circuit
    def seed_minimum(self, bed, ids, indexes, warehouse, bed_load, best, seed):
        if self.fastest_route[0] < best[0]:
            best = self.fastest_route[:]
        self.hamiltonian_circuit_setup(indexes, bed_load, True)
        if self.fastest_route[0] < best[0]:
            print("Calculation " + str(seed) + " -- Fastest Route " +
                  str(self.fastest_route[0]) + " -- Packages-- " + str(ids))
            record = True
        else:
            print("Calculation " + str(seed) + " --")
            record = False
        return bed, ids, indexes, warehouse, bed_load, best, record

    # O(N!) runtime for setting up the Hamiltonian Circuit variables
    def hamiltonian_circuit_setup(self, indexes, bed_load, fast):
        unique_addresses = list(set(indexes))
        unique_addresses.append(0)
        unique_addresses.sort()
        self.subset_matrix = []
        for row_index in unique_addresses:
            subset = []
            row = self.simulation.distances[row_index]
            for col_index in unique_addresses:
                subset.append(row[col_index])
            self.subset_matrix.append(subset)
        self.unique_count = len(unique_addresses)
        self.basecase = [True] * self.unique_count
        bitmap = [False] * self.unique_count
        bitmap[0] = True

        # 2 versions of the Hamiltonian Circuit were used. One is for only miles and the other (slow) for a history
        if fast:
            self.hamiltonian_circuit_fast(bitmap, 0, 0)
        else:
            self.hamiltonian_circuit_slow(bitmap, 0, 0, [], [0])

        return unique_addresses

    # O(N!) runtime for the faster version of the Hamiltonian Circuit.
    def hamiltonian_circuit_fast(self, bitmap, position, cost):
        if bitmap == self.basecase:
            if self.truck.final_trip:
                cost = round(cost, 2)
            else:
                cost = round(cost + self.subset_matrix[position][0], 2)
            if cost < self.fastest_route[0]:
                self.fastest_route[0] = cost
                return
        if cost >= self.fastest_route[0]:
            return
        for _next in range(1, self.unique_count):
            if not bitmap[_next]:
                new_bitmap = bitmap[:]
                new_bitmap[_next] = True
                self.hamiltonian_circuit_fast(new_bitmap, _next, cost + self.subset_matrix[position][_next])

    # O(N!) runtime for the slower version of the Hamilatonian Circuit
    # This version is slower because it keeps a history of the location and distance.
    def hamiltonian_circuit_slow(self, bitmap, position, cost, distances, locations):
        if bitmap == self.basecase:
            for location in locations[len(locations):]:
                if location == 21:
                    return
            if self.truck.final_trip:
                cost = round(cost, 2)
            else:
                locations.append(0)
                distances.append(self.subset_matrix[position][0])
                cost = round(cost + self.subset_matrix[position][0], 2)
            if cost <= self.fastest_route[0]:
                self.fastest_route[0] = cost
                self.fastest_route[1] = locations
                self.fastest_route[2] = distances
                return
        if cost > self.fastest_route[0]:
            return
        for _next in range(1, self.unique_count):
            if not bitmap[_next]:
                new_bitmap = bitmap[:]
                new_locations = locations[:]
                new_distances = distances[:]
                new_bitmap[_next] = True
                new_locations.append(_next)
                new_distances.append(self.subset_matrix[position][_next])
                new_cost = cost + self.subset_matrix[position][_next]
                self.hamiltonian_circuit_slow(new_bitmap, _next, new_cost, new_distances, new_locations)

    # O(N^2) runtime for checking package delivery times against constraints before even loading them up
    def finalize_variables(self, uniques, bed):
        for indexes, location in enumerate(self.fastest_route[1][:]):
            self.fastest_route[1][indexes] = uniques[location]
        if self.fastest_route[1][-2] in self.urgent_addresses and self.truck.identifier == 2:
            print("Calculation error based upon constraints. Attempting function again.")
            self.reset = True
        else:
            for package in bed:
                self.warehouse.remove(package)

    # O(N^2) runtime for loading the packages into the truck - includes history for location and distance
    def finalize_truck(self, bed_load, bed):
        if self.reset:
            self.load_truck(self.truck)
            return
        self.truck.bed_load = bed_load
        self.truck.available = False
        self.truck.locations = self.fastest_route[1][:]
        self.truck.locations.pop(0)
        self.truck.distances = self.fastest_route[2][:]
        self.truck.cost = self.fastest_route[0]
        for indexes in self.fastest_route[1]:
            for package in bed:
                if package[-1] == indexes:
                    self.truck.pkg_id.append(int(package[0]))
                    self.truck.bed.append(package)
        self.truck.next_distance = self.truck.distances[0]
        for package in self.truck.pkg_id:
            self.simulation.hash_table[package][-1] = "Loaded on Truck " + str(self.truck.identifier)
        print("\n\n\n\n\n\n" + self.truck.buffer + "[Departed WHS Fully Loaded]\n" + str(self.simulation))
        self.simulation.event = True

    # O(N) runtime for unloading a package from the truck's holding area
    def unloading(self, package, bed, ids, indexes, warehouse, bed_load):
        bed.remove(package)
        ids.remove(package[0])
        indexes.remove(package[-1])
        warehouse.append(package)
        bed_load = bed_load - 1
        return bed, ids, indexes, warehouse, bed_load

    # O(N) runtime for loading the package into the truck's holding area
    def loading(self, package, bed, ids, indexes, warehouse, bed_load):
        bed.append(package)
        ids.append(package[0])
        indexes.append(package[-1])
        warehouse.remove(package)
        bed_load = bed_load + 1
        return bed, ids, indexes, warehouse, bed_load

    # This will transform all the dleayed packages located in the Warehouse.
    # It also will make Truck 2 available. Runtime is O(N^2)

    # O(N^2) runtime for moving newly flown in packages to the warehouse
    def flight_arrival(self):
        self.simulation.truck_2.available = True
        for package in self.do_not_ship_packages[:]:
            if package[2] != "Invalid Address":
                available = self.do_not_ship_packages.pop(0)
                try:
                    self.do_not_ship_addresses.remove(available[-1])
                except ValueError:
                    pass
                self.simulation.hash_table[int(available[0])][-1] = "Available at Warehouse"
                self.warehouse.append(available)
        print("\n DELAYED PACKAGES NOW AVAILABLE AT WAREHOUSE -" + str(self.simulation.time) + ".")
        self.simulation.event = True
        self.simulation.gui()

    # O(N^2) runtime for fixing the addresses that were incorrect
    def address_fixed(self):
        for package in self.do_not_ship_packages[:]:
            if package[-2] == "Invalid Address":
                package[-1] = "410 S State St; 84111"
            available = self.do_not_ship_packages.pop(0)
            try:
                self.do_not_ship_addresses.remove(available[-1])
            except ValueError:
                pass
            self.simulation.hash_table[int(available[0])][-1] = "Available at Warehouse"
            self.simulation.hash_table[int(available[0])][1] = "410 S State St"
            self.simulation.hash_table[int(available[0])][3] = "84111"
            self.warehouse.append(available)
        print("\n PACKAGES WITH INVALID ADDRESSES ARE NOW FIXED AND AVAILABLE AT WAREHOUSE -"
              + str(self.simulation.time) + ".")
        self.simulation.event = True

        # TODO