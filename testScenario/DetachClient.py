from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from MDDVector import MDDVector
import pickle


c = connect(host="127.0.0.1",port=10123)

MDDVector = MDDVector(20,"117.17.102.21")
pickledMDDVector = pickle.dumps(MDDVector)
c.call.networkDetach(pickledMDDVector)
# do something here ...
print "User Equipment Disconnected"
