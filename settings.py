# Settings per the Project Instructions
# The time the simulation will start
start_time = "8:00:00"

# The time that the packages that are delayed will arrive
delay_time = "9:05:00"

# The time that the invalid address will be fixed
address_fix_time = "10:20:00"

# The maximum load of the truck beds
truck_max_load = 16

# The speed of the truck in mph and mps
truck_mph = 18
truck_mps = ((truck_mph / 60) / 60)


max_int = 99999
file_distances = 'Distances.csv'
file_packages = 'Packages.csv'

# seed_count can be changed
# Too low will result in the function being restarted many times due to packages not arriving on time
seed_count = 19

# From the PDF:
# Each truck can carry 16 packages max
# Trucks average speed are 18mph
# Trucks are powered by perpetual engines so no fuel requirements
# Drivers remain with trucks
# Drivers leave warehouse at 0800 with the truck already loaded and can return to the warehouse PRN
# Simulation is complete once all 40 packages have been delivered
# Delivery time is instantaneous
# Maximum of 1 special note per package
# Invalid address will be fixed at 1020
# Package IDs are unique - no collisions

# TODO
