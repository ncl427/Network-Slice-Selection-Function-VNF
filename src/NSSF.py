#NSSF.py
"""Module in Charge of selecting the right Network Slice with Information from
User Equipment, Type of Service and other Subscriber Information"""

#For object Database
#Management
from ZEO.ClientStorage import ClientStorage
from NSlice import NSlice
from MDDVector import MDDVector
from ZODB import FileStorage, DB
from time import sleep
from DataBase import DataBase
from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from models.Mdd import Mdd
from models.ueAttachObj import ueAttachObj
import BTrees.OOBTree
import transaction
import random
import pickle


"""Define Functionality of NSSF, each of these functions represent a step
of the Algorithm that was proposed"""

ServiceType = ['Video', 'SNS', 'IoT', 'Web', 'Messaging'] #Type of Services

"""Database creation"""
def getSliceroot():
    Slicesdb = DataBase('Database/NS.config') #holding Slice Object Information
    Sliceroot = Slicesdb.dbroot #Network Slice DB object
    return Sliceroot

def getUESRoot():
      #Creates a UEId and NSId that represent connection information
     UESlice = DataBase('Database/Table.config') #for keeping Connection Information
     UESRoot = UESlice.dbroot #Local Table for Connection DB
     return UESRoot

#InsertSlice
"""Funcion in charge of inserting Slice information into the Object DataBase"""
def InsertSlice(SliceId, Service, Sliceroot):
    Sliceroot["NS" + str(SliceId + 1)] = NSlice(SliceId+1, Service)

#SliceInitialization
"""Function in charge of making the Initial State of the Slice Database, In
This case it is requiered for the local operation, but in the Final Project This
information is gonna be provided by OPENSTACK/ONOS"""
def SliceInitialization(Sliceroot):
    if not Sliceroot.values():
        while True:
            try:
                NumberofSlices = int(raw_input("Enter a number of Network Slices: "))
                while NumberofSlices > 5 or NumberofSlices == 0 :
                    NumberofSlices = int(raw_input("Enter values from 1 - 5: "))
                break
            except:
                print "Please use only Numbers"
        x=0
        Sample = random.sample(ServiceType, NumberofSlices) #Not repeating services in Slices
        while (x < NumberofSlices):
            InsertSlice(x, Sample.pop(), Sliceroot) #Populating the Slice DB
            x += 1
        transaction.commit()

#RecieveUEInfo
"""Prompt for UE-ID request, then calls a Service selection function and
registering UE in Local DataBase"""
def RecieveUEInfo(UESRoot, ConnInfo):
#    while True: #Infinite Loop for catching incorrect input
#        try:
#            UEId = int(raw_input("Enter UE-ID: "))#This is just for this scenario
#            while UEId == 0:
#                UEId = int(raw_input("Enter values above 1: "))
#            break
#        except:
#            print "Please use only Numbers"
    count = 0 #Internal Counter for comparissions
    Bigio = "UENS" + str(ConnInfo.UEId) #Comparission
#    i = let_user_pick(ServiceType)#Calls a function for selecting Type of Service
    i = ConnInfo.ServiceType
    try:
        UENService = MDDVector(ServiceType[i-1], ConnInfo.UEId)
    except:
        UENService = MDDVector("NotFound", ConnInfo.UEId)
    #Saves Type of Service and UE ID for later use

    for key in UESRoot.keys():
        if Bigio == key:
            count += 1
    if count > 0:
        print "Connection Resummed Proceeding to Select a Slice"
        #sleep(0.5)
    else:
        print "Sending Attach Request to MME"
        #sleep(0.5)
        #attachRequestMME(MDDVector.UEId,MDDVector.ServiceType)
        #Sends Attach Request to MME, Not Implemented
        RegisterUENSId(ConnInfo.UEId, ConnInfo.NSId, UESRoot) #Registers Local Database
    return UENService #Returns the Type of service to use it in Slice Verification

#RegisterUENSId
"""Uses a Object Database for keeping UE-ID and NS-ID information while the
connection is active"""
def RegisterUENSId(UEId, NSId, UESRoot):
    UESRoot["UENS"+ str(UEId)] = [UEId, NSId]
    print "User Equipment Registration Is: ", UESRoot#["UENS"+ str(UEid)]
    transaction.commit()
    #sleep(0.5)

#let_user_pick
"""Presents an Option List for selecting the type of services that are configure
in our Network, """
def let_user_pick(options):
    print("Select Type of Service: ")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element)) #Option presentation format
    i = raw_input("Enter number: ")
    while True:
        try:
            if 0 < int(i) <= len(options):
                return int(i)
            else:
                i = raw_input("Please enter correct number: ")
        except:
            i = raw_input("Please enter correct value: ")
    return None

#SliceVerification
"""Checks if the required service can be provided by an Existing Network Slice,
In case it does not exist, will request a Creation of IT to OpenStack/ONOS/XoS """
def SliceVerification(MDDVector, Sliceroot, UESRoot):
    for key in Sliceroot.keys():
        if Sliceroot[key].ServiceType == MDDVector.ServiceType:
            print "The UE is using the network for: ", Sliceroot[key].ServiceType
            RegisterUENSId(MDDVector.UEId, Sliceroot[key].NSId, UESRoot) #Updates the UE,NS info in local Database
            Sliceroot[key].getUEId(MDDVector.UEId) #Adds the UE to the Network Slice DB, (List of UE served)
            MDDVector.NSId = Sliceroot[key].NSId #Updates the Connection Object Information
            #print Sliceroot[key].UEId
            transaction.commit()
            #sleep(0.5)
            return True
    print "Service Type", MDDVector.ServiceType, "Not Found, Requesting Slice Creation"
    return False
    #requestSlice(Localtable[0])

"""When the Flow ends, it Will send the Connection Information to UE, to let it know to
which Network Slice to connect"""
def sendAuthInfo(UENService):
    print "Sent Connection Information to UE/vBBU"
    #sleep(0.5)

"""Removes the User Equipment ID from the local tables and the NS register"""
def removeUE(UEID, NSTable, ConnTable):
    #sleep(0.5)
    print "Disconnecting User Equipment:", UEID
    for key in NSTable.keys():
        if UEID in NSTable[key].UEId:
            NSTable[key].UEId.remove(UEID)
            transaction.commit()
    for key in ConnTable.keys():
        if UEID == ConnTable[key][0]:
            del ConnTable[key]
            transaction.commit()

"""Send Attach information to MME for network Authentication"""
def attachRequestMME(UEId,UENService):
    c = connect(host="192.168.0.170",port=10123)
    response = c.call.auth(UEId)
    if response == True:
        "User Equipment Attacht Approved"
        return True
    else:
        print "Connection Refused"
        quit()
""" Creates the MDDVector with information from UE and Core NEtwork, it will be used
to send back to the vBBU"""
def createMDDVector(Object):
    mddVector = Mdd()
    mddVector.nesId = Object.NSId
    mddVector.tempId = Object.UEId + str(Object.NSId) + "ASIF"
    return mddVector

"""Main Function with the Flow of the Module"""
def attach(ConnInfo):

    connObject = pickle.loads(ConnInfo) #Parses the Object with Connection Info.
    ueInfo = MDDVector(connObject.serviceType, connObject.ip)
    Sliceroot = getSliceroot() #NS DB creation
    UESRoot = getUESRoot() #Local DB creation
    SliceInitialization(Sliceroot) #If no slice exists in DB, populate it with info
    UENService = RecieveUEInfo(UESRoot, ueInfo) #Recives UE information
    if SliceVerification(UENService, Sliceroot, UESRoot): #Verifies Service Type with NS
        sendAuthInfo(UENService) #Finish the flow and sends info to UE

    for key in Sliceroot.keys():
        print("{}: {}, Service: {}, UE:".format(key, Sliceroot[key],Sliceroot[key].ServiceType)),
        try:
            print Sliceroot[key].UEId

        except:
            print "No UEId assigned"
    print "User Equipment ", UENService.UEId, "with Slice Id ", UENService.NSId,
    print "is using Internet for ", UENService.ServiceType


    mddVector = createMDDVector(UENService)
    return mddVector

"""Detach function, It will delete all user information from the connection tables"""
def detach(ConnInfo):
    MDDVector = pickle.loads(ConnInfo) #Parses the Object with Connection Info.
    Sliceroot = getSliceroot() #Open Slice Database
    UESRoot = getUESRoot() #Open Connection Database
    removeUE(MDDVector.UEId, Sliceroot, UESRoot)
    for key in Sliceroot.keys():
        print("{}: {}, Service: {}, UE:".format(key, Sliceroot[key],Sliceroot[key].ServiceType)),
        try:
            print Sliceroot[key].UEId

        except:
            print "No UEId assigned"
    #sleep(0.5)
    print "Connection Table Info is: ", UESRoot


#if __name__ == '__main__':
#    main()
