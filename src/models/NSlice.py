#NSlice.py
import ZODB
from persistent import Persistent

"""A class that defines the atributes that a Network Slice should have for
using in the NSSF(Network Slice Selection Funciton)"""
class NSlice(Persistent):
  def __init__(self, NSId, ServiceType):
      """Creates a Slice Object with Defined Atributes"""
      self.NSId = NSId
      self.ServiceType = ServiceType
      self.UEId = []

  def getUEId(self, UEId):
      if UEId not in self.UEId:
          self.UEId.append(UEId)
          self._p_changed = 1

  def remUE(self, UEId):
      self.UEId.remove(UEId)
      self._p_changed = 1

  def getCPId(self, CPId):
      self.CPId = CPId

"""Here is the class for the object that I am using to represent MDDVector
class UENS(Persistent):
    def __init__(self, ServiceType, UEId):
        self.ServiceType = ServiceType
        self.UEId = UEId
        self.NSId = 0
"""
