# Heather Antwine 000425323


# RUBRIC ITEM D
# Hash Table has been chosen as the primary data structure for storing the package data


# Class Hashtable for package information
class HashTable:
    # Initializing variables
    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size  # package IDs
        self.data = [None] * self.size  # package data

    # O(1) runtime to find hashtable length
    def __len__(self):
        return int(self.size)

    # O(1) runtime to see if the hashtable contains the key being searched for
    def __contains__(self, key):
        if self.__getitem__(key) is None:
            return False
        return True

    # Getters and Setters
    # O(1) runtime to fetch hashtable data
    def __getitem__(self, key):
        return self.get(key)

    # O(1) runtime to put hashtable data
    def __setitem__(self, key, data):
        self.put(key, data)

    # O(N) runtime to return a string that contains the slots that are occupied and the corresponding data
    def __str__(self):
        table_string = "\nPackage Hashtable \n    [ID, Street, City, Zip Code, Time Req, Weight, Location]\n"
        for slot in self.slots:
            if slot is None:
                continue
            table_string = table_string + "Package " + repr(slot) + ": " + repr(self.get(slot)) + "\n"
        return table_string

    # O(1) runtime to put the key and slots' data in the hashtable
    def put(self, key, data):
        hash_value = self.hash_fx(key, len(self.slots))
        hash_value_start = hash_value

        # RUBRIC ITEM B6
        # Once the hashtable is 83% filled, it will double in size
        # To speed up the program, increase the load_factor so it doesn't resize as often
        load_factor = len([a for a in self.data if a is not None]) / len(self)
        if load_factor >= .83:
            temp_slots = [None] * self.size
            temp_data = [None] * self.size
            self.size *= 2
            self.slots = self.slots + temp_slots
            self.data = self.data + temp_data

        # Sets key and data if the hash_value is None
        if self.slots[hash_value] is None:
            self.slots[hash_value] = key
            self.data[hash_value] = data
        else:
            # Sets the data if the hash_value is fonud to be equal to the key
            if self.slots[hash_value] == key:
                self.data[hash_value] = data
            else:
                # Rehashes the hash_value is it isn't empty AND it cannot find a match
                next_slot = self.rehash(hash_value, len(self.slots))
                while self.slots[next_slot] is not None and self.slots[next_slot] != key:
                    next_slot = self.rehash(next_slot, len(self.slots))
                # Sets the key and data
                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = data
                else:
                    self.data[next_slot] = data

    # O(1) runtime for searching then returning the proper data or, if the key is never found, None
    def get(self, key):
        start_slot = self.hash_fx(key, len(self.slots))
        position = start_slot
        while self.slots[position] is not None:
            if self.slots[position] == key:
                return self.data[position]
            position = self.rehash(position, len(self.slots))
            if position == start_slot:
                return None

    # O(1) runtime for hashing the value
    def hash_fx(self, key, size):
        return key % size

    # O(1) runtime for dealing with collisions when hashing.
    def rehash(self, bad_hash, size):
        return (bad_hash + 3) % size

    # TODO
    # hash_fx STATIC?
    # rehash STATIC?
