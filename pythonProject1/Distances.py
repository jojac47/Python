import csv

# store csv's in data files

from datetime import datetime, timedelta


# get the distance data into a distance list
def load_distance_data(filename_dv):
    distance_list = []
    # The below loops read in the CSV files as two separate lists
    with open(filename_dv) as Distances_CSV:
        distance_data = csv.reader(Distances_CSV, delimiter=",")
        for i in distance_data:
            distance_list.append(i)
    return distance_list


# load name data into a name list
def load_name_data(filename_dn):
    name_list = []
    with open(filename_dn) as Names_CSV:
        name_data = csv.reader(Names_CSV, delimiter="/")
        for i in name_data:
            name_list.append(i)
    return name_list


# This method is going to return the distance between 2 values using the distance csv
def get_distance_value(current_distance_index, next_distance_index, distance_list):
    # this is going to check to see if the current distance index is less than the next destination index
    # This is because of the way the table is set up and to ensure value stays in bounds by flipping the index order
    if current_distance_index < next_distance_index:
        distance_value = distance_list[next_distance_index][current_distance_index]
    if current_distance_index >= next_distance_index:
        distance_value = distance_list[current_distance_index][next_distance_index]

    return float(distance_value)


# this method is to keep track of the total distance traveled. Much like the above method except it keeps a running
# total.

def get_total_distance_value(current_distance_index, next_distance_index, total_distance, distance_list,
                             truck_start_time, package):
    # default truck speed
    truck_speed_mph = 18
    # how many minutes it takes the truck to go 1 mile
    truck_speed_minutes_per_mile = 60 / truck_speed_mph

    # number of seconds per mile traveled
    truck_speed = truck_speed_minutes_per_mile * 60

    # get the distance value by matching the name to the distance column. its 2 functions because the data is a half
    # table.
    if current_distance_index < next_distance_index:
        distance_value = distance_list[next_distance_index][current_distance_index]

    if current_distance_index >= next_distance_index:
        distance_value = distance_list[current_distance_index][next_distance_index]
    # total distance so far
    total_distance += float(distance_value)
    # Time in seconds it takes to get to the next stop
    next_distance_time_seconds = float(distance_value) * truck_speed
    # set the time as a time delta
    next_distance_time_seconds = timedelta(seconds=next_distance_time_seconds)
    # add this time to the current time to get the time the truck is delivered
    next_distance_arrival_time = truck_start_time + next_distance_time_seconds
    # set the time in the hash table
    package.p_delivery_time = next_distance_arrival_time
    # return the total distance and the next arrival time
    return total_distance, next_distance_arrival_time


# this method returns the closest next location index, next location name, and distance to next location
def get_shortest_distance_value(current_distance_index, names_list, distance_list, packages):
    # place holder for the shortest distance value and shortest name indexes
    shortest_distance = 20
    shortest_address_index = "holder"
    shortest_address_name = "holder"

    # Loop through every entry in names_list

    for package in packages:
        next_distance_index = get_name_index(names_list, package.pAddress)

        next_package_distance = get_distance_value(current_distance_index, next_distance_index[0], distance_list)
        # if the package is the shortest distance store the value
        if next_package_distance < shortest_distance:
            shortest_distance = next_package_distance
            shortest_address_index = next_distance_index[0]
            shortest_address_name = package.pAddress

    return shortest_address_index, shortest_distance, shortest_address_name


# This will take the names_list form the distance.csv table and match it with the package.csv entry and return the
# address index for other methods to use
def get_name_index(names_list, location_name):
    for name in names_list:

        if location_name in name[1]:
            name_index = names_list.index(name)

        if location_name[0:6] in name[1]:
            name_index = names_list.index(name)

    return name_index, location_name
