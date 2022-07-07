import csv

from HashTable import ChainingHashTable


class Package:
    """Package Class for creating and looking up packages"""

    # constructor for packages
    def __init__(self, pId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pque="holder",
                 p_delivery_time=None, p_truck=0):
        self.pId = pId
        self.pAddress = pAddress
        self.pCity = pCity
        self.pState = pState
        self.pZip = pZip
        self.pDeadline = pDeadline
        self.pWeight = pWeight
        self.pNotes = pNotes
        self.pStatus = pStatus
        self.pque = pque
        self.p_delivery_time = p_delivery_time
        self.p_truck = p_truck

    # Allowing output of package object
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.pId, self.pAddress, self.pCity, self.pState, self.pZip, self.pDeadline, self.pWeight, self.pNotes,
            self.pStatus, self.pque, self.p_delivery_time, self.p_truck)


    #insert package data from the csv into the hash table
    def load_Package(fileName, myHash):
        with open(fileName) as Packages_CSV:
            Packages_Data = csv.reader(Packages_CSV, delimiter=",")
            next(Packages_Data)
            for package in Packages_Data:
                pID = int(package[0])
                pAddress = (package[1])
                pCity = (package[2])
                pState = (package[3])
                pZip = (package[4])
                pDeadline = (package[5])
                pWeight = (package[6])
                pNotes = (package[7])
                pStatus = "At Hub"
                pque = "holder"
                p_delivery_time = "holder"
                p_truck = 0

                package = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pque,
                                  p_delivery_time, p_truck)

                myHash.insert(pID, package)
