from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from MDDVector import MDDVector
import pickle


c = connect(host="127.0.0.1",port=10123)

MDDVector = MDDVector(4,20)
pickledMDDVector = pickle.dumps(MDDVector)
Authentication = pickle.loads(c.call.networkAttach(pickledMDDVector))
# do something here ...
print "Network State -", "User Equipment:", Authentication.UEId, "Will connect",
print "to Network Slice:", Authentication.NSId
