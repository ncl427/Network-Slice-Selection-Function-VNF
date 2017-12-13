#MDDVector.py
import ZODB
from persistent import Persistent

"""Here is the class for the object that I am using to represent MDDVector"""

class netObject(Persistent):
    def __init__(self, ServiceType, UEId):
        self.ServiceType = ServiceType
        self.UEId = UEId
        self.NSId = 0       #At this moment is an Integer
        self.TEMPId = 0     #Will be created by adding information from all modules
        self.CPId = 0       #Includes the UEId plus other connection information


    def getCPId(self, CPId):
        self.CPId = CPId
