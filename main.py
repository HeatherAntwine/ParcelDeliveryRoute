# Heather Antwine 000425323

# RUBRIC ITEM C1
# Imports
from clock import Clock
from hashtable import HashTable
from settings import *
from truck import Truck
from warehouse import Warehouse


# Primary class for executing the code and finding the optimal route
class Simulation:
    # Initializing variables
    def __init__(self, prep):
        self.prepper = prep
        self.index_addresses = {v: k for k, v in prep.address_dictionary.items()}
        self.distances = prep.distance_matrix
        self.packages = prep.package_table
        self.hash_table = HashTable(len(self.packages) + 1)
        self.construct()
        self.time = Clock(0, 0, 0)
        self.warehouse = Warehouse(self, self.packages)
        self.truck_1 = Truck(self, 1, True, True, 41)
        self.truck_2 = Truck(self, 2, False, False, 149)
        self.trucks = []
        self.newline = "\n"
        self.end = False
        self.event = True
        self.loop = False

        # E for Display Everything
        # N for Next Event
        # P for Packages
        # S for Search for Packages
        # A for Addresses
        # F for Find Address
        self.key_bindings = ['E', 'N', 'P', 'S', 'A', 'F']

    # Print the information with a buffer for style
    def __str__(self):
        clock_buffer_2 = "-"
        if self.time.hr >= 10:
            clock_buffer_2 = ""

        # Buffers for style
        add_1 = 68
        add_2 = 60
        add_3 = 64
        add_4 = 46
        sub_1 = len(str(self.truck_1.pkg_id))
        sub_2 = len(str(self.truck_1.locations))
        sub_3 = len(str(self.truck_1.distances)) + len(str(round(self.truck_1.sum_distances, 1)))
        sub_4 = len(str(round(self.truck_1.odometer, 1))) + len(str(self.truck_1.bed_load)) + len(
            str(self.index_addresses[self.truck_1.current_location]))
        c1_r1 = self.space(19)
        c1_r2 = self.space(13)
        c1_r3 = self.space(12)
        c1_r4 = self.space(7)
        c1_r5 = self.space(7)
        c1_r6 = self.space(4, 0, "-")

        # Building the string to display information for Truck 1
        truck = self.truck_1
        c2_r1 = ""
        c2_r2 = "Packages:    " + str(truck.pkg_id) + self.space(add_1, sub_1)
        c2_r3 = "Addresses:           " + str(truck.locations) + self.space(add_2, sub_2)
        c2_r4 = "Distances:    " + str(truck.distances) + " = " + str(round(truck.sum_distances, 1)) + self.space(add_3, sub_3)
        c2_r5 = "Miles: " + str(round(truck.odometer, 1)) + "    Packages: " + str(truck.bed_load) + \
                "    Location: " + str(self.index_addresses[truck.current_location][:41]) + self.space(add_4, sub_4)
        c2_r6 = "Truck 1 -" + str(self.time) + "  " + clock_buffer_2

        # Buffers for style
        sub_5 = len(str(self.truck_2.pkg_id))
        sub_6 = len(str(self.truck_2.locations))
        sub_7 = len(str(self.truck_2.distances)) + len(str(round(self.truck_2.sum_distances, 1)))
        sub_8 = len(str(round(self.truck_2.odometer, 1))) + len(str(self.truck_2.bed_load)) + len(
            str(self.index_addresses[self.truck_2.current_location]))
        c3_r1 = self.space(25)
        c3_r2 = self.space(10)
        c3_r3 = self.space(11)
        c3_r4 = self.space(12)
        c3_r5 = self.space(12)
        c3_r6 = self.space(75)

        # Building the string to display information for Truck 2
        truck = self.truck_2
        c4_r1 = ""
        c4_r2 = "Packages:    " + str(truck.pkg_id) + self.space(add_1, sub_5)
        c4_r3 = "Addresses:           " + str(truck.locations) + self.space(add_2, sub_6)
        c4_r4 = "Route Weight: " + str(truck.distances) + " = " + str(round(truck.sum_distances, 1)) + self.space(add_3, sub_7)
        c4_r5 = "Miles: " + str(round(truck.odometer, 1)) + "    Packages: " + str(truck.bed_load) + \
                "    Location: " + str(self.index_addresses[truck.current_location][:41]) + self.space(add_4, sub_8)
        c4_r6 = "Truck 2 -" + str(self.time) + "  " + clock_buffer_2

        # Buffers for style
        c5_r1 = self.space(141)
        c5_r2 = self.space(0)
        c5_r3 = self.space(0)
        c5_r4 = self.space(4)
        c5_r5 = self.space(4)
        c5_r6 = self.space(60)

        # User's commands - will show on the interface for user friendliness
        c6_r1 = "[E] Display Everything\n"
        c6_r2 = "[N] Next Event\n"
        c6_r3 = "[P] Packages\n"
        c6_r5 = "[S] Search for Package\n"
        c6_r4 = "[A] Addresses\n"
        c6_r6 = "[F] Find Address\n"

        # R = rows, C = columns - displays the string after construction
        return c1_r1 + c2_r1 + c3_r1 + c4_r1 + c5_r1 + c6_r1 + \
            c1_r2 + c2_r2 + c3_r2 + c4_r2 + c5_r2 + c6_r2 + \
            c1_r3 + c2_r3 + c3_r3 + c4_r3 + c5_r3 + c6_r3 + \
            c1_r4 + c2_r4 + c3_r4 + c4_r4 + c5_r4 + c6_r4 + \
            c1_r5 + c2_r5 + c3_r5 + c4_r5 + c5_r5 + c6_r5 + \
            c1_r6 + c2_r6 + c3_r6 + c4_r6 + c5_r6 + c6_r6

    # O(N) runtime to display the string of a single character
    def space(self, add, sub=0, token=" "):
        buffer = ""
        for char in range(0, add - sub):
            buffer = buffer + token
        return buffer

    # O(N) runtime to build the hashtable - data is package information and IDs are keys
    def construct(self):
        for package in self.prepper.package_table[:]:
            package_data = []
            # Appending the data to be stored in the hashtable
            for index in [0, 1, 2, 4, 5, 6, 8]:
                package_data.append(package[index])
            # Status update on package
            if package[7] == '9:05 arrival time':
                package_data[-1] = "Flight Delayed"
            elif package[7] == 'Invalid Address':
                package_data[-1] = "Invalid Address"
            else:
                package_data[-1] = "Available at Warehouse"
            # ID is the key - adding the data to the hashtable
            self.hash_table[int(package[0])] = package_data

    # Primary execution function to run the entire simulation
    def execute(self):
        self.setup()
        while True:
            self.gui()
            self.time.sec_tick()
            self.special()
            for truck in self.trucks:
                self.drive(truck)
                self.load(truck)
                self.deliver(truck)

    # Set the start time for the simulation, build the truck lists, and print the information to the console.
    # O(N) runtime
    def setup(self):
        self.time.set_time(start_time)
        self.trucks.append(self.truck_1)
        self.trucks.append(self.truck_2)
        print(self.newline + str(self))

    # O(N^2) runtime for checking for any special constraints such as delayed flight and incorrect address.
    # If no constraints are found, set the package deliveries to complete
    def special(self):
        if self.time.compare_time(delay_time):
            self.warehouse.flight_arrival()
        elif self.time.compare_time(address_fix_time):
            self.warehouse.address_fixed()
        elif not self.warehouse.warehouse and not self.warehouse.do_not_ship_packages and not self.truck_1.pkg_id \
                and not self.truck_2.pkg_id:
            self.complete()

    # O(M*N!) runtime to load the truck if it's at the warehouse
    def load(self, truck):
        if truck.available and truck.bed_load == 0:
            self.warehouse.load_truck(truck)

    # O(1) runtime for 1 sec of the truck driving.
    def drive(self, truck):
        if truck.locations:
            truck.drive()

    # O(N^2) runtime for delivering a package upon arrival, loading up next destination, then printing to console.
    def deliver(self, truck):
        if truck.next_distance <= 0 and truck.locations:
            truck.deliver_pkg()
            truck.next_destination()
            truck.print_simulation()

    # O(N) runtime for user commands. The individual functions are keybound.
    def gui(self):
        while (self.event and not self.end) or self.loop:
            command = input("Key Command: ").upper()
            if command in self.key_bindings:
                if command == 'E':
                    self.end = True
                elif command == 'N':
                    self.event = False
                elif command == 'P':
                    print(self.hash_table)
                elif command == 'A':
                    self.print_data(self.prepper.address_dictionary)
                elif command == 'S':
                    self.search_package()
                elif command == 'F':
                    self.search_address()

    # O(1) runtime for function for searching for package ID and printing the information to the console.
    def search_package(self):
        while True:
            package_id = input('Input Package ID: ').upper()
            if package_id in self.key_bindings or package_id in ['STOP', 'EXIT', 'QUIT', 'LEAVE']:
                break
            try:
                if int(package_id) > 0:
                    print("\t\t\t\t" + str(self.hash_table[int(package_id)]))
            except (ValueError, KeyError, TypeError, IndexError):
                pass

    # O(N) runtime for function for searching for address and printing the information to the console.
    def search_address(self):
        while True:
            address_id = input('Input Address ID: ').upper()
            if address_id in self.key_bindings or address_id in ['STOP', 'EXIT', 'QUIT', 'LEAVE']:
                break
            try:
                if 0 <= int(address_id) <= len(self.index_addresses) - 1:
                    print("\t\t\t\t Address " + address_id + ": " + str(self.index_addresses[int(address_id)]), end='')
                    if int(address_id) == 0:
                        print("")
                    else:
                        package_list = [x[0] for x in self.packages if x[-1] == int(address_id)]
                        print(" (Package " + str((', '.join(package_list))) + ")")
            except (ValueError, KeyError, TypeError, IndexError):
                pass

    # O(1) runtime for completing the simulation and printing the information to the console.
    def complete(self):
        print("%sThe simulation has completed at%s with all the packages delivered." % (self.newline, self.time))
        print("Total miles driven is %0.4s miles." % (self.truck_1.odometer + self.truck_2.odometer))
        self.loop = True
        while self.loop:
            self.gui()

    # O(N) runtime for printing the data that needs to be displayed
    def print_data(self, data, title=""):
        print("\n" + title)
        if type(data) is list:
            for index, element in enumerate(data):
                print("Address %02d: \t%s" % (index, element))
        elif type(data) is dict:
            for key, value in data.items():
                print("Address %02d: \t%s" % (value, key))


# Reads data from the provided CSV files with a small data cleansing
class DataPrep:
    # Initializing variables
    def __init__(self):
        self.temp = None
        self.address_dictionary = {}
        self.distance_matrix = []
        self.package_table = []

    # Executing the DataPrep function
    def execute(self):
        self.build_distance_matrix()
        self.build_pkg_table()

    # Build Address disctionary and the matrix for distance
    def build_distance_matrix(self):
        self.open_file(file_distances)
        self.clean_matrix_file()
        self.delete_lead_data("\n")
        self.delete_junk_data(",")
        self.clean_matrix_addresses()
        self.build_address_dictionary()
        self.clean_matrix_elements()
        self.split_matrix_elements()
        self.transpose_matrix()
        self.assign_matrix()

    # Build the table for the packages
    def build_pkg_table(self):
        self.open_file(file_packages)
        self.clean_table_file()
        self.delete_lead_data("1")
        self.delete_junk_data("")
        self.nest_table_elements()
        self.format_special_notes()
        self.format_package_status()
        self.format_short_address()
        self.format_grouped_packages()
        self.format_address_index()

    # O(1) runtime to open the file, read the information, and assign the data to a temporary file (self.temp)
    def open_file(self, file_name):
        with open(file_name) as file_python:
            self.temp = file_python.read()

    # O(n) runtime to perform the data cleansing and split the file
    def clean_matrix_file(self):
        self.temp = self.temp.replace(",,", "")
        self.temp = self.temp.replace("\n(", "; ")
        self.temp = self.temp.replace(")", "")
        self.temp = list(self.temp.split('"'))

    # O(N^2) runtime for deleting anything before the data actually starts
    def delete_lead_data(self, stop_string):
        while self.temp[0] != stop_string:
            del self.temp[0]

    # O(N^2) runtime for deleting trash data.
    def delete_junk_data(self, junk_string):
        while junk_string in self.temp:
            self.temp.remove(junk_string)

    # O(N^2) runtime for removing the unused A column from the data and sets the warehouse's index to 0 and 1
    def clean_matrix_addresses(self):
        for index in range(len(self.temp) - 3, -1, -3):
            del self.temp[index]
        self.temp[0] = 'Warehouse'
        self.temp[1] = ',0.0\n'

    # O(N^2) runtime for buiildng the address dictionary.
    def build_address_dictionary(self):
        address_list = []
        for index in range(len(self.temp) - 2, -1, -2):
            address_list.insert(0, self.temp.pop(index).strip())
        for index, address in enumerate(address_list):
            self.address_dictionary[address] = index

    # O(N^2) for cleaning up the format of the matrix
    def clean_matrix_elements(self):
        for index, element in enumerate(self.temp):
            tokens = list(element)
            del tokens[0]
            while tokens[-1] != '0':
                del tokens[-1]
            self.temp[index] = ("".join(tokens))

    # O(N^2) runtime for splitting the matrix into separate lists.
    def split_matrix_elements(self):
        for index, element in enumerate(self.temp):
            self.temp[index] = self.temp[index].split(",")

    # O(N^2) runtime for transposing the matrix to build a perfect square matrix
    def transpose_matrix(self):
        for index, row in enumerate(self.temp):
            while len(row) < len(self.temp[-1]):
                self.temp[index].append(True)
        for x in range(len(self.temp)):
            for y in range(x, len(self.temp[-1])):
                self.temp[x][y] = self.temp[y][x]

    # O(N^2) runtime for assigning the matrix list and changing the elements to float data types
    def assign_matrix(self):
        self.distance_matrix = [[float(element) for element in nested_list] for nested_list in self.temp]

    # O(N) runtime to clean the table data by splitting it into a list of strings for the constraints
    def clean_table_file(self):
        self.temp = self.temp.replace(",,", "")
        self.temp = self.temp.replace(", ", " & ")
        self.temp = self.temp.replace("\n", ",")
        self.temp = self.temp.replace("5383 South", "5383 S")
        self.temp = self.temp.replace("Delayed on flight--will not arrive to depot until 9:05 am", "9:05 arrival time")
        self.temp = self.temp.replace("Must be delivered with", "Group")
        self.temp = self.temp.replace("Can only be on truck", "Truck")
        self.temp = self.temp.replace("Wrong address listed", "Invalid Address")
        self.temp = list(self.temp.split(","))

    # O(N^3) runtime for building the lists with the package data
    def nest_table_elements(self):
        while self.temp:
            self.package_table.append([])
            stop_string = str(int(self.temp[0]) + 1)
            for index, element in enumerate(self.temp[:]):
                if element == stop_string and self.temp[1] != stop_string:
                    break
                self.package_table[-1].append(self.temp.pop(0))

    # O(N) runtime for setting the final element to Empty for if there are not special notes or constraints
    def format_special_notes(self):
        for element in self.package_table:
            if len(element) <= 7:
                element.append("Empty")

    # O(N) runtime for setting the last element as status for now
    def format_package_status(self):
        for element in self.package_table:
            element.append("Status")

    # O(N) runtime for shortening the address and assigning as final element - street and zip only
    def format_short_address(self):
        for element in self.package_table:
            element.append(element[1] + "; " + element[4])

    # O(N^2) runtime for grouping the packages that have special notes or constraints - spatial
    def format_grouped_packages(self):
        # O(N*K) runtime for pairing up the special notes packages
        group_pairs = []
        for element in self.package_table:
            if element[7][0:6] == '"Group':
                group_pairs.append(str(element[7][6:]).strip())
                element[7] = "Group"

        # O(N^2) runtime for locating the IDs for the packages with constraints
        group_ids = []
        for element in group_pairs:
            package_id = ""
            for index, char in enumerate(element):
                try:
                    package_id = package_id + str(int(char))
                except ValueError:
                    if package_id != "":
                        group_ids.append(package_id)
                        package_id = ""

        # O(N) runtime for adding the IDs of these constrained packages to the group
        for element in self.package_table:
            if element[0] in group_ids:
                element[7] = "Group"

    # O(N) runtime for setting the address as the final element
    def format_address_index(self):
        for element in self.package_table:
            element.append(self.address_dictionary.get(element[9]))

    # O(N) runtime for displaying the data in the console
    def print_data(self, data, title=""):
        print("\n" + title)
        if type(data) is list:
            for index, element in enumerate(data):
                print("Index %02d: \t%s" % (index, element))
        elif type(data) is dict:
            for key, value in data.items():
                print("Index %02d: \t%s: %s" % (value, key, value))


prepper = DataPrep()
prepper.execute()
simulation = Simulation(prepper)
simulation.execute()

# TODO