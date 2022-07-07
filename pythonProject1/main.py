#Joseph Jackso, Student Id: 001227749
from datetime import datetime
import datetime
import Distances
from HashTable import ChainingHashTable
from Package import Package
from Trucks import Trucks

#Space complexity 3N  Time O
# initialize excel data lists and hash table
myHash = ChainingHashTable()
distance_list = []
names_list = []

# Load Packages into the hash table
Package.load_Package("packages.csv", myHash)

# Load in the data files from the distance table as
distance_list = Distances.load_distance_data("distances.csv")
names_list = Distances.load_name_data("names.csv")

# set up the ques based on delivery time requirements
Trucks.get_ques(myHash.table)

# Load the packages on the trucks
truck_loads = Trucks.load_trucks(myHash, names_list, distance_list)

# This is going to call the Get Total Distance method and also keep track of time as it passes along with distance.

# initialize the first trucks distance, set the current distance index for the hub to start the day and set the
# delivery start time to when the truck leaves the hub
total_distance_truck1 = 0
truck1_current_distance_index = 0
delivery_start_time_t1 = datetime.timedelta(hours=8, minutes=0, seconds=0)

for package in truck_loads[0]:
    next_index = Distances.get_name_index(names_list, package.pAddress)[0]

    total_distance_truck1_info = Distances.get_total_distance_value(truck1_current_distance_index, next_index,
                                                                    total_distance_truck1, distance_list,
                                                                    delivery_start_time_t1, package)
    total_distance_truck1 = total_distance_truck1_info[0]

    delivery_start_time_t1 = total_distance_truck1_info[1]

    package.p_delivery_time = total_distance_truck1_info[1]

    myHash.insert(package.pId, package)

    truck1_current_distance_index = next_index

# Head back to base for lunch and for driver to get on next ruck
total_distance_truck1 += Distances.get_distance_value(truck1_current_distance_index, 0, distance_list)
truck1_current_distance_index = 0

# set back to original start time for later use
delivery_start_time_t1 = datetime.timedelta(hours=8, minutes=0, seconds=0)

# initialize the second trucks distance, set the current distance index for the hub to start the day and set the
# delivery start time to when the truck leaves the hub
total_distance_truck2 = 0
truck2_current_distance_index = 0
delivery_start_time_t2 = datetime.timedelta(hours=9, minutes=10, seconds=0)
for package in truck_loads[1]:
    next_index = Distances.get_name_index(names_list, package.pAddress)[0]

    total_distance_truck2_info = Distances.get_total_distance_value(truck2_current_distance_index, next_index,
                                                                    total_distance_truck2, distance_list,
                                                                    delivery_start_time_t2, package)
    total_distance_truck2 = total_distance_truck2_info[0]

    delivery_start_time_t2 = total_distance_truck2_info[1]

    package.p_delivery_time = total_distance_truck2_info[1]

    myHash.insert(package.pId, package)

    truck2_current_distance_index = next_index
# Head back to base
total_distance_truck2 += Distances.get_distance_value(truck2_current_distance_index, 0, distance_list)
truck2_current_distance_index = 0

# set back to original start time for later use
delivery_start_time_t2 = datetime.timedelta(hours=9, minutes=10, seconds=0)

# initialize the third trucks distance, set the current distance index for the hub to start the day and set the
# delivery start time to when the truck leaves the hub
total_distance_truck3 = 0
truck3_current_distance_index = 0
delivery_start_time_t3 = datetime.timedelta(hours=12, minutes=0, seconds=0)
for package in truck_loads[2]:
    next_index = Distances.get_name_index(names_list, package.pAddress)[0]

    total_distance_truck3_info = Distances.get_total_distance_value(truck3_current_distance_index, next_index,
                                                                    total_distance_truck3, distance_list,
                                                                    delivery_start_time_t3, package)
    total_distance_truck3 = total_distance_truck3_info[0]

    delivery_start_time_t3 = total_distance_truck3_info[1]

    package.p_delivery_time = total_distance_truck3_info[1]

    myHash.insert(package.pId, package)

    truck3_current_distance_index = next_index

# Head back to base
total_distance_truck3 += Distances.get_distance_value(truck3_current_distance_index, 0, distance_list)
truck3_current_distance_index = 0

# set back to original start time for later use
delivery_start_time_t3 = datetime.timedelta(hours=12, minutes=10, seconds=0)

#initialize the UI
menu_option = ""
while menu_option != -1:
    # This is going to get input from the user It is going to loop until the user enters in a valid entry that can be
    # split into a time delta
    print("Hello Thank you for using WGUPS")
    print("The total distance traveled for all 3 trucks on the currently loaded data is:",
          + total_distance_truck1 + total_distance_truck2 + total_distance_truck3,
          " This includes there return journey back to the hub")
    print("\nFirst enter the time, this will help us tell you where packages are and when they will arrive")

    valid_input = False
    while not valid_input:

        input_time = str(
            input(
                "Please enter the time in the following format: HHMMSS for example Eight o'clock in the morning would be "
                "080000, 5 secconds past 8 would be 080005 and 5 minutes past 8 would be 080500\n:"))

        try:
            HH = int(input_time[0:2])
            MM = int(input_time[2:4])
            SS = int(input_time[4:6])

            if 24 >= HH >= 0:
                if 60 >= MM >= 0:
                    if 60 >= SS >= 0:
                        input_time_delta = datetime.timedelta(hours=HH, minutes=MM, seconds=SS)
                        valid_input = True
        except ValueError:
            print("Incorrect input format please try again")
            valid_input = False

    # This will set all of the package statuses based on the input time and when the truck leaves the hub
    for item in myHash.table:
        for package in item:
            if package[1].p_delivery_time <= input_time_delta:
                package[1].pStatus = "Delivered"
                myHash.insert(package[1].pId, package[1])
            if package[1].p_delivery_time > input_time_delta:
                if package[1].p_truck == 1:
                    if input_time_delta >= delivery_start_time_t1:
                        package[1].pStatus = "On Truck"
                        myHash.insert(package[1].pId, package[1])
                    if input_time_delta < delivery_start_time_t1:
                        package[1].pStatus = "At Hub"
                        myHash.insert(package[1].pId, package[1])
                if package[1].p_truck == 2:
                    if input_time_delta >= delivery_start_time_t2:
                        package[1].pStatus = "On Truck"
                        myHash.insert(package[1].pId, package[1])
                    if input_time_delta < delivery_start_time_t2:
                        package[1].pStatus = "At Hub"
                        myHash.insert(package[1].pId, package[1])
                if package[1].p_truck == 3:
                    if input_time_delta >= delivery_start_time_t3:
                        package[1].pStatus = "On Truck"
                        myHash.insert(package[1].pId, package[1])
                    if input_time_delta < delivery_start_time_t3:
                        package[1].pStatus = "At Hub"
                        myHash.insert(package[1].pId, package[1])

    print("Thank You!", "All packages are scheduled for Delivery!")

    #This is the start of the main menu
    menu_option = int(input(
        "Main Menu\n\nPlease Enter 1 to search for a specific package by package ID\nPlease Enter 2 to search "
        "for a group of packages based on known information ie address weight etc...\nPlease enter 3 to "
        "display all packages in detail\nPlease enter -1 to quit\n:"))
    #menu option for looking up a package by id
    if menu_option == 1:
        searh_Id = int(input("Please enter the package ID you wish to look up. All package ID's are integers"))
        if myHash.search(searh_Id) == None:
            print("I'm sorry it looks like we dont have a package with ID:", searh_Id)
        else:
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            print(myHash.search(searh_Id))

        input("Press Enter to continue")

    # Search by ID, address, deadline, delivery city, delivery zip, weight, status
    if menu_option == 2:
        submenu_option = int(input("Return packages based on the following components\nPlease Enter 1 to return all "
                                   "packages with an ID number\nPlease Enter 2 to return all packages at an address\n"
                                   "Please Enter 3 to return all packages with a specific Deadline\nPlease Enter 4 to "
                                   "return all packages delivered to a specific City\nPlease Enter 5 to return all "
                                   "packages in a specific Zip Code\nPlease enter 6 to return all packages with a "
                                   "specific weight in kilos\nPlease enter 7 to return all packages that are at the "
                                   "Hub, on the truck, or already delivered\n:"))

        if submenu_option == 1:
            searh_Id = int(input("Please enter the package ID you wish to look up. All package ID's are integers\n:"))
            if myHash.search(searh_Id) == None:
                print("I'm sorry it looks like we dont have a package with ID:", searh_Id)
            else:
                print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                      "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
                print(myHash.search(searh_Id))

            input("Press Enter to continue")

        if submenu_option == 2:
            input_address = input(
                "Please Enter the address of a package or group of packages you wish to look up. It must be exactly "
                "as it is in our "
                "system!\n:")
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:
                    if package[1].pAddress == input_address:
                        print(package[1])
            print("\nIf no packages appear above the address doesn't match one in our system")
            input("Press Enter to continue")

        if submenu_option == 3:
            input_deadline = str(input(
                "Please Enter the Delivery Deadline of a group of packages you wish to look up. It must be exactly as "
                "it is "
                "in our system! Our Current Deadlines are '10:30 AM', '09:00 AM', and 'EOD'\n:"))
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:

                    if package[1].pDeadline == input_deadline:
                        print(package[1])
            print("\nIf no packages appear above the Delivery Deadline doesn't match one in our system")
            input("Press Enter to continue")

        if submenu_option == 4:
            input_city = input(
                "Please Enter the City of a group of packages you wish to look up. It must be exactly as it is in our "
                "system!\n:")
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:
                    if package[1].pCity == input_city:
                        print(package[1])
            print("\nIf no packages appear above the City doesn't match one in our system")
            input("Press Enter to continue")

        if submenu_option == 5:
            input_zip = input(
                "Please Enter the Zip Code of a group of packages you wish to look up. It must be exactly as it is in "
                "our "
                "system!\n:")
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:
                    if package[1].pZip == input_zip:
                        print(package[1])
            print("\nIf no packages appear above the Zip Code doesn't match one in our system")
            input("Press Enter to continue")

        if submenu_option == 6:
            input_weight = input(
                "Please Enter the Weight in Kilos of a package or group of packages you wish to look up. It must be "
                "exactly as "
                "it is in "
                "our "
                "system!\n:")
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:
                    if package[1].pWeight == input_weight:
                        print(package[1])
            print("\nIf no packages appear above the Weight in Kilos doesn't match one in our system")
            input("Press Enter to continue")

        if submenu_option == 7:
            input_status = input(
                "Please Enter the status a package or group of packages you wish to look up. It must be "
                "exactly as it is in our system! Our System uses the following Statuses 'Delivered', 'On Truck,', "
                "'At Hub'\n:")
            print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
                  "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
            for item in myHash.table:
                for package in item:
                    if package[1].pStatus == input_status:
                        print(package[1])
            print("\nIf no packages appear there are no packages in that status or the entered status doesn't match "
                  "one in our system")
            input("Press Enter to continue")
    # Final Menu Option that prints all packages and all of the information associated with them
    if menu_option == 3:
        print("\nPackage Id, Address, City, State, Zip, Delivery Deadline, Mass KILO, page 1 of 1PageSpecial "
              "Notes, Package Status, Delivery Que, Delivery Time, Truck Number")
        for item in myHash.table:
            for package in item:
                print(package[1])

        input("\nPress Enter to continue")



