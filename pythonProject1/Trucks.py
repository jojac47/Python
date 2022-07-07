import datetime
from time import time

import Distances

from collections import Counter


class Trucks:

    def get_ques(myHash):

        # for package in myHash.items():
        # if p.pdeliverytime = "9:00:
        # package.pque = "prio"

        # make these datetime to use datetime.timedelta
        priority_que_time_string = "09:00 AM"
        urgent_que_time_string = "10:30 AM"
        time_format = "%H:%M %p"

        # create date time and just return time for the prio que list
        parsed_prioque_datetime = datetime.datetime.strptime(priority_que_time_string, time_format)
        priority_que_time = parsed_prioque_datetime.strftime(time_format)

        # create date time and just return time for the urgent que list
        parsed_urgent_que_datetime = datetime.datetime.strptime(urgent_que_time_string, time_format)
        urgent_que_time = parsed_urgent_que_datetime.strftime(time_format)

        # this will go therey every package and fill in the que variable based on package deadline.
        for item in myHash:
            for package in item:

                if package[1].pDeadline != "EOD":

                    # create date time and just return time for the package
                    package_deadline_datetime = datetime.datetime.strptime(package[1].pDeadline, time_format)
                    package_deadline_time = package_deadline_datetime.strftime(time_format)
                    # if the package deadline in 9am the queue is in priority queue
                    if package_deadline_time == priority_que_time:
                        package[1].pque = "prio que"
                    # if the package deadline in 1030am the queue is in urgent queue
                    if package_deadline_time == urgent_que_time:
                        package[1].pque = "urgent que"
                # if the deadline is EOD it gets assigned to the normal que
                if package[1].pDeadline == "EOD":
                    package[1].pque = "normal que"

    # This method loops through the hash table and places packages in lists to be loaded onto trucks based on the
    # que. This is the Greedy Algorithm.
    def load_trucks(myHash, names_list, distance_list):

        # initialize all of the lists and variables for the ques, truck loads, and counter for the packages that have
        # to be on truck 2.
        truck1_load = []
        truck2_load = []
        truck3_load = []
        truck1_location = 0
        truck2_location = 0
        truck3_location = 0
        urgent_packages = []
        normal_packages = []
        delayed_urgent_packages = []
        delayed_normal_packages = []
        must_be_on_truck2 = 4
        must_be_on_truck2_packages = []
        # The list for wrong address packages
        wrong_address_packages = []

        # This loop goes through package hash table and check for prio que packages and adds them directly to truck 1
        # because there is only 1 package
        for item in myHash.table:
            for package in item:
                if package[1].pque == "prio que":
                    truck1_load.append(package[1])
                    package[1].p_truck = 1
                    truck1_location = Distances.get_name_index(names_list, package[1].pAddress)[0]
        # This loop goes through package hash table and check for urgen que packages and adds them into a new list
        for item in myHash.table:
            for package in item:
                if package[1].pque == "urgent que":
                    # delayed on flight packages that are in the urgent que get there own list too
                    if "Delayed" in package[1].pNotes:
                        delayed_urgent_packages.append(package[1])
                    else:
                        urgent_packages.append(package[1])
        # This loop goes through package hash table and check for normal que packages and adds them into a new list
        for item in myHash.table:
            for package in item:
                if package[1].pque == "normal que":
                    if ("Delayed" not in package[1].pNotes) and ("Wrong" not in package[1].pNotes):
                        normal_packages.append(package[1])
                    else:
                        # put delayed normal packages in the delayed normal packages list.
                        delayed_normal_packages.append(package[1])
        # loop through every package in urgent packages and delayed urgent packages. This loop is for when removing
        # the items from the list causes the list to break temporarily
        while (len(urgent_packages) > 0) or (len(delayed_urgent_packages) > 0):
            # Loop through every package in in urgent packages. as long as no truck is assigned  get the shortest
            # distance from the current location and store it.
            for package in urgent_packages:
                if package.p_truck == 0:
                    truck1_shortest_distance = Distances.get_shortest_distance_value(truck1_location,
                                                                                     names_list,
                                                                                     distance_list,
                                                                                     urgent_packages)
                # loop through the packages again until the package delivery address matches shortest distance
                # address and load it onto the truck and update the hashtable with the assigned truck
                for u_package in urgent_packages:
                    if u_package.pAddress == truck1_shortest_distance[2]:
                        truck1_load.append(u_package)
                        urgent_packages.remove(u_package)
                        u_package.p_truck = 1
                        truck1_location = truck1_shortest_distance[0]
                        myHash.insert(u_package.pId, u_package)
            # Loop through every package in in urgent packages. as long as no truck is assigned  get the shortest
            # distance from the current location and store it.
            for package in delayed_urgent_packages:
                if package.p_truck == 0:
                    truck2_shortest_distance = Distances.get_shortest_distance_value(truck2_location,
                                                                                     names_list,
                                                                                     distance_list,
                                                                                     delayed_urgent_packages)

                # loop through the packages again until the package delivery address matches shortest distance
                # address and load it onto the truck and update the hashtable with the assigned truck
                for du_package in delayed_urgent_packages:
                    if du_package.pAddress == truck2_shortest_distance[2]:
                        truck2_load.append(du_package)
                        delayed_urgent_packages.remove(du_package)
                        du_package.p_truck = 2
                        truck2_location = truck2_shortest_distance[0]
                        myHash.insert(du_package.pId, du_package)

        # Loop through the normal packages until there are no more left in the list to be loaded This is to catch
        # breaks in other loops as packages are removed.
        while len(normal_packages) > 0:
            # Loop through every package in in normal packages. as long as no truck is assigned  get the shortest
            # distance from the current location and store it.
            for package in normal_packages:
                if package.p_truck == 0:
                    truck1_shortest_distance = Distances.get_shortest_distance_value(truck1_location, names_list,
                                                                                     distance_list, normal_packages)
                # loop through the packages again until the package delivery address matches shortest distance
                # address and load it onto the truck and update the hashtable with the assigned truck
                for npackage in normal_packages:
                    if npackage.pAddress == truck1_shortest_distance[2] and (len(truck1_load) < 16):
                        truck1_load.append(npackage)
                        normal_packages.remove(npackage)
                        npackage.p_truck = 1
                        truck1_location = truck1_shortest_distance[0]
                        myHash.insert(npackage.pId, npackage)

            # add back in delayed packages to normal packages to keep package optimization running well
            for cpackage in delayed_normal_packages:

                if "Delayed" in cpackage.pNotes:
                    normal_packages.append(cpackage)
            # add the wrong addres package into its own list because this package cant leave until truck 3 leaves.
            for package in delayed_normal_packages:
                if "Wrong" in package.pNotes:
                    wrong_address_packages.append(package)
            # loop through the pakcages again and get the shortest distance from the current location for each package.
            for package in normal_packages:
                if package.p_truck == 0:
                    truck2_shortest_distance = Distances.get_shortest_distance_value(truck2_location, names_list,
                                                                                     distance_list, normal_packages)
                # loop through the packages again and if the addresses matches the shortest returned value load it on
                # the truck
                for npackage in normal_packages:
                    # This makes sure that all packages make it on truck 2 that need to. but the dynamic counter lets
                    # me keep it optimized as long as possible The check go on through line 186
                    if (npackage.pAddress == truck2_shortest_distance[2]) and (
                            len(truck2_load) < (12 + must_be_on_truck2)):

                        truck2_load.append(npackage)
                        normal_packages.remove(npackage)
                        npackage.p_truck = 2
                        truck2_location = truck2_shortest_distance[0]
                        myHash.insert(npackage.pId, npackage)
                        if "Can only be" in npackage.pNotes:
                            must_be_on_truck2 -= 1
            for package in normal_packages:
                if "Can only be" in package.pNotes:
                    must_be_on_truck2_packages.append(package)


            #add the rest of the packages that must be on truck 2  until the truck is full
            for package in must_be_on_truck2_packages:
                if ("Can only be" in package.pNotes) and (package.p_truck == 0):
                    if len(truck2_load) < 16:
                        truck2_shortest_distance = Distances.get_shortest_distance_value(truck2_location, names_list,
                                                                                         distance_list,
                                                                                         must_be_on_truck2_packages)
                    for req2package in must_be_on_truck2_packages:

                        if truck2_shortest_distance[2] == req2package.pAddress and req2package.p_truck == 0:
                            req2package.p_truck = 2
                            truck2_load.append(req2package)
                            truck2_location = truck2_shortest_distance[0]
                            myHash.insert(req2package.pId, req2package)
                            normal_packages.remove(req2package)
                        else:
                            truck2_load.append(req2package)
                            normal_packages.remove(req2package)
                    must_be_on_truck2_packages = []
            # add back in wrong address package with the correct address and cycle through the remaining names just
            # like above until all packages are loaded.
            for package in wrong_address_packages:
                normal_packages.append(package)

            wrong_address_packages = []

            while len(normal_packages) > 0:
                for package in normal_packages:
                    if package.pId == 9:
                        package.pAddress = "410 S State St."
                        package.pCity = "Salt Lake City"
                        package.pState = "UT"
                        package.pZip = "84111"

                for package in normal_packages:
                    if package.p_truck == 0:
                        truck3_shortest_distance = Distances.get_shortest_distance_value(truck3_location, names_list,
                                                                                         distance_list, normal_packages)

                        if package.pAddress == truck3_shortest_distance[2]:
                            package.p_truck = 3
                            truck3_load.append(package)
                            truck3_location = truck3_shortest_distance[0]
                            myHash.insert(package.pId, package)
                            normal_packages.remove(package)
        #return the 3 truck load lists.
        return truck1_load, truck2_load, truck3_load
