from ZEO.ClientStorage import ClientStorage
from ZODB import DB
import ZODB.config

class DataBase(object):
  def __init__(self, confile):
    self.db = ZODB.config.databaseFromURL(confile)  #Creates an Object Database
    self.connection = self.db.open()
    self.dbroot = self.connection.root()

  def close(self): #Close the connection to the database
    self.connection.close()
    self.db.close()
    self.storage.close()
